# 8.role_prompting.py
from openai import OpenAI
from dotenv import load_dotenv
import truststore

truststore.inject_into_ssl()

load_dotenv()

client = OpenAI()

def who_is_the_most_beautiful(role: str):
    response = client.responses.create(
        model="gpt-4.1-nano",
        temperature=1.2, # 창의적 답변
        instructions=f"당신은 {role} 입니다. 사용자 질의에 한 문장으로 답변해 주세요.",
        input="세상에서 누가 제일 아름다워요?",
    )

    print(f"{role} >>> ")
    print(response.output_text)
    print()

who_is_the_most_beautiful("백설공주 이야기 속의 마법 거울")
who_is_the_most_beautiful("영화 베트맨 속의 조커")
who_is_the_most_beautiful("어린이집에 다니는 여자아이")
who_is_the_most_beautiful("사회생활 잘하는 김 대리")
who_is_the_most_beautiful("표독하고 심술궃은 김진환")