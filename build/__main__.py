#!/usr/bin/env python3

"""build client & server bundles"""

import pathlib
import shutil
import subprocess
import argparse

from build.manifest_models import Manifest
from build.paths import ManifestName, PathTo
from build.zenscript import postprocess_scripts


def parse_args():
    parser = argparse.ArgumentParser(prog="build", description=__doc__)
    parser.add_argument("--sha", action="store_true", help="append git hash to zips")
    parser.add_argument("--name", type=str, help="append name to zips")
    parser.add_argument("--retries", type=int, default=3, help="download attempts before failure")
    parser.add_argument("--clean", action="store_true", help="clean output dirs")
    parser.add_argument("--dev_build", action="store_true", help="makes a folder with all the files symlinked for development. probally only works on linux")
    parser.add_argument("--try_server", action="store_true", help="tries to use old way of getting server jars")
    return parser.parse_args()


def client_copy_directories() -> list[pathlib.Path]:
    directories = ["scripts", "resources", "config", "mods", "structures"]
    return [PathTo.Repository / subdir for subdir in directories]


def server_copy_directories() -> list[pathlib.Path]:
    directories = ["scripts", "config", "mods", "structures"]
    return [PathTo.Repository / subdir for subdir in directories]


def clean_output() -> None:
    shutil.rmtree(PathTo.ClientOverrides, ignore_errors=True)
    shutil.rmtree(PathTo.ServerOut, ignore_errors=True)
    shutil.rmtree(PathTo.Mods, ignore_errors=True)
    print("Output cleaned")


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


def create_directories() -> None:
    directories = [
        PathTo.ClientOverrides,
        PathTo.ServerOut,
        PathTo.Mods,
        PathTo.ModCache
    ]
    for directory in directories:
        create_if_not_exists(directory)


def cache_server_mods():
    server_mods = PathTo.ServerOut / "mods"
    n_cached_mods = 0
    if not server_mods.exists() or not server_mods.is_dir():
        print(f"Nothing to cache from {server_mods.relative_to(PathTo.Repository)}")
        return

    for mod in server_mods.iterdir():
        cached_mod = PathTo.ModCache / mod.name
        if cached_mod.exists():
            continue
        n_cached_mods += 1
        shutil.copy2(mod, cached_mod)

    if n_cached_mods > 0:
        print(f"cached {n_cached_mods} mod downloads in {PathTo.ModCache}")


def copy_client_files() -> None:
    for directory in client_copy_directories():
        target = PathTo.ClientOverrides / directory.name
        if target.exists():
            shutil.rmtree(target)

        try:
            shutil.copytree(directory, target)
        except FileNotFoundError:
            print(f"'{directory.name}' was not found, skipping")

    postprocess_scripts(PathTo.ClientOverrides / "scripts")

    print(f"Directories copied to {PathTo.ClientOut.relative_to(PathTo.Repository)}")


def client_archive_path_no_format(sha: str) -> pathlib.Path:
    path = PathTo.ClientArchiveNoFormat
    if not sha:
        return path

    name = f"{path.name}-{sha}"
    return path.parent / name


def create_client_archive(target_archive_path: pathlib.Path) -> None:
    shutil.copy(PathTo.Manifest, PathTo.ClientOut / ManifestName)
    shutil.make_archive(target_archive_path, "zip", PathTo.ClientOut)
    print(f"Client zip '{target_archive_path.name}.zip' made")


def main():
    args = parse_args()
    if args.clean:
        clean_output()
        return

    sha = ""
    if args.sha:
        sha = extract_git_sha()

    manifest = Manifest.parse_file(PathTo.Manifest)

    create_directories()
    cache_server_mods()

    copy_client_files()

    create_client_archive(client_archive_path_no_format(sha))


if __name__ == "__main__":
    main()
