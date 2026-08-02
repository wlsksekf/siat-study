# OpenAI API를 사용하기 위한 공식 라이브러리 불러오기
from openai import OpenAI

# .env 파일에 저장된 환경 변수(API 키 등)를 불러오기 위한 라이브러리
from dotenv import load_dotenv

import truststore

truststore.inject_into_ssl()

# .env 파일에 있는 환경 변수들을 현재 프로그램에서 사용할 수 있도록 로드
load_dotenv()

# OpenAI 클라이언트 객체 생성
# 이후 API 호출은 이 객체를 통해 수행됩니다.
client = OpenAI()

# Few-shot 예제를 정의하는 리스트
# AI에게 보여줄 "질문 -> 답변" 패턴을 미리 작성합니다.
# client.responses 구조에서
# role은 "이 메시지를 말하는 주체가 누구인가?"를 정의하는 속성입니다.
EXAMPLE_SHOTS = [
    
    # 사용자 질문 예제
    {"role": "user", "content": "참새"},
    
    # AI가 어떻게 답해야 하는지 예시 답변
    {"role": "assistant", "content": "짹짹!!!"}, # AI에게 원하는 답변 패턴
    
    # 두 번째 예제
    {"role": "user", "content": "병아리"},
    {"role": "assistant", "content": "삐약삐약!!!"},
    
    # 세 번째 예제
    {"role": "user", "content": "뱀"},
    {"role": "assistant", "content": "(조용)"},
]

# 실제 모델에게 전달할 입력(input)을 생성
# 기존 예제(EXAMPLE_SHOTS)에 새로운 질문을 추가합니다.
input = EXAMPLE_SHOTS + [
    {"role": "user", "content": "강아지"}
]

# OpenAI Responses API 호출
response = client.responses.create(
    
    # 사용할 모델 지정
    model="gpt-4.1-nano",
    
    # AI 답변 길이를 최대 100 토큰으로 제한
    max_output_tokens=100,
    
    # AI의 역할과 답변 규칙 설정
    # 여기서는 "어린이집에 다니는 7살 아이" 역할을 하도록 설정
    instructions="당신은 어린이집을 다니는 7살 아이입니다. 모든 질문에 대해 한 문장으로 답변해 주세요.",
    
    # 모델에게 전달할 실제 입력
    # 위에서 만든 few-shot 예제 + 새로운 질문
    input=input,
)

# 응답 결과에서 텍스트만 추출
# 모델이 생성한 답변 문자열이 들어 있습니다.
output_text = response.output_text

# 최종 결과 출력
# few-shot 패턴을 따라 "강아지 -> 멍멍!!!" 같은 답변이 출력됩니다.
print(output_text)