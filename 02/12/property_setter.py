class Person:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        if len(value) > 1:
            self.__name = value
        else:
            print("이름이 너무 짧습니다.")