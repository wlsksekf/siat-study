jumin = "010427-1234567"

# 1. 주민 번호 길이 구하기
print(len(jumin))

# 2. 하이픈(-) 위치 찾기
print(jumin.find("-"))

# 3. 하이픈 기준 분리
print(jumin.split("-")[0])
print(jumin.split("-")[1])

# 4. 하이픈 제거
print(jumin.replace("-", ""))

# 5. 앞자리 6글자 추출
print(jumin[:6])

# 6. 뒷자리 7글자 추출
print(jumin[7:])

# 7. 성별 코드 추출
print(jumin[7])

# 8. 문자열이 숫자로만 구성되어 있는지
print(jumin.isdigit())

# 9. 하이픈 제거 후 숫자 여부 확인
print(jumin.replace("-", "").isdigit())

# 10. 특정 문자 포함 여부 (in)
print("-" in jumin)

# 11. 시작 문자열 확인 ("80"으로 시작하는지)
print(jumin.startswith("80"))

# 12. 끝 문자열 확인 ("4567"로 끝나는지)
print(jumin.endswith("4567"))

# 13. 주민번호 뒷자리 중 마지막 6개 별로 바꾸기
print(jumin[:8] + "*" * 6)

# 14. 14번 * 찍기
print("*" * 14)

# 15. 특정 문자 개수 세기("-")
print(jumin.count("-"))

# 16. 생년월일 추출(80-11-12)
print(jumin[:2] + "-" + jumin[2:4] + "-" + jumin[4:6])