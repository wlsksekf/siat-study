# chatbot_logic.py
from io import BytesIO

def prepare_audio(uploaded_file):
    """업로드된 파일을 OpenAI API가 요구하는 형태로 변환"""
    audio = BytesIO(uploaded_file.getvalue())
    audio.name = uploaded_file.name
    return audio


def whisper_process(client, uploaded_file, mode="transcribe"):
    """
    Whisper 처리 공통 함수
    mode = "transcribe" -> 전사 (Whisper 전사는 한국어/영어 등 원문 그대로 텍스트화)
    mode = "translate" -> 번역 (Whisper 번역 : Whisper -> 항상 영어로 번역됨)
    """

    audio_file = prepare_audio(uploaded_file)

    if mode == "transcribe":
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    else:  # translate
        result = client.audio.translations.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )

    return result