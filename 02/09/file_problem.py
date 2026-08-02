from pathlib import Path

current_file_path = Path(__file__).resolve()

base_dir = current_file_path.parent

data_folder = base_dir / "original"

if not data_folder.exists():
    data_folder.mkdir(parents=True)
    print(f"7. {data_folder} 폴더를 생성")
else:
    print(f"")

target_file = data_folder / "gugudan.txt"

with open(target_file, "w", encoding="utf-8") as f:
    f.write("=== 파이썬 구구단 프로그램 ===\n\n")
    for i in range(2, 10):
        f.write(f"--- {i}단 ---\n")
        for dan in range(1, 10):
            f.write(f"{i} x {dan} = {i*dan}\n")
        f.write("\n")
    
with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

print(content)