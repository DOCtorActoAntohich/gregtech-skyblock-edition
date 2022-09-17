import hashlib
import pathlib
import sys

def print_hash(file_path: pathlib.Path):
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    with file_path.open(mode="rb") as file:
        hash = hashlib.sha256(file.read()).hexdigest()
    print(hash)


if __name__ == "__main__":
    print_hash(pathlib.Path(sys.argv[1]))
