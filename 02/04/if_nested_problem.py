user_id = "Kim"
user_pw = "1234"

input_id = input("아이디 입력: ")
input_pw = input("비번 입력: ")

if user_id == input_id:
    if user_pw == input_pw:
        print("로그인 성공!")    
    else:
        print("비밀번호 틀림")
else:
    print("아이디 존재 x")

if user_id != input_id:
    print("아이디 존재 x")
elif user_pw != input_pw:
    print("비밀번호 틀림")
else:
    print("로그인 성공!")