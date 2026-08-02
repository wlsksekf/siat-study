class A:
    pass

a = A()

# len(a) # TypeError: object of type 'A' has no len()

class Test:
    def __len__(self):
        return 5
    
t = Test()
print(len(t))

class MyList:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)
    
lst = MyList([1, 2, 3])
print(len(lst))

lst = MyList((1, 2, 3, 4, 5))
print(len(lst))