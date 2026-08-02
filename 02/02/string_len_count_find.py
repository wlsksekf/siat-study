text = "   Hello Python World   "

print("원본: ", text)

result = len(text)
print("문자열 길이: ", result)

result = text.count("a")
print("특정 문자 개수: ", result)

result = text.count("l")
print("특정 문자 개수: ", result)

result = text.find("h")
print("특정 문자 위치 찾기/없으면 -1: ", result)

result = text.find("ha")
print("특정 문자 위치 찾기/없으면 -1: ", result)

sample = "python"

print("시작 문자 확인: ", sample.startswith("py"))
print("끝 문자 확인: ", sample.endswith("on"))