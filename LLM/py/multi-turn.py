# 10. single-turn.py
from openai import OpenAI
from dotenv import load_dotenv
import truststore

truststore.inject_into_ssl()

load_dotenv()

client = OpenAI()

messages = []

while True:
    user_input = input("사용자: ")
    if user_input == "exit":
        break

    messages.append({"role": "user", "content": user_input})

    response = client.responses.create(
        model="gpt-4.1-nano",
        instructions="당신은 사용자를 도와주는 상담사입니다.",
        input=messages,
        max_output_tokens=100,
    )

    messages.append({"role": "assistant", "content": response.output_text})

    print("상담사:", response.output_text)
    print()

# 소중한 사람, 잊고 싶지 않은 사람, 잊어서는 안 되는 사람...! 누구야...? 이름은...!