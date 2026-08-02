visited_today = ["김철수", "이영희", "김철수", "박민수", "이영희"]

print(f"{len(set(visited_today))}명, 고객 명단: {sorted(list(set(visited_today)))}")

menu = {'아메리카노': 4100, '라떼': 4600, '에이드':5000}
print(f"아메리카노 가격: {menu.get('아메리카노')}")

menu.update({'케이크': 6000})

print(f"전체 메뉴: {menu}")
