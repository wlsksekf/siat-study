from pathlib import Path

print(__file__)
print(type(__file__))

current_file_path = Path(__file__).resolve()
print(f"현재 파일의 전체 경로: {current_file_path}")

base_dir = current_file_path.parent
print(f"1. 현재 파일이 위치한 폴더: {base_dir}")
print(f"2. 상위의 상위 폴더: {base_dir.parent}")

print(f"3. 파일명 전체: {current_file_path.name}")
print(f"4. 파일명만(확장자 제외): {current_file_path.stem}")
print(f"5. 확장자만: {current_file_path.suffix}")

data_folder = base_dir / "data" / "write"
print(f"6. 합쳐진 경로: {data_folder}")

if not data_folder.exists():
    data_folder.mkdir(parents=True)
    print(f"7. {data_folder} 폴더를 생성")
else:
    print(f"7. 이미 폴더가 존재하므로 생성 x")

print(f"8. 현재 폴더 내 파이썬 파일 목록:")

for py_file in base_dir.glob("*.py"):
    print(f"   - {py_file.name}")