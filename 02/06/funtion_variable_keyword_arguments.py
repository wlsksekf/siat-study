def show_profile(**kwargs):
    print(type(kwargs))
    print(kwargs)

show_profile(name="이철수", age=20)
show_profile(name="김영희", age=25, city="서울")

def order(*args, **kwargs):
    print(f"메뉴: {args[0]}")
    print(f"옵션: {args[1:]}")
    print(f"정보: {kwargs}")

order("아메리카노", "얼음적게", "샷추가", size="Tall", takeout=True)
