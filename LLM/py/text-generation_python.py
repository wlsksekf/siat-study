import os
from pathlib import Path

import requests
import truststore
from dotenv import load_dotenv

# 1. .env 파일에 있는 환경변수를 현재 실행 환경으로 불러옵니다.
# override=True 이므로 이미 같은 이름의 값이 있어도 .env 값으로 덮어씁니다.
load_dotenv(override=True)

# 2. Windows가 가지고 있는 신뢰할 수 있는 인증서 저장소를
# Python SSL 통신에서도 사용하도록 연결합니다.
# 학교/회사 네트워크에서 자체 인증서를 쓰는 경우 도움이 됩니다.
truststore.inject_into_ssl()

# 3. OpenAI API 키를 환경변수에서 읽어옵니다.
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY is not set.")

# 4. OpenAI Responses API 주소
url = "https://api.openai.com/v1/responses"

# 5. 요청 헤더 설정
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

# 6. 요청 본문 데이터
data = {
    "model": "gpt-4.1-nano",
    "input": "OpenAI Responses API를 한 문장으로 설명해줘.",
}

# 7. 네트워크 프록시가 자체 루트 인증서를 사용하는 경우를 대비한 설정입니다.
# OPENAI_CA_BUNDLE 환경변수에 PEM 또는 CRT 파일 경로를 넣으면
# requests가 그 인증서를 신뢰하도록 할 수 있습니다.
verify = os.getenv("OPENAI_CA_BUNDLE")
if verify:
    verify_path = Path(verify)
    if not verify_path.exists():
        raise FileNotFoundError(
            f"OPENAI_CA_BUNDLE file not found: {verify_path}"
        )

try:
    # 8. POST 요청 전송
    # verify 값이 있으면 해당 인증서 파일로 SSL 검증을 수행합니다.
    # 없으면 기본 검증 방식을 그대로 사용합니다.
    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=30,
        verify=verify if verify else True,
    )

    # 9. HTTP 상태 코드가 4xx/5xx면 예외를 발생시킵니다.
    response.raise_for_status()
except requests.exceptions.SSLError as exc:
    # 10. SSL 인증서 검증 실패 시, 원인과 해결 방향을 안내합니다.
    raise SystemExit(
        "SSL certificate verification failed.\n"
        "If your school/company network uses a proxy certificate, export that "
        "root certificate as a PEM/CRT file and set OPENAI_CA_BUNDLE to it.\n"
        "Example: $env:OPENAI_CA_BUNDLE='C:\\path\\company-root.pem'"
    ) from exc
except requests.exceptions.RequestException as exc:
    # 11. 그 밖의 요청 오류 처리
    raise SystemExit(f"Request failed: {exc}") from exc

# 12. 응답을 JSON으로 변환해서 출력합니다.
completion = response.json()
print("전체 응답 데이터 구조:", completion)
print()
print("응답 내용:", completion["output"])