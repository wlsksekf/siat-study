print("="*50)
def display(*args, **kwargs):
    if not args:
        print()
        return

    sep_val = kwargs.get('sep', ' ')
    end_val = kwargs.get('end', '\n')
    print(*args, sep=sep_val, end=end_val)

display("2", "3", "4", sep="  ")
display(2026, 2, 1, sep="-")
display("사과", "배", "포도", sep=", ", end="...끝!\n")

display("나는", "파이썬", "입니다.")
display("python")
print("="*50)