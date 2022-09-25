import argparse
from pathlib import Path
import pathlib
import shutil

from build.paths import PathTo


def _delete_item(path: pathlib.Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
        return
    path.unlink()

def remove(path: pathlib.Path) -> None:
    try:
        _delete_item(path)
        print(f"Removed: {path}")
    except:
        print(f"Skipping: {path}")



def clean_output(*, clean_cache: bool = False) -> None:
    remove(PathTo.OutClient)
    remove(PathTo.OutServer)

    if clean_cache:
        remove(PathTo.OutModCache)

    remove(PathTo.OutClientArchive)
    remove(PathTo.OutServerArchive)

    print("\nOutput cleaned\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="build.clean",
        description="Cleans output directories (build results and intermediates)."
    )
    parser.add_argument(
        "--cache",
        action="store_true",
        help="Clean mod cache too."
    )
    args = parser.parse_args()

    clean_output(clean_cache=args.cache)
