# 3. 책 개수 세기
book_list = ["파이썬 입문", "자바 스크립트", "HTML/CSS", "파이썬 입문"]

books = sorted(list(set(book_list)))
# set으로 중복을 없앤 뒤 sorted로 재정렬 해주고 list 로 만들기
print(books) # ['HTML/CSS', '자바 스크립트', '파이썬 입문']

book_count = [  # 해당 부분은 성적표 작성 방법과 Count를 응용했습니다.
    (books[0], book_list.count(books[0])),
    (books[1], book_list.count(books[1])),
    (books[2], book_list.count(books[2]))
] 
# 책의 1번째를 지정한 뒤 책의 Count를 확인하기
# 나머지 2번째 3번째도 동일

book_result = dict(book_count)
# list로 만들었던 books를 딕셔너리로 변경

print(book_result) # {'HTML/CSS': 1, '자바 스크립트': 1, '파이썬 입문': 2}
# 딕셔너리로 바꾼 책의 결과값을 제출

# 힌트
# 리스트 -> 딕셔너리
# lst = [("a", 1), ("b", 2)]
# d = dict(lst)
# print(d)        # {'a': 1, 'b': 2}

book_list = ["파이썬 입문", "자바 스크립트", "HTML/CSS", "파이썬 입문"]

set1 = set(book_list)
unique_list = sorted(set1)

b1 = book_list.count(unique_list[0])
b2 = book_list.count(unique_list[1])
b3 = book_list.count(unique_list[2])

t = ((unique_list[0], b1), (unique_list[1], b2), (unique_list[2], b3))
di = dict(t)

print(di)