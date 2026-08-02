from pathlib import Path

current_file_path = Path(__file__).resolve()
base_dir = current_file_path.parent

source_file = base_dir / "original" / "tree.jpg"

target_folder = base_dir / "target"
target_file = target_folder / "tree.jpg"

target_folder.mkdir(parents=True, exist_ok=True)

with open(source_file, "rb") as f_src:
    img_data = f_src.read(1024*1024)

with open(target_file, "wb") as f_dst:
    f_dst.write(img_data)
