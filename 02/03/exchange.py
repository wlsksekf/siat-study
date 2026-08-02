lst = [1, 2, 3]
t = tuple(lst)
print(t)

t2 = (4, 5, 6)
lst2 = list(t2)
print(lst2)

lst = [("a", 1), ("b", 2)]
d = dict(lst)
print(d)

t = (("x", 10), ("y", 20))
d2 = dict(t)
print(d2)

d = {"a":1, "b":2}

keys_list = list(d.keys())
keys_tuple = tuple(d.keys())
print(keys_list)
print(keys_tuple)

values_list = list(d.values())
values_tuple = tuple(d.values())
print(values_list)
print(values_tuple)

items_list = list(d.items())
items_tuple = tuple(d.items())
print(items_list)
print(items_tuple)