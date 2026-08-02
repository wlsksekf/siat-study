class A:
    def method_a(self):
        print("A 메서드")
        
class B:
    def method_b(self):
        print("B 메서드")

class C(A, B):
    def method_c(self):
        print("C 메서드")

c = C()
c.method_a()
c.method_b()
c.method_c()