class MyList:
    def __init__(self, items):
        self.items = items
        
    def __getitem__(self, index):
        return self.items[index]
    
lst = MyList([1, 2, 3])

print(lst[1])

print(lst[0:2])