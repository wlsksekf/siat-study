def outer():
    x = 10

    def inner():
        return x
    
    return inner

f = outer()
print(f())

def make_multiplier(n):

    def multiplier(x):
        return x * n
    
    return multiplier

times2 = make_multiplier(2)
times3 = make_multiplier(3)

print(times2(5))
print(times3(5))

def counter():
    count = 0
    
    def inc():
        nonlocal count
        count += 1
        return count
    
    return inc

c = counter()

print(c())
print(c())