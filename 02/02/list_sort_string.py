fruits = ["Apple", "pineapple", "banana", "cherry"]

fruits.sort()
print(fruits)

fruits.reverse()
print("최종 리스트: ", fruits)

errors = [1, "1", 2]
# errors.sort()

nums = [4, 1, 3, 2]
nums.sort()
print(nums)

nums = [4, 1, 3, 2]
nums.sort(reverse=True)
print(nums)

words = ["banana", "apple", "cherry"]
words.sort()
print(words)

words = ["kiwi" "banana", "apple", "fig"]
words.sort(key=len)
print(words)

words = ["kiwi" "banana", "apple", "fig"]
words.sort(key=len, reverse=True)
print(words)

names = ["kiwi", "banana", "apple", "cherry", "Apple"]
names.sort()
print(names)

names = ["kiwi", "banana", "apple", "cherry", "Apple"]
names.sort(key=str.lower)
print(names)