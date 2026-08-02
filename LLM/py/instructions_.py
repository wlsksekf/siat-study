from openai import OpenAI
from dotenv import load_dotenv
import truststore

truststore.inject_into_ssl()

# .env 파일에서 API 키를 로드하여 환경 변수로 설정합니다.
load_dotenv()

# OpenAI 클라이언트 인스턴스를 생성합니다.
client = OpenAI()

# Responses API를 통한 모델 호출
response = client.responses.create(
    model="gpt-4.1-nano",
    
    # instructions: 모든 대화에 공통으로 적용됩니다.
    instructions="You are a helpful assistant.",
    
    # input: 실제 모델에게 전달할 사용자의 질문이나 요청입니다.
    input="홍길동전을 한 문장으로 요약해줘.",
)

# 전체 응답 객체 출력
# API가 반환하는 전체 데이터 구조(ID, 모델명, 생성 시간, 상세 결과 등)를 확인할 수 있습니다.
print(response)

# SDK에서 제공하는 속성으로, 복잡한 계층 구조를 거치지 않고 최종 텍스트만 바로 가져옵니다.
print(response.output_text)