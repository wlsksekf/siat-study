users_json = [
    {"id": 1, "name": "Alice", "age": 25, "active":True},
    {"id": 2, "name": "Bob", "age": 17, "active":False},
    {"id": 3, "name": "Charlie", "age": 30, "active":True},
]

active_users = {
    user['name']: ('active' if user['active'] == True else 'inactive') 
    for user in users_json
    if user['age'] >= 20
    }
print(active_users)

users_20 = {
    user['name']: user['age'] 
    for user in users_json
    if user['age'] >= 20
    }
print(users_20)



