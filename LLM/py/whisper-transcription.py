# OpenAI API를 사용하기 위한 공식 Python SDK에서 OpenAI 클래스를 가져옵니다.
from openai import OpenAI

# .env 파일에 저장된 환경 변수를 불러오기 위한 라이브러리입니다.
from dotenv import load_dotenv

# 파일 경로를 객체 형태로 다루기 위한 pathlib 모듈입니다.
from pathlib import Path

import truststore

truststore.inject_into_ssl()

# .env 파일에 저장된 환경 변수를 현재 Python 실행 환경에 로드합니다.
# 예) OPENAI_API_KEY
load_dotenv()

# OpenAI API와 통신하기 위한 클라이언트 객체를 생성합니다.
client = OpenAI()

# 음성 파일의 경로를 Path 객체로 생성합니다.
# Path를 사용하면 운영체제에 상관없이 동일한 방식으로 경로를 처리할 수 있습니다.
audio_file_path = Path("./data/성범죄 예방안내.mp3")

# 파일이 실제로 존재하는지 확인합니다.
# Path 객체의 exists() 메서드를 사용합니다.
if not audio_file_path.exists():
    raise FileNotFoundError(f"[ERROR] File not found: {audio_file_path}")

# Path 객체의 open() 메서드를 사용하여 파일을 읽기 모드로 엽니다.
# "rb"는 binary read를 의미하며, 오디오 파일은 반드시 바이너리 모드로 읽어야 합니다.

with audio_file_path.open("rb") as audio_file:

    # Whisper 전사 호출
    # Whisper는 "한 파일당 언어 하나"만 안정적으로 인식하는 특성이 있음
    # 한국어만 전사
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text",
        language="ko"
    )

    print("전사 결과[한국어]", transcription)

    # 영어만 전사
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text",
        language="en"
    )

    print("전사 결과[영어]:", transcription)