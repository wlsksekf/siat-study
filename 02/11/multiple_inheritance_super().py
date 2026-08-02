class Base:
    def hello(self):
        pass

class A(Base):
    def hello(self):
        print("A")
        super().hello()

class B(Base):
    def hello(self):
        print("B")
        super().hello()

class C(A, B):
    def hello(self):
        print("C")
        super().hello()

print(C.mro())
c = C()
c.hello()