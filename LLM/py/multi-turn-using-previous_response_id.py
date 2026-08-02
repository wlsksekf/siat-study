import time

from openai import OpenAI
from dotenv import load_dotenv
import truststore

truststore.inject_into_ssl()

load_dotenv()

client = OpenAI()

previous_id = None

turns = 10

for i in range(1, turns + 1):
    print(f"\n=== TURN {i} ===")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input="이전 대화를 기억하고 있다면, 지금은 몇 번째 턴인지 숫자만 말해.",
        previous_response_id=previous_id,
    )

    previous_id = response.id

    print("AI:", response.output_text)

    time.sleep(1)
