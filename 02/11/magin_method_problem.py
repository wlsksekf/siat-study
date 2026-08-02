# # 1. 여러 상품 객체 생성
# p1 = Product("무선 마우스", 25000, "로지텍")
# p2 = Product("기계식 키보드", 120000, "레오폴드")
# p3 = Product("4K 모니터", 450000, "LG")

# # 2. 단일 객체 출력 (사용자에게 보여주는 화면)
# print("--- 오늘의 추천 상품 ---")
# print(p1)  # [로지텍] 무선 마우스 - 25,000원
# print(p2)  # [레오폴드] 기계식 키보드 - 120,000원

# # 3. 리스트에 담아 관리 (디버깅 화면)
# cart = [p1, p2, p3]
# print("\n--- 장바구니 내부 데이터 (REPR) ---")
# print(repr(cart)) # [Product(name='무선 마우스', price=25000), Product(name='기계식 키보드', price=120000), Product(name='4K 모니터', price=450000)]

# * 위 조건을 만족하는 클래스 Product를 만들어 주세요
# 생성자에서 사용할 변수들 입니다.
# 1. 상품 이름은 name 변수 사용
# 2. 가격은 price 변수 사용
# 3. 회사명은 brand 변수 사용

class Product:
    def __init__(self, name, price, brand):
        self.name = name
        self.price = price
        self.brand = brand
    
    def __str__(self):
        return f"[{self.brand}] {self.name} - {self.price}원"
    
    def __repr__(self):
        return f"[Product(name={self.name}, price={self.price})]"

p1 = Product("무선 마우스", 25000, "로지텍")
p2 = Product("기계식 키보드", 120000, "레오폴드")
p3 = Product("4K 모니터", 450000, "LG")

print("--- 오늘의 추천 상품 ---")
print(p1)
print(p2)

cart = [p1, p2, p3]
print("\n--- 장바구니 내부 데이터 (REPR) ---")
print(repr(cart))