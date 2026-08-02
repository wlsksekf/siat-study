# 1. Person 클래스를 만듭니다.
#     - 생성자에서 name 매개변수를 받아 인스턴스 변수 name에 저장하세요.
#     - greet() 메서드를 정의하세요.      
#     - greet()는 "안녕하세요, 저는 {name}입니다." 를 출력하도록 하세요.
        
# 2. Student 클래스를 만들고 Person 클래스를 상속받습니다.
#     - study() 메서드를 정의하세요.
#     - study()는 "{name}이(가) 공부합니다." 를 출력하도록 하세요.

# 3. Teacher 클래스를 만들고 Person 클래스를 상속받습니다.
#     - teach() 메서드를 정의하세요.
#     - teach()는 "{name} 선생님이 수업을 합니다." 를 출력하도록 하세요.

# 4. 다음과 같이 객체를 생성하고 메서드를 호출했을 때 아래의 출력 결과가 나오도록 하세요.
#     - Student("철수")
#     - Teacher("민수")

# 5. 출력결과 입니다.
# 안녕하세요, 저는 철수입니다.
# 철수이(가) 공부합니다.
# 안녕하세요, 저는 민수입니다.
# 민수 선생님이 수업을 합니다.

class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"안녕하세요, 저는 {self.name}입니다.")

class Student(Person):
    def study(self):
        print(f"{self.name}이(가) 공부합니다.")

class Teacher(Person):
    def teach(self):
        print(f"{self.name} 선생님이 수업을 합니다.")

student = Student("철수")
teacher = Teacher("민수")

student.greet()
student.study()

teacher.greet()
teacher.teach()