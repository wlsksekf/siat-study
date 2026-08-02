input_num = int(input("숫자를 입력하세요: "))

if input_num % 3 == 0 and input_num % 5 == 0:
    print("FizzBuzz")
elif input_num % 3 == 0:
    print("Fizz")
elif input_num % 5 == 0:
    print("Buzz")
else:
    print(input_num)

result = (
    "FizzBuzz" if input_num % 15 == 0 else
    "Fizz" if input_num % 15 == 0 else
    "Buzz" if input_num % 15 == 0 else
    input_num
)

result = "FizzBuzz" if input_num % 3 == 0 and input_num % 5 == 0 else "Fizz" if input_num % 3 == 0 else "Buzz" if input_num % 5 == 0 else input_num
print(result)
