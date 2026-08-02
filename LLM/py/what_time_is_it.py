import json

from tool_time import get_current_time, tools
from openai import OpenAI
from dotenv import load_dotenv
from tool_time import tools

load_dotenv()
client = OpenAI()

# 모델에 질의하고 질의 결과를 반환하는 함수
# input_list 주고 받았던 대화 내용
def get_ai_response(input_list, tools=None):
    print("messages >>> ...")
    for i, msg in enumerate(input_list):
        print(f"{i}\t{msg}")
    print()

    response = client.responses.create(
        model="gpt-4.1-nano",
        instructions="당신은 친절한 비서입니다.",
        input=input_list,
        tools=tools,
        tool_choice="auto", # 질의 내용을 보고 LLM이 어떤 도구를 사용할 지 결정
        # parallel_tool_calls=False,
    )

    print("... >>> response.output")
    print(response.output)
    print()

    return response

# 대화 내용을 기록할 리스트
input_list = []

while True:
    user_input = input("사용자: ")
    if user_input.lower() == "exit":
        break

    input_list.append({"role": "user", "content": user_input})

    response = get_ai_response(input_list, tools=tools)
    input_list += response.output

    # 함수 호출이 있으면 함수 실행 후 결과를 질의에 추가
    is_function_call = False

    for item in response.output:
        if item.type == "function_call":
            is_function_call = True
            if item.name == "get_current_time":
                # 문자열을 내부 객체인 딕셔너리로 변환-> 값 추출이 용이
                arguments = json.loads(item.arguments) # arguments='{"timezone":"Asia/Seoul"}'

                function_response = get_current_time(timezone=arguments.get("timezone"))

                # 대화 내용을 담고 있는 input_list에 아래 정보들을 추가합니다.
                input_list.append(
                    {
                        "type": "function_call_output", # 정해진 값
                        "call_id": item.call_id,
                        "output": function_response,
                    }
                )

    # 함수 호출의 경우 함수 실행 결과와 함께 다시 모델에 질의
    if is_function_call:
        response = get_ai_response(input_list)
        input_list += response.output

    print(f"AI비서: {response.output_text}")

    print()