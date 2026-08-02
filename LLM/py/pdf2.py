import io
from pathlib import Path

import fitz  # PyMuPDF
import pandas as pd

# img2table
from img2table.document import PDF as Img2TablePDF
from img2table.ocr import EasyOCR
import re

from openai_service import create_openai_client



# ---------------------------
# 업로드 파일 저장
# ---------------------------
def save_uploaded_pdf(uploaded_file, upload_dir: Path) -> Path:
    upload_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = upload_dir / uploaded_file.name

    # uploaded_file : 파일 자체가 아니라 메모리에 올라온 파일 데이터 객체입니다.
    # name에는 파일 이름, size에는 파일 크기, type에는 파일 타입, getbuffer()는 실제 파일 데이터가 있습니다.
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer()) # getbuffer() 는 파일의 바이너리 데이터를 가져오는 함수입니다.
        # 메모리에 있는 PDF 데이터를 디스크 파일에 그대로 저장합니다.
    
    return pdf_path


# ---------------------------
# PDF 텍스트 추출
# ---------------------------
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    text_parts = []

    # PDF 파일을 context manager로 열기
    # with 블록이 끝나면 자동으로 doc.close()가 실행됩니다.
    with fitz.open(pdf_path) as doc:

        # PDF의 모든 페이지를 순회
        for i, page in enumerate(doc):

            # 페이지에서 텍스트 추출 후 앞뒤 공백 제거
            page_text = page.get_text().strip()

            # 페이지 구분을 위해 페이지 번호를 함께 저장
            text_parts.append(f"\n\n--- PAGE {i+1} ---\n\n{page_text}")

    # 모든 페이지 텍스트를 하나의 문자열로 합쳐서 반환
    return "\n".join(text_parts).strip()


# ---------------------------
# 텍스트만 요약
# ---------------------------
def summarize_pdf_text_only(pdf_text: str, api_key: str) -> str:
    client = create_openai_client(api_key)

    prompt = f"""
다음은 PDF에서 추출한 텍스트입니다.

텍스트만 기준으로 한국어 마크다운 형식으로 요점 정리해 주세요.

형식:
# PDF 요약
## 문서 주제
## 핵심 내용
## 중요 개념
## 결론
## 5줄 요약

주의:
- 이미지나 표는 해석하지 말고 텍스트만 기준으로 정리해 주세요.
- 내용이 불명확하면 추측하지 말고 '텍스트에서 명확하지 않음'이라고 적어 주세요.

[텍스트 시작]
{pdf_text[:120000]}
[텍스트 끝]
"""

    response = client.responses.create(
        model="gpt-4.1-nano",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt}
                ]
            }
        ]
    )

    return response.output_text.strip()


# -------------------------------------------
# PDF 내 이미지 추출
# page.get_images() 사용
# pdf_path : 분석할 PDF 파일 경로
# 반환값 : 저장된 이미지 파일 경로 리스트
# -------------------------------------------
def extract_images_from_pdf(pdf_path: str):
    # 문자열 경로를 Path 객체로 변환합니다.
    # Path 객체를 사용하면 파일 경로 조작이 편리합니다.
    pdf_path = Path(pdf_path)

    # pdf_path.name은 파일 전체 이름
    # pdf_path.stem은 확장자 제외 이름
    # pdf_path.suffix는 확장자

    # 이미지 저장 폴더를 생성합니다.
    # 예: output_streamlit_pdf/images/crop-model
    output_dir = pdf_path.parent.parent / "images" / pdf_path.stem

    # 폴더가 없으면 자동 생성합니다.
    # parents=True : 상위 폴더까지 함께 생성
    # exist_ok=True : 폴더가 이미 있어도 오류 발생하지 않음
    output_dir.mkdir(parents=True, exist_ok=True)

    # PyMuPDF(fitz)를 이용하여 PDF 파일을 엽니다.
    # PyMuPDF(fitz)를 context manager 방식으로 열기
    # with 블록이 끝나면 자동으로 doc.close()가 실행됩니다.
    with fitz.open(pdf_path) as doc:

        # 저장된 이미지 파일 경로를 저장할 리스트
        saved_images = []

        # 전체 이미지 번호를 관리하기 위한 변수
        image_index = 1

        # enumerate(..., start=1) → 페이지 번호를 1부터 시작
        for page_num, page in enumerate(doc, start=1):

            # 현재 페이지에 포함된 이미지 목록을 가져옵니다.
            # full=True : 이미지의 전체 정보 가져오기
            image_list = page.get_images(full=True)

            # 페이지 안의 모든 이미지를 반복합니다.
            for img in image_list:

                # img 튜플의 첫 번째 값은 이미지의 xref ID입니다.
                # xref는 PDF 내부에서 이미지 객체를 식별하는 번호입니다.
                xref = img[0]

                # xref를 이용하여 실제 이미지 데이터를 추출합니다.
                base_image = doc.extract_image(xref)

                # 이미지의 바이너리 데이터 (실제 이미지 파일 데이터)
                image_bytes = base_image["image"]

                # 이미지 확장자 (png, jpg 등)
                image_ext = base_image["ext"]

                # 저장할 이미지 파일 경로 생성
                # page_001_img_001.png 같은 형식으로 저장합니다.
                # :03d → 숫자를 3자리로 표현 (예: 1 → 001)
                image_path = output_dir / f"page_{page_num:03d}_img_{image_index:03d}.{image_ext}"

                # 이미지 파일을 바이너리 모드로 저장합니다.
                with open(image_path, "wb") as f:

                    # 이미지 데이터를 파일로 기록합니다.
                    f.write(image_bytes)

                # 저장된 이미지 경로를 리스트에 추가합니다.
                saved_images.append(str(image_path))

                # 다음 이미지를 위해 번호 증가
                image_index += 1

    # 저장된 이미지 파일 경로 리스트 반환
    return saved_images


# ---------------------------
# PDF 표 추출 후 Excel 저장
# img2table 사용
# ---------------------------
def clean_excel_illegal_chars(value):

    # isinstance() 는 변수의 데이터 타입(자료형)을 확인하는 함수입니다.
    # 전달된 값이 문자열(str) 타입인지 확인합니다.
    # Excel에서 문제가 되는 제어문자는 대부분 문자열에서 발생합니다.
    if isinstance(value, str):

        # Excel에서 허용되지 않는 제어문자를 제거합니다.
        # \x00-\x08 : NULL ~ Backspace
        # \x0B-\x0C : Vertical Tab, Form Feed
        # \x0E-\x1F : 기타 제어 문자
        # 이러한 문자가 있으면 openpyxl에서 오류가 발생할 수 있습니다.
        value = re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F]", "", value)

        # 문자열의 앞뒤 공백을 제거합니다.
        value = value.strip()

        # 제어문자를 제거한 후 문자열이 비어 있으면
        # Excel에 빈 문자열("")을 반환합니다.
        # 의미 없는 데이터가 저장되는 것을 방지합니다.
        if not value:
            return ""

        # 정리된 문자열을 반환합니다.
        return value

    # 문자열이 아닌 경우 (숫자, None 등)는 그대로 반환합니다.
    return value

def clean_dataframe_for_excel(df: pd.DataFrame) -> pd.DataFrame:
    # df.map()은 데이터프레임의 모든 개별 원소(Cell)를 하나씩 순회하며 
    # 괄호 안에 지정된 함수(clean_excel_illegal_chars)를 적용합니다.
    # 결과적으로 '정제된 값'들로 구성된 새로운 데이터프레임을 반환합니다. 
    return df.map(clean_excel_illegal_chars)

def extract_tables_to_excel(pdf_path: str):

    # 문자열 경로를 Path 객체로 변환합니다.
    # Path 객체를 사용하면 파일 경로 조작이 편리합니다.
    pdf_path = Path(pdf_path)

    # 표 추출 결과를 저장할 폴더를 생성합니다.
    # 예: output_streamlit_pdf/tables
    output_dir = pdf_path.parent.parent / "tables"

    # 폴더가 없으면 자동 생성합니다.
    output_dir.mkdir(parents=True, exist_ok=True)

    # 생성할 Excel 파일 경로
    # 예: crop-model_tables.xlsx
    excel_path = output_dir / f"{pdf_path.stem}_tables.xlsx"


    # -------------------------------------------------
    # OCR 설정
    # -------------------------------------------------

    # EasyOCR 객체 생성
    # 한글(ko)과 영어(en)를 인식하도록 설정합니다.
    ocr = EasyOCR(lang=["ko", "en"])


    # -------------------------------------------------
    # PDF 로드
    # -------------------------------------------------

    # img2table 라이브러리를 사용하여 PDF 파일을 읽습니다.
    pdf = Img2TablePDF(
        src=str(pdf_path),

        # 페이지 회전 감지 여부
        # True로 하면 자동 회전 처리하지만 속도가 느려질 수 있습니다.
        detect_rotation=False
    )


    # -------------------------------------------------
    # PDF에서 표 추출
    # -------------------------------------------------

    extracted_tables = pdf.extract_tables(

        # OCR 엔진 (이미지 기반 표 인식)
        ocr=ocr,

        # 명시적인 선이 없어도 행을 추정
        implicit_rows=True,

        # 명시적인 선이 없어도 열을 추정
        implicit_columns=True,

        # 테두리가 없는 표도 탐지
        borderless_tables=True,

        # OCR 인식 신뢰도 기준
        min_confidence=50
    )


    # 추출된 표 개수를 저장하는 변수
    table_count = 0


    # -------------------------------------------------
    # Excel 파일 생성
    # -------------------------------------------------

    # pandas ExcelWriter를 사용하여 Excel 파일 작성
    # engine="openpyxl" : Excel 파일(.xlsx) 저장 엔진
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:

        # 페이지별로 추출된 표를 반복합니다.
        for page_number, tables in extracted_tables.items():

            # 한 페이지 안에 여러 개의 표가 있을 수 있습니다.
            for idx, table in enumerate(tables, start=1):

                # 표 데이터를 DataFrame 형태로 가져옵니다.
                df = table.df

                # DataFrame이 없거나 비어 있으면 건너뜁니다.
                if df is None or df.empty:
                    continue


                # -------------------------------------------------
                # Excel 저장 오류 방지
                # -------------------------------------------------

                # PDF에서 추출된 텍스트에는 제어문자가 포함될 수 있습니다.
                # 예: \x00 \x01 \x0B
                # 이러한 문자가 있으면 openpyxl에서 오류가 발생합니다.
                #
                # 예:
                # IllegalCharacterError:
                # "     cannot be used in worksheets."
                #
                # 그래서 Excel 저장 전에 DataFrame 전체 데이터를 정리합니다.
                df = clean_dataframe_for_excel(df)


                # -------------------------------------------------
                # Excel Sheet 이름 생성
                # -------------------------------------------------

                # 예: p1_t1 : 1페이지의 첫 번째 테이블
                sheet_name = f"p{page_number}_t{idx}"

                # Excel Sheet 이름은 최대 31자까지 가능합니다.
                df.to_excel(
                    writer,
                    sheet_name=sheet_name[:31],
                    index=False
                )

                # 추출된 표 개수 증가
                table_count += 1


    # -------------------------------------------------
    # 표가 없는 경우 처리
    # -------------------------------------------------

    if table_count == 0:

        # Excel 파일이 생성되었다면 삭제합니다.
        if excel_path.exists():
            excel_path.unlink()

        # 표가 없음을 반환
        return None, 0


    # -------------------------------------------------
    # 결과 반환
    # -------------------------------------------------

    # Excel 파일 경로와 추출된 표 개수 반환
    return str(excel_path), table_count