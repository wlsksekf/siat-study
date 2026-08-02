def calc(*args, **kwargs):
    if kwargs:
        a = kwargs.get('a', 0)
        b = kwargs.get('b', 0)
        return a + b
    
    if len(args) >= 2:
        num1 = args[0]
        num2 = args[1]
        
        if len(args) < 3:
            return num1 + num2
        
        op = args[2]
        if op == "-": return num1 - num2
        elif op == "*": return num1 * num2
        elif op == "/": return num1 / num2
    
    return "계산 불가"

print(calc(10, 5))
print(calc(10, 5, "-"))
print(calc(10, 5, "*"))
print(calc(10, 5, "/"))
print(calc(b=20, a=7))