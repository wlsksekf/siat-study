# https://developers.openai.com/api/reference/resources/responses/methods/create

# [참고] OpenAI SDK란?
# 개발자가 API 서버와 직접 통신(HTTP 통신)하는 복잡한 과정을 생략하고,
# 파이썬 함수 호출만으로 AI 기능을 사용할 수 있게 해주는 '공식 도구 모음'입니다.

# 1. 필수 라이브러리 임포트
# OpenAI 서비스와 통신하기 위한 메인 클라이언트 클래스
from openai import OpenAI

# .env 파일에 저장된 환경 변수를 읽어오기 위한 라이브러리
from dotenv import load_dotenv

import truststore

# 2. 환경 변수 로드
# 시스템 환경 변수에 이미 OPENAI_API_KEY가 있더라도,
# .env 파일에 명시된 값을 우선적으로 덮어쓰기(override)하여 설정합니다.
load_dotenv(override=True)

# Windows가 가지고 있는 신뢰할 수 있는 인증서 저장소를
# Python SSL 통신에서도 사용하도록 연결합니다.
# 학교/회사 네트워크에서 자체 인증서를 쓰는 경우 도움이 됩니다.
truststore.inject_into_ssl()

# 3. OpenAI 클라이언트 객체 초기화
# 별도의 인자를 주지 않으면 환경 변수의 'OPENAI_API_KEY'를 자동으로 찾아 사용합니다.
client = OpenAI()

# 4. Responses API를 통한 메시지 생성 요청
# 모델에게 입력값(input)을 전달하고 그 결과를 받아옵니다.
response = client.responses.create(
    model="gpt-4.1-nano", # 사용할 인공지능 모델의 ID (예: gpt-4o, gpt-4-turbo 등)
    input="OpenAI Responses API에 대해 한 문장으로 설명해줘" # 모델에게 던지는 질문/명령
)

# 5. 결과 출력 및 파싱(Parsing)
# API로부터 받은 전체 응답 객체(메타데이터 포함)를 출력합니다.
print("전체 응답:", response)

# 응답 객체 내에서 실제 생성된 텍스트 내용만 추출하여 출력합니다.
print("응답:", response.output_text)