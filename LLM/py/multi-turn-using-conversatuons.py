from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# OpenAI Responses API의 “Conversation 기능”을 사용해서 멀티턴 대화가 가능한 예제입니다.
# 즉 AI가 이전 대화를 기억하면서 계속 대화하는 구조입니다.

# 서버 측에 새로운 대화 세션(대화방)을 생성합니다.
# 이전 방식처럼 대화 내역을 개발자가 직접 리스트로 보관할 필요 없이, 서버가 이 대화방 ID를 기준으로 기억합니다.
# 새로운 대화방 생성과 같은 의미입니다.
conversation = client.conversations.create()

while True: # 사용자가 종료하기 전까지 무한 반복 (채팅 루프)
    user_input = input("사용자: ")
    if user_input == "exit":
        break

    response = client.responses.create(
        model="gpt-4.1-nano",
        instructions="당신은 사용자를 도와주는 상담사입니다.",
        max_output_tokens=100,
        input=[
            {"role": "user", "content": user_input},
        ],
        conversation=conversation.id, # 위에서 생성한 OpenAI 대화방 ID의 고유 ID를 전달합니다.
    )

    print("상담사:", response.output_text)