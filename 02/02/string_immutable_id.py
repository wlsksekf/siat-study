sample = "abced"

old_id = id(sample)
print(f"처음 주소: {old_id}")

sample = "f" + sample[1:]

new_id = id(sample)
print(f"새 주소: {new_id}")

print(f"주소 일치 여부: {old_id == new_id}")