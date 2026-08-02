from tool_time_stock import get_current_time, tools, get_yf_stock_info
from openai import OpenAI
from dotenv import load_dotenv
import json

import truststore


truststore.inject_into_ssl()

load_dotenv()
client = OpenAI()


def get_ai_response(input_list, tools=None):
    print("messages >>> ...")
    for i, msg in enumerate(input_list):
        print(f"{i}\t{msg}")
    print()

    response = client.responses.create(
        model="gpt-4.1-nano",
        instructions=(
            "당신은 친절한 주식 비서입니다. "
            "주가를 물어보면 관련 주식 도구를 사용하고, 여러 종목이면 빠짐없이 모두 조회하세요. "
            "시간은 사용자가 직접 요청한 경우에만 조회하세요."
        ),
        input=input_list,
        tools=tools,
        tool_choice="auto",
    )

    print("... >>> response.output")
    print(response.output)
    print()

    return response


def append_function_outputs(response, input_list):
    function_call_count = 0

    for item in response.output:
        if item.type != "function_call":
            continue

        function_call_count += 1
        arguments = json.loads(item.arguments)

        if item.name == "get_current_time":
            function_response = get_current_time(
                timezone=arguments.get("timezone", "Asia/Seoul")
            )
        elif item.name == "get_yf_stock_info":
            function_response = get_yf_stock_info(ticker=arguments.get("ticker", ""))
        else:
            function_response = f"지원하지 않는 함수입니다: {item.name}"

        input_list.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": function_response,
            }
        )

    return function_call_count


input_list = []

while True:
    user_input = input("사용자: ").strip()
    if user_input.lower() == "exit":
        break

    if not user_input:
        continue

    input_list.append({"role": "user", "content": user_input})

    response = get_ai_response(input_list, tools=tools)
    input_list += response.output

    while append_function_outputs(response, input_list):
        response = get_ai_response(input_list, tools=tools)
        input_list += response.output

    print(f"AI비서: {response.output_text}")
    print()
