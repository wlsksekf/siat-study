f = open("example.txt", "r", encoding="utf-8")
content = f.read()
f.close()

print(content)

f = open("example.txt", "r", encoding="utf-8")
for line in f:
    print(line.strip())
f.close()
