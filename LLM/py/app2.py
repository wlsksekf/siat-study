import os
from pathlib import Path

import streamlit as st
import truststore
from dotenv import load_dotenv

from json_db2 import clear_analyses, init_pdf_db, load_analyses, save_analysis
from openai_service2 import create_openai_client, get_runtime_diagnostics
from pdf import (
    extract_images_from_pdf,
    extract_tables_to_excel,
    extract_text_from_pdf,
    get_pdf_runtime_diagnostics,
    save_uploaded_pdf,
    summarize_pdf_text_only,
)


# SSL 인증서와 환경 변수를 앱 시작 시 한 번만 준비합니다.
truststore.inject_into_ssl()
load_dotenv()
init_pdf_db()


st.set_page_config(page_title="PDF Analyzer 2", page_icon="📄", layout="wide")


# 가장 최근 분석 결과를 세션에 유지해 탭에서 재사용합니다.
if "latest_result" not in st.session_state:
    st.session_state["latest_result"] = None


with st.sidebar:
    # 분석 옵션과 현재 실행 환경 정보를 사이드바에 모읍니다.
    st.header("설정")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    runtime_info = get_runtime_diagnostics()
    pdf_runtime_info = get_pdf_runtime_diagnostics()

    model_name = st.text_input("모델", value="gpt-4.1-nano")
    custom_prompt = st.text_area(
        "분석 요청",
        value="이 PDF를 한국어로 요약하고 핵심 내용, 주요 숫자, 실무 포인트를 정리해줘.",
        height=120,
    )
    extract_images_option = st.checkbox("PDF 이미지 추출", value=True)
    extract_tables_option = st.checkbox("PDF 표 추출 후 Excel 저장", value=True)

    st.caption(f"Python: `{runtime_info['python_executable']}`")
    st.caption(f"EasyOCR 사용 가능: `{'예' if runtime_info['easyocr_available'] else '아니오'}`")
    st.caption(f"img2table 사용 가능: `{'예' if pdf_runtime_info['img2table_available'] else '아니오'}`")

    if st.button("기록 초기화"):
        clear_analyses()
        st.session_state["latest_result"] = None
        st.rerun()


st.title("PDF 분석기")
st.caption("텍스트 추출, OCR, 이미지 추출, 표 추출(Excel 저장), OpenAI 요약을 한 번에 처리합니다.")

uploaded_file = st.file_uploader("PDF 파일 업로드", type=["pdf"])

if uploaded_file is not None and st.button("PDF 분석 시작", type="primary"):
    # 업로드한 원본 PDF를 먼저 저장한 뒤 후속 작업에서 같은 경로를 사용합니다.
    saved_pdf_path = save_uploaded_pdf(uploaded_file)

    with st.spinner("PDF 텍스트를 추출하는 중입니다..."):
        text_result = extract_text_from_pdf(saved_pdf_path)

    image_paths: list[str] = []
    if extract_images_option:
        # PDF 내부에 포함된 원본 이미지만 추출합니다.
        with st.spinner("PDF 이미지를 추출하는 중입니다..."):
            image_paths = extract_images_from_pdf(saved_pdf_path)

    excel_path = ""
    table_count = 0
    if extract_tables_option:
        # 표가 감지되면 각 표를 시트별로 나눠 Excel 파일로 저장합니다.
        with st.spinner("PDF 표를 추출하는 중입니다..."):
            excel_path, table_count = extract_tables_to_excel(saved_pdf_path)

    summary = "OpenAI API Key가 없어 요약을 건너뛰었습니다."
    if openai_api_key:
        with st.spinner("OpenAI로 PDF 내용을 요약하는 중입니다..."):
            client = create_openai_client(openai_api_key)
            summary = summarize_pdf_text_only(
                client=client,
                file_name=uploaded_file.name,
                extracted_text=text_result["full_text"],
                user_prompt=custom_prompt,
                model=model_name,
            )

    latest_result = {
        "file_name": uploaded_file.name,
        "saved_pdf_path": str(saved_pdf_path),
        "page_count": text_result["page_count"],
        "full_text": text_result["full_text"],
        "preview_text": text_result["preview_text"],
        "ocr_used": text_result["ocr_used"],
        "ocr_available": text_result["ocr_available"],
        "summary": summary,
        "image_paths": image_paths,
        "image_count": len(image_paths),
        "excel_path": excel_path,
        "table_count": table_count,
    }
    # 화면 표시용 결과와 기록 저장용 결과를 함께 남깁니다.
    st.session_state["latest_result"] = latest_result

    save_analysis(
        file_name=uploaded_file.name,
        page_count=text_result["page_count"],
        extracted_text=text_result["full_text"],
        summary=summary,
    )


latest_result = st.session_state.get("latest_result")
if latest_result:
    # 결과를 기능별 탭으로 나눠 한 화면에서 확인할 수 있게 합니다.
    summary_tab, text_tab, image_tab, table_tab, history_tab = st.tabs(
        ["요약", "텍스트", "이미지", "표", "기록"]
    )

    with summary_tab:
        st.subheader("분석 결과")
        st.write(f"파일명: `{latest_result['file_name']}`")
        st.write(f"저장 경로: `{latest_result['saved_pdf_path']}`")
        st.write(f"페이지 수: `{latest_result['page_count']}`")
        st.write(f"OCR 사용: `{'예' if latest_result['ocr_used'] else '아니오'}`")
        st.write(f"추출 이미지 수: `{latest_result['image_count']}`")
        st.write(f"추출 표 수: `{latest_result['table_count']}`")
        st.markdown(latest_result["summary"])

        if not latest_result["ocr_available"] and "(No extractable text found)" in latest_result["full_text"]:
            st.warning(
                "현재 실행 중인 Python 환경에서 EasyOCR을 사용할 수 없습니다. "
                "OCR이 필요하면 해당 가상환경에 `easyocr`를 설치한 뒤 다시 실행해주세요."
            )

    with text_tab:
        st.subheader("추출 텍스트")
        st.text_area(
            "추출 텍스트 미리보기",
            value=latest_result["preview_text"],
            height=500,
        )

    with image_tab:
        st.subheader("PDF 내 이미지 추출")
        if latest_result["image_paths"]:
            st.write(f"총 `{latest_result['image_count']}`개의 이미지를 저장했습니다.")
            for image_path in latest_result["image_paths"]:
                st.image(image_path, caption=Path(image_path).name)
        else:
            st.info("추출된 이미지가 없습니다.")

    with table_tab:
        st.subheader("PDF 표 추출 후 Excel 저장")
        if latest_result["excel_path"]:
            excel_file = Path(latest_result["excel_path"])
            st.write(f"표 `{latest_result['table_count']}`개를 Excel로 저장했습니다.")
            st.write(f"저장 경로: `{latest_result['excel_path']}`")
            st.download_button(
                label="표 Excel 다운로드",
                data=excel_file.read_bytes(),
                file_name=excel_file.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        elif extract_tables_option and not pdf_runtime_info["img2table_available"]:
            st.warning("현재 환경에는 `img2table`이 없어 표 추출 기능을 사용할 수 없습니다.")
        else:
            st.info("추출된 표가 없습니다.")

    with history_tab:
        st.subheader("최근 분석 이력")
        history = list(reversed(load_analyses()))
        if not history:
            st.info("저장된 분석 이력이 없습니다.")
        else:
            for item in history[:10]:
                with st.expander(f"{item['created_at']} | {item['file_name']}"):
                    st.write(f"페이지 수: `{item['page_count']}`")
                    st.markdown(item["summary"])
else:
    st.info("PDF를 업로드한 뒤 `PDF 분석 시작`을 눌러주세요.")
