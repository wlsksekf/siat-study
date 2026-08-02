str1 = "python"
str2 = "nohtyp"

print(len(str1))
print(len(str2))

print(str1[::-1])
print(str2[::-1])

result = (len(str1) == len(str2)) and (str1[::-1] == str2)
print(result)
