#!/usr/bin/env python3

"""build client & server bundles"""

import pathlib
import shutil
import subprocess
import argparse

from build.manifest import generate_manifest
from build.paths import PathTo
from build.zenscript import postprocess_scripts


def parse_args():
    parser = argparse.ArgumentParser(prog="build", description=__doc__)
    parser.add_argument("--sha", action="store_true", help="append git hash to zips")
    parser.add_argument("--name", type=str, help="append name to zips")
    parser.add_argument("--retries", type=int, default=3, help="download attempts before failure")
    parser.add_argument("--dev_build", action="store_true", help="makes a folder with all the files symlinked for development. probally only works on linux")
    parser.add_argument("--try_server", action="store_true", help="tries to use old way of getting server jars")
    return parser.parse_args()


def client_copy_directories() -> list[pathlib.Path]:
    directories = ["scripts", "resources", "config", "mods", "structures"]
    return [PathTo.Repository / subdir for subdir in directories]


def server_copy_directories() -> list[pathlib.Path]:
    directories = ["scripts", "config", "mods", "structures"]
    return [PathTo.Repository / subdir for subdir in directories]


def extract_git_sha() -> str:
    try:
        p = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            cwd=PathTo.Repository
        )
        return p.stdout.strip().decode("utf-8")
    except Exception as e:
        print("Couldn't determine git SHA, skipping")
        return ""


def create_if_not_exists(path: pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def prepare_directories() -> None:
    directories = [
        PathTo.OutClientOverrides,
        PathTo.OutClientMods,
        PathTo.OutServer,
        PathTo.OutModCache
    ]
    for directory in directories:
        create_if_not_exists(directory)


def cache_server_mods():
    n_cached_mods = 0
    if not PathTo.OutServerMods.exists() or not PathTo.OutServerMods.is_dir():
        print(f"Nothing to cache from {PathTo.OutServerMods.relative_to(PathTo.Repository)}")
        return

    for mod in PathTo.OutServerMods.iterdir():
        cached_mod = PathTo.OutModCache / mod.name
        if cached_mod.exists():
            continue
        n_cached_mods += 1
        shutil.copy2(mod, cached_mod)

    if n_cached_mods > 0:
        print(f"cached {n_cached_mods} mod downloads in {PathTo.OutModCache}")


def copy_client_files() -> None:
    for directory in client_copy_directories():
        target = PathTo.OutClientOverrides / directory.name
        if target.exists():
            shutil.rmtree(target)

        try:
            shutil.copytree(directory, target)
        except FileNotFoundError:
            print(f"'{directory.name}' was not found, skipping")

    postprocess_scripts(PathTo.OutClientOverrides / "scripts")

    print(f"Directories copied to {PathTo.OutClient.relative_to(PathTo.Repository)}")


def append_sha(path: pathlib.Path, sha: str) -> pathlib.Path:
    if not sha:
        return path

    parent = path.parent

    new_name = f"{path.stem}-{sha}"
    if path.suffixes:
        new_name += "".join(path.suffixes)

    return parent / new_name


def create_client_archive(target_archive_path: pathlib.Path) -> None:
    parent = target_archive_path.parent
    file_name = target_archive_path.stem
    extension = target_archive_path.suffix.replace(".", "")
    shutil.make_archive(parent / file_name, extension, PathTo.OutClient)
    print(f"Client zip '{target_archive_path.name}' made")


def main():
    args = parse_args()

    sha = ""
    if args.sha:
        sha = extract_git_sha()

    prepare_directories()

    manifest = generate_manifest()
    manifest.save(PathTo.OutClientManifest)

    cache_server_mods()

    copy_client_files()
    create_client_archive(append_sha(PathTo.OutClientArchive, sha))


if __name__ == "__main__":
    main()
