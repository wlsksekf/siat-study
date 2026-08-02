class Person:
    def __init__(self, name, age):
        self.name = name
        self._nickname = "zㅣ존최강지민"
        self.__age = age

    def show_info(self):
        print(f"이름: {self.name}, 닉네임: {self._nickname}, 나이: {self.__age}")

    def get_age(self):
        return self.__age
    
    def set_age(self, age):
        if age > 0:
            self.__age = age
        else:
            print("잘못된 나이입니다.")

p1 = Person("지민", 25)
print(p1.name)
print(p1._nickname)

# print(p1.__age) - 오류
print(p1.get_age())

p1.set_age(30)
print(p1.get_age())

p1.set_age(-5)
print(p1.get_age())