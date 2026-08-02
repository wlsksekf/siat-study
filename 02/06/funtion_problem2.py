print("="*50)
def display(*args, end="\n", **kwargs):
    if not args:
        print()
        return

    print(*args, **kwargs, end=end)

display("안녕하세요")
display("안녕하세요", "파이썬")
display("안녕하세요", "파이썬", "공부 중입니다.")

display("사과", "배", "포도", end=" *** ")
display("과일 목록 끝") 
display()
print("="*50)