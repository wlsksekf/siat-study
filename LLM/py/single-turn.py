# 10. single-turn.py
from openai import OpenAI
from dotenv import load_dotenv
import truststore

truststore.inject_into_ssl()

load_dotenv()

client = OpenAI()

while True:
    user_input = input("사용자: ")
    if user_input == "exit":
        break
    
    response = client.responses.create(
        model="gpt-4.1-nano",
        instructions="당신은 사용자를 도와주는 상담사입니다.",
        input=[
            {"role": "user", "content": user_input},
        ],
        max_output_tokens=100,
    )

    print("상담사:", response.output_text)
    print()