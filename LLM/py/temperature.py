from openai import OpenAI
from dotenv import load_dotenv
import truststore

# .env 파일에서 API 키 로드
load_dotenv(override=True)

# Windows가 가지고 있는 신뢰할 수 있는 인증서 저장소를
# Python SSL 통신에서도 사용하도록 연결합니다.
# 학교/회사 네트워크에서 자체 인증서를 쓰는 경우 도움이 됩니다.
truststore.inject_into_ssl()

# OpenAI SDK 클라이언트 초기화
client = OpenAI()

# AI 모델에서 Temperature(온도) 설정은 모델이 답변을 생성할 때 얼마나 창의적(무작위적)으로 답변할 것인가를 결정합니다.
# 0에서 2 사이의 값을 가지며(OpenAI 기준) 수치에 따라 모델의 성격이 완전히 달라집니다.
# 0에 가까울 때 : 항상 일관된 답변을 하지만, 표현이 단조로울 수 있습니다.
# 1 이상 : 창의적이고 의외의 답변이 나오지만, 엉뚱한 소리(환각)를 할 확률도 높아집니다.

def generate_response(temperature):
    # 최신 Responses API의 .create 메서드 사용
    response = client.responses.create(
        model="gpt-4.1-nano",
        
        # 질문
        input="국민한대 국가의 수도와 국기는 무엇입니까?",
        max_output_tokens=100,
        # 창의성 조절: 0(일관됨) ~ 2(매우 무작위)
        temperature=temperature,
    )
    
    print(f"현재 설정된 Temperature: {temperature}")
    print("-" * 50)
    
    # Responses API 응답 객체에서 텍스트 결과만 추출
    print(response.output_text)
    print("\n")

# Temperature 값에 따른 차이 테스트
# 0: 항상 같은 답변 (사실 관계 확인용)
generate_response(0)

# 1: 일반적인 균형 잡힌 답변
generate_response(1)

# 2: 창의적이거나 무의미한 답변(최대치)
generate_response(2)