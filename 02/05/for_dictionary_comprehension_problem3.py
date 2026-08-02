logs_json = [
    {"url": "/login", "status": 200},
    {"url": "/board", "status": 404},
    {"url": "/admin", "status": 500},
]

result = {
    url["url"]: ("백엔드 개발자놈 잘못임" if url["status"] >= 500 else "프론트 개발자놈 잘못임") 
    for url in logs_json
    if url["status"] >= 400
}

print(result)


