count = 1
while count <= 5:
    print("현재 숫자:", count)
    count += 1

while True:
    text = input("종료하려면 q를 입력하세요: ")
    print("입력 데이터: ", text)
    if text == "q":
        print("프로그램 종료")
        break

