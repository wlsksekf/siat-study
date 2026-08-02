from __future__ import annotations

import sys
from io import BytesIO

import numpy as np
import streamlit as st
from openai import OpenAI

try:
    import fitz
except ModuleNotFoundError:
    try:
        import pymupdf as fitz
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "PyMuPDF가 설치되어 있지 않습니다. "
            "가상환경에서 `python -m pip install PyMuPDF` 후 다시 실행해주세요."
        ) from exc

try:
    import easyocr
except ModuleNotFoundError:
    easyocr = None


DEFAULT_MODEL = "gpt-4.1-nano"
MAX_TEXT_CHARS = 12000


@st.cache_resource
def create_openai_client(api_key: str) -> OpenAI:
    # 같은 API 키로 만든 클라이언트는 앱 세션에서 재사용합니다.
    return OpenAI(api_key=api_key)


@st.cache_resource
def get_ocr_reader():
    if easyocr is None:
        return None
    # OCR 모델 로딩 비용이 커서 한 번만 생성해 캐시합니다.
    return easyocr.Reader(["ko", "en"], gpu=False)


def get_runtime_diagnostics() -> dict[str, object]:
    return {
        "python_executable": sys.executable,
        "fitz_available": fitz is not None,
        "easyocr_available": easyocr is not None,
    }


def extract_text_with_ocr(page) -> str:
    reader = get_ocr_reader()
    if reader is None:
        return ""

    # 텍스트가 없는 페이지는 이미지로 렌더링해 OCR로 다시 읽습니다.
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    image = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    result = reader.readtext(image, detail=0, paragraph=True)
    return "\n".join(text.strip() for text in result if text and text.strip())


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> dict[str, object]:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page_texts: list[str] = []
    ocr_used = False
    ocr_available = easyocr is not None

    try:
        for index, page in enumerate(doc, start=1):
            # 먼저 일반 텍스트 추출을 시도하고, 비어 있으면 OCR로 보완합니다.
            text = page.get_text("text").strip()
            source = "text"

            if not text:
                text = extract_text_with_ocr(page).strip()
                if text:
                    source = "ocr"
                    ocr_used = True

            if text:
                if source == "ocr":
                    page_texts.append(f"[Page {index}][OCR]\n{text}")
                else:
                    page_texts.append(f"[Page {index}]\n{text}")
            else:
                page_texts.append(f"[Page {index}]\n(No extractable text found)")
    finally:
        doc.close()

    # 미리보기에는 너무 긴 텍스트가 들어가지 않도록 길이를 제한합니다.
    full_text = "\n\n".join(page_texts).strip()
    preview_text = full_text[:MAX_TEXT_CHARS]

    return {
        "page_count": len(page_texts),
        "full_text": full_text,
        "preview_text": preview_text,
        "ocr_used": ocr_used,
        "ocr_available": ocr_available,
    }


def analyze_pdf_text(
    client: OpenAI,
    file_name: str,
    extracted_text: str,
    user_prompt: str | None = None,
    model: str = DEFAULT_MODEL,
) -> str:
    prompt = user_prompt or (
        "다음 PDF 내용을 읽고 한국어로 요약해줘. "
        "핵심 주제, 중요한 내용, 실무적으로 볼 포인트를 구분해서 정리해줘."
    )

    # Responses API에 요약 프롬프트와 추출 텍스트를 함께 전달합니다.
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "당신은 PDF 문서를 분석하는 도우미다. "
                            "과장 없이 핵심만 정확하게 정리하고, 표나 숫자가 보이면 중요 수치를 함께 언급한다."
                        ),
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": f"파일명: {file_name}"},
                    {"type": "input_text", "text": prompt},
                    {"type": "input_text", "text": extracted_text[:MAX_TEXT_CHARS]},
                ],
            },
        ],
        max_output_tokens=1000,
    )
    return response.output_text


def pdf_bytes_to_downloadable_file(pdf_bytes: bytes) -> BytesIO:
    buffer = BytesIO(pdf_bytes)
    buffer.seek(0)
    return buffer
