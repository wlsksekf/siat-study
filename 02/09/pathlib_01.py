from pathlib import Path

def info(p):
    print(p)
    print(type(p))
    print(p.resolve())
    print("*"*50)

p = Path(".")
info(p)

p = Path("./")
info(p)

p = Path("../a/b")
info(p)