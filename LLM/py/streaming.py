# 7.responses_streaming.py
from openai import OpenAI
from dotenv import load_dotenv
import truststore

truststore.inject_into_ssl()

load_dotenv()

client = OpenAI()

"""
1. 일반 모드(stream=False) : 서버가 전체 답변을 완성한 뒤 한 번에 응답을 보냄.
2. 스트리밍 모드(stream=True) : 서버가 답변을 생성하는 중간중간 아주 작은 조각(chunk) 단위로 요청한 프로그램에 보내줌.
"""

# AI 모델에 요청을 보냅니다.
response = client.responses.create(
    model="gpt-4.1-nano",                # 사용할 인공지능 모델 지정
    input="홍길동전을 두 문장으로 요약해줘.", # 모델에게 전달할 질문
    stream=True                          # 답변을 한 번에 다 만들 때까지 기다리지 않고 실시간으로 전송 받음
)


# 실시간 이벤트 처리 루프
# 서버에서 보내오는 이벤트(event)들을 하나씩 꺼내어 처리합니다.
# event 안에 chunk 데이터가 들어 있습니다.
for event in response:
    # 각 이벤트가 어떤 데이터를 담고 있는지 궁금하다면 아래 주석을 해제해 보세요.
    # print(event)

    # 1. 이벤트 객체 타입 확인
    print("\n" + "*" * 70)
    print("이벤트 객체 타입:", type(event))
    print("이벤트 타입:", event.type)

    # 2. 이벤트 객체 전체 출력
    # 이벤트 안에 어떤 데이터가 있는지 확인하기 위한 코드
    print("이벤트 전체 내용:")
    print(event)
    print()

    # 3. 텍스트 조각 이벤트
    if event.type == "response.output_text.delta":
        print("텍스트 조각(delta):", event.delta)

    # 4. 메시지 생성 완료 이벤트
    elif event.type == "response.output_item.done":
        print("메시지 생성 완료")
        print("완성된 메시지 내용:")
        print(event.item)

    # 5. 응답 완료 이벤트
    elif event.type == "response.completed":
        print("응답 스트림 종료")

    # 6. 기타 이벤트
    else:
        print("기타 이벤트 수신")

    # AI 모델에 요청을 보냅니다.
response = client.responses.create(
    model="gpt-4.1-nano",           # 사용할 인공지능 모델 지정
    input="홍길동전을 두 문장으로 요약해줘.", # 모델에게 전달할 질문
    stream=True                     # 답변을 한 번에 다 만들 때까지 기다리지 않고 실시간으로 전송받음
)

# 실시간 이벤트 처리 루프
# 서버에서 보내오는 이벤트(event)들을 하나씩 꺼내어 처리합니다.
# event 안에 chunk 데이터가 들어 있습니다.
for event in response:
    # 각 이벤트가 어떤 데이터를 담고 있는지 궁금하다면 아래 주석을 해제해 보세요.
    # print(event)

    # 특정 이벤트 타입 필터링
    # 'response.output_text.delta'는 텍스트 답변의 조각이 생성되었을 때 발생하는 이벤트입니다.
    if event.type == "response.output_text.delta":

        # event.delta에 실제 글자 조각이 들어있습니다.
        # end="|": 각 조각이 어느 단위로 끊겨서 오는지 확인하기 위해 구분선(|)을 넣었습니다.
        # flush=True: 출력 버퍼를 비워 터미널에 실시간으로 글자가 나타나게 합니다.
        print(event.delta, end="|", flush=True)