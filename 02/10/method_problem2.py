class Book:
    library = "시립 도서관"  # 클래스 변수

    def __init__(self, title, author):
        self.title = title      # 인스턴스 변수
        self.author = author

    # 인스턴스 메서드
    def info(self):
        print(f"책 제목: {self.title}, 저자: {self.author}")

    # 클래스 메서드
    @classmethod
    def library_info(cls):
        print(f"이 책은 {cls.library}에 있습니다.")

    # 정적 메서드
    @staticmethod
    def welcome():
        print("도서관에 오신 것을 환영합니다!")

# 사용 예시
s1 = Book("파이썬 프로그래밍", "홍길동")
s1.info()        # 인스턴스 메서드 호출

Book.library_info() # 클래스 메서드 호출
Book.welcome()     # 정적 메서드 호출