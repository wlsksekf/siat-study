from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd

try:
    import fitz
except ModuleNotFoundError:
    try:
        import pymupdf as fitz
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "PyMuPDF가 설치되어 있지 않습니다. `python -m pip install PyMuPDF` 후 다시 실행해주세요."
        ) from exc

try:
    from img2table.document import PDF as Img2TablePDF
except ModuleNotFoundError:
    Img2TablePDF = None

try:
    from img2table.ocr import EasyOCR as Img2TableEasyOCR
except ModuleNotFoundError:
    Img2TableEasyOCR = None

try:
    import easyocr
except ModuleNotFoundError:
    easyocr = None

try:
    from openai_service2 import analyze_pdf_text, extract_text_from_pdf_bytes
except ModuleNotFoundError:
    from .openai_service2 import analyze_pdf_text, extract_text_from_pdf_bytes


LLM_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = LLM_DIR / "uploaded"
OUTPUT_DIR = LLM_DIR / "output"
IMAGE_DIR = OUTPUT_DIR / "images"
TABLE_DIR = OUTPUT_DIR / "tables"

# Excel이 허용하지 않는 제어 문자를 저장 전에 제거합니다.
ILLEGAL_EXCEL_CHARS_RE = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")


def ensure_output_dirs() -> None:
    # 분석 결과물이 저장될 기본 폴더를 미리 만들어 둡니다.
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)


def get_pdf_runtime_diagnostics() -> dict[str, bool]:
    return {
        "img2table_available": Img2TablePDF is not None,
        "img2table_easyocr_available": Img2TableEasyOCR is not None,
        "easyocr_available": easyocr is not None,
    }


def save_uploaded_pdf(uploaded_file) -> Path:
    # Streamlit 업로드 파일을 디스크에 저장해 후속 처리에서 재사용합니다.
    ensure_output_dirs()
    save_path = UPLOAD_DIR / uploaded_file.name
    save_path.write_bytes(uploaded_file.getbuffer())
    return save_path


def extract_text_from_pdf(pdf_path: str | Path) -> dict[str, Any]:
    # 공통 텍스트 추출 로직은 openai_service2 쪽 함수를 그대로 사용합니다.
    path = Path(pdf_path)
    return extract_text_from_pdf_bytes(path.read_bytes())


def summarize_pdf_text_only(
    client,
    file_name: str,
    extracted_text: str,
    user_prompt: str | None = None,
    model: str = "gpt-4.1-nano",
) -> str:
    if not extracted_text.strip():
        return "추출된 텍스트가 없어 요약할 수 없습니다."

    # 텍스트 추출 결과만 OpenAI에 전달해 요약합니다.
    return analyze_pdf_text(
        client=client,
        file_name=file_name,
        extracted_text=extracted_text,
        user_prompt=user_prompt,
        model=model,
    )


def extract_images_from_pdf(pdf_path: str | Path) -> list[str]:
    ensure_output_dirs()
    path = Path(pdf_path)
    saved_images: list[str] = []

    with fitz.open(path) as doc:
        # 같은 PDF의 이미지들을 한 폴더에 모아 저장합니다.
        pdf_stem = path.stem
        target_dir = IMAGE_DIR / pdf_stem
        target_dir.mkdir(parents=True, exist_ok=True)

        for page_index, page in enumerate(doc, start=1):
            image_list = page.get_images(full=True)
            for image_index, image_info in enumerate(image_list, start=1):
                xref = image_info[0]
                image_data = doc.extract_image(xref)
                image_bytes = image_data["image"]
                image_ext = image_data.get("ext", "png")
                image_path = target_dir / f"{pdf_stem}_page{page_index}_img{image_index}.{image_ext}"
                image_path.write_bytes(image_bytes)
                saved_images.append(str(image_path))

    return saved_images


def clean_excel_illegal_chars(value):
    if value is None:
        return ""
    if not isinstance(value, str):
        return value
    return ILLEGAL_EXCEL_CHARS_RE.sub("", value)


def clean_dataframe_for_excel(df: pd.DataFrame) -> pd.DataFrame:
    return df.map(clean_excel_illegal_chars)


def build_table_ocr():
    if Img2TableEasyOCR is None:
        return None
    return Img2TableEasyOCR(lang=["ko", "en"], kw={"gpu": False})


_CELL_OCR_READER = None


def build_cell_ocr_reader():
    global _CELL_OCR_READER

    if easyocr is None:
        return None
    if _CELL_OCR_READER is None:
        _CELL_OCR_READER = easyocr.Reader(["ko", "en"], gpu=False)
    return _CELL_OCR_READER


def needs_cell_ocr(df: pd.DataFrame) -> bool:
    for value in df.fillna("").to_numpy().flatten():
        if isinstance(value, str) and re.search(r"[\x00-\x1F]", value):
            return True
    return False


def ocr_table_cells(table, page_image) -> pd.DataFrame | None:
    reader = build_cell_ocr_reader()
    if reader is None:
        return None

    rows: list[list[str]] = []
    for row_index in sorted(table.content.keys()):
        row_values: list[str] = []
        for cell in table.content[row_index]:
            x1 = max(int(cell.bbox.x1), 0)
            y1 = max(int(cell.bbox.y1), 0)
            x2 = min(int(cell.bbox.x2), page_image.shape[1])
            y2 = min(int(cell.bbox.y2), page_image.shape[0])

            if x2 <= x1 or y2 <= y1:
                row_values.append("")
                continue

            crop = page_image[y1:y2, x1:x2]
            texts = reader.readtext(crop, detail=0, paragraph=True)
            text = "\n".join(part.strip() for part in texts if part and part.strip()).strip()
            row_values.append(text)
        rows.append(row_values)

    return pd.DataFrame(rows)


def extract_tables_to_excel(pdf_path: str | Path) -> tuple[str, int]:
    # img2table이 없으면 앱은 유지하고 표 추출만 건너뜁니다.
    if Img2TablePDF is None:
        return "", 0

    ensure_output_dirs()
    path = Path(pdf_path)
    pdf = Img2TablePDF(src=str(path), detect_rotation=False)
    ocr = build_table_ocr()
    extract_options: dict[str, Any] = {
        "implicit_rows": True,
        "implicit_columns": True,
        "borderless_tables": True,
        "min_confidence": 50,
    }
    if ocr is not None:
        extract_options["ocr"] = ocr

    extracted_tables = pdf.extract_tables(**extract_options)
    table_count = sum(len(page_tables) for page_tables in extracted_tables.values())
    if table_count == 0:
        return "", 0

    # 표마다 시트를 분리해 하나의 Excel 파일로 저장합니다.
    excel_path = TABLE_DIR / f"{path.stem}_tables.xlsx"
    written_table_count = 0
    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        for page_number, page_tables in extracted_tables.items():
            page_image = pdf.images[page_number]
            for index, table in enumerate(page_tables, start=1):
                df = table.df.copy()
                if df.empty:
                    continue

                if needs_cell_ocr(df):
                    ocr_df = ocr_table_cells(table, page_image)
                    if ocr_df is not None and not ocr_df.empty:
                        df = ocr_df

                df = clean_dataframe_for_excel(df)
                df.to_excel(
                    writer,
                    sheet_name=f"p{page_number + 1}_t{index}"[:31],
                    index=False,
                )
                written_table_count += 1

    if written_table_count == 0:
        if excel_path.exists():
            excel_path.unlink()
        return "", 0

    return str(excel_path), written_table_count
