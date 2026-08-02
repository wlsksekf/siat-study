text = "   Hello Python World   "

print("원본: ", text)

result = len(text)
print("문자열 길이: ", result)

result = text.strip()
print("strip: ", result)

result = text.lstrip()
print("lsstrip: ", result)

result = text.rstrip()
print("rsstrip: ", result)

words = text.split()
print("split: ", words)

data = "python,java,c++,html"
result = data.split(",")
print(result)

print("join: ", "-".join(words))