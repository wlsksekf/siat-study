class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return self.title == other.title and self.author == other.author

    def __hash__(self):
        return hash((self.title, self.author))

    def __repr__(self):
        return f"Book(title='{self.title}')"

b1 = Book("파이썬 입문", "홍길동")
b2 = Book("파이썬 입문", "홍길동")
b3 = b1

print(f"id(b1): {id(b1)}")
print(f"id(b2): {id(b2)}")
print(f"b1 해시: {hash(b1)}")
print(f"b2 해시: {hash(b2)}")
print(f"해시값이 같은가?: {hash(b1) == hash(b2)}")