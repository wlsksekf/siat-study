from pathlib import Path

current_file_path = Path(__file__).resolve()

base_dir = current_file_path.parent

data_folder = base_dir / "data" / "write"

if not data_folder.exists():
    data_folder.mkdir(parents=True)
    print(f"7. {data_folder} 폴더를 생성")
else:
    print(f"7. 이미 폴더가 존재하므로 생성 x")

target_file = data_folder / "example.txt"

f = open(target_file, "w", encoding="utf-8")
f.write("Hello, Python!\n")
f.write("파일 입출력 예제입니다.\n")
f.close()