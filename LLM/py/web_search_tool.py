# web_search_tool.py
from dotenv import load_dotenv
from openai import OpenAI
import json

import truststore

truststore.inject_into_ssl()

load_dotenv()

client = OpenAI()

# 모델은 필요할 때 자동으로 웹 검색을 호출하도록 설정합니다.
def get_web_searched_response(prompt: str):
    print(f"질문: {prompt}\n")

    try:
        response = client.responses.create(
            model="gpt-4o",
            input=prompt,
            tools=[
                {
                    "type": "web_search"  # 내장 도구
                }
            ],
        )
        print("[응답] ", response)

        citations = []  # 조회한 사이트 정보
        question = ""   # 질문을 어떤 검색어로 검색했는지 확인할 수 있어요
        answer = ""     # 검색 결과
        for item in response.output:
            if item.type == 'web_search_call':
                question = item.action.query            # item.action.query : 모델이 자동 생성한 검색어
            elif item.type == 'message':                # message : 모델이 사용자에게 돌려주는 실제 응답 메시지
                citations = item.content[0].annotations  # 웹 검색 결과에서 인용한 출처 목록
                answer = item.content[0].text           # text : 모델의 최종 응답 텍스트

        return question, answer, citations  # 검색어(question), 모델 최종 응답(answer), 출처 정보(citations)
    
    except Exception as e:
        print(f"API 요청 중 오류 발생: {e}")
        return f"오류 발생: {e}", "", []

query = "2026년 3월에 출시된 가성비좋은 스마트폰 3가지를 알려줘 100자 이내로"
question, answer, citations = get_web_searched_response(query)

print("검색어 >>> ")
print(question)
print()

print("모델 응답 >>> ")
print(answer)
print()

print("검색 결과 >>> ")
for citation in citations:
    print(f"title={citation.title}")
    print(f"url=({citation.url})")
    print()
