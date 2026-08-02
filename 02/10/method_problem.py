class Student:
    school_name = "파이썬 고등학교"  # 클래스 변수

    def __init__(self, name, age):
        self.name = name      # 인스턴스 변수
        self.age = age

    # 인스턴스 메서드
    def introduce(self):
        print(f"안녕하세요, 제 이름은 {self.name}이고 {self.age}살입니다.")

    # 클래스 메서드
    @classmethod
    def school_info(cls):
        print(f"저희 학교는 {cls.school_name}입니다.")

    # 정적 메서드
    @staticmethod
    def welcome():
        print("학생 여러분, 환영합니다!")

# 사용 예시
s1 = Student("홍길동", 18)
s1.introduce()        # 인스턴스 메서드 호출

Student.school_info() # 클래스 메서드 호출
Student.welcome()     # 정적 메서드 호출