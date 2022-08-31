#!/usr/bin/env python3

"""build client & server bundles"""

# if there is a problem with building, please let htmlcsjs know
from genericpath import isdir
from importlib.resources import path
import os
import pathlib
import sys
import shutil
import subprocess
import requests
import json
import hashlib
import argparse

from manifest_models import Manifest


def parse_args():
    parser = argparse.ArgumentParser(prog="build", description=__doc__)
    parser.add_argument("--sha", action="store_true", help="append git hash to zips")
    parser.add_argument("--name", type=str, help="append name to zips")
    parser.add_argument("--retries", type=int, default=3, help="download attempts before failure")
    parser.add_argument("--clean", action="store_true", help="clean output dirs")
    parser.add_argument("--dev_build", action="store_true", help="makes a folder with all the files symlinked for development. probally only works on linux")
    parser.add_argument("--try_server", action="store_true", help="tries to use old way of getting server jars")
    return parser.parse_args()


modlist = []
modURLlist = []
modClientOnly = []


# for mod in manifest["externalDeps"]:
#    with open(basePath + "/mods/" + mod["url"].split("/")[-1], "w+b") as jar:
#        for i in range(args.retries + 1):
#            if i == args.retries:
#                raise Exception("Download failed")

#            r = requests.get(mod["url"])

#            hash = hashlib.sha256(jar.read()).hexdigest()
#            if str(hash) == mod["hash"]:
#                jar.write(r.content)
#                modlist.append(mod["name"])
#                print("hash succsessful")
#                break
#            else:
#                print("hash unsuccsessful")
#                print("use", str(hash), "this if it is consistant across runs")
#                pass


'''
if args.try_server:
    for mod in manifest["files"]:
        url = "https://cursemeta.dries007.net/" + str(mod["projectID"]) + "/" + str(mod["fileID"]) + ".json"
        r = requests.get(url)
        metadata = json.loads(r.text)
        if "name" in mod:
            name = mod["name"]
            if name[-4:] != ".jar":
                name += ".jar"
            modlist.append(name)
        else:
            modlist.append(metadata["FileName"])
        modURLlist.append(metadata["DownloadURL"])
        try:
            modClientOnly.append(mod["clientOnly"])
        except:
            modClientOnly.append(False)

    print("modlist compiled")

    with open(basePath + "/buildOut/modlist.html", "w") as file:
        data = "<html><body><h1>Modlist</h1><ul>"
        for mod in modlist:
            data += "<li>" + mod.split(".jar")[0] + "</li>"
        data += "</ul></body></html>"
        file.write(data)

    print("modlist.html done")

    shutil.copy(basePath + "/manifest.json", basePath + "/buildOut/server/manifest.json")
    shutil.copy(basePath + "/LICENSE", basePath + "/buildOut/server/LICENSE")
    shutil.copy(basePath + "/launch.sh", basePath + "/buildOut/server/launch.sh")

    for dir in serverCopyDirs:
        try:
            shutil.copytree(basePath + dir, basePath + "/buildOut/server" + dir)
        except Exception as e:
            print("Directory exists, skipping")
    print("directories copied to buildOut/server")

    for i, mod in enumerate(modURLlist):
        jarname = mod.split("/")[-1]
        if (modClientOnly[i] == True):
            break

        if os.path.exists(os.path.join(cachepath, jarname)):
            shutil.copy2(os.path.join(cachepath, jarname), os.path.join(basePath, "buildOut", "server", "mods", jarname))
            print("%s loaded from cache" % (mod))
            continue

        with open(basePath + "/buildOut/server/mods/" + jarname, "w+b") as jar:
            r = requests.get(mod)
            jar.write(r.content)
            print(mod + " Downloaded")
    print("Mods Downloaded")

    with open(basePath + "/buildOut/server/forge-installer.jar", "w+b") as jar:
        forgeVer = manifest["minecraft"]["modLoaders"][0]["id"].split("-")[-1]
        mcVer = manifest["minecraft"]["version"]
        url = (
            "https://maven.minecraftforge.net/net/minecraftforge/forge/"
            + mcVer
            + "-"
            + forgeVer
            + "/forge-"
            + mcVer
            + "-"
            + forgeVer
            + "-installer.jar"
        )
        r = requests.get(url)
        jar.write(r.content)
    print("Forge installer Downloaded")

    # TODO: make a portable version between versions

    vanilla = basePath + "/buildOut/server/minecraft_server.1.12.2.jar"

    if not os.path.isfile(vanilla):
        with open(basePath + "/buildOut/server/minecraft_server.1.12.2.jar", "w+b") as jar:
            url = "https://launcher.mojang.com/v1/objects/886945bfb2b978778c3a0288fd7fab09d315b25f/server.jar"
            r = requests.get(url)
            jar.write(r.content)
        print("Vanilla Downloaded")

    subprocess.run(["java", "-jar", "forge-installer.jar", "--installServer"], cwd=basePath + "/buildOut/server/")
    print("Forge Installed")

    try:
        os.remove(basePath + "/buildOut/server/forge-installer.jar")
    except Exception as e:
        print("Couldn't delete forge-installer.jar: %s" % (e))
    try:
        os.remove(basePath + "/buildOut/server/forge-installer.jar.log")
    except Exception as e:
        print("Couldn't delete forge-installer.jar.log: %s" % (e))

    archive = "buildOut/server"
    if sha:
        archive = "%s-%s" % (archive, sha)
    shutil.make_archive(archive, "zip", basePath + "/buildOut/server")
    print('server zip "%s.zip" made' % (archive))

if (args.dev_build):
    mkdirs(basePath + "/buildOut/mmc/minecraft")
    try:
        shutil.rmtree(basePath + "/buildOut/mmc/minecraft/mods/")
    except:
        pass
    shutil.copytree(basePath + "/buildOut/server/mods/", basePath + "/buildOut/mmc/minecraft/mods/")
    for dir in copyDirs:
        try:
            os.symlink(basePath + dir, basePath + "/buildOut/mmc/minecraft/" + dir)
        except Exception as e:
            print("Directory exists, skipping")
        print("directories copied to buildOut/mmc/minecraft")

    for i, mod in enumerate(modURLlist):
        jarname = mod.split("/")[-1]
        if (modClientOnly[i] == False):
            break

        with open(basePath + "/buildOut/mmc/minecraft/mods/" + jarname, "w+b") as jar:
            r = requests.get(mod)
            jar.write(r.content)
            print(mod + " Downloaded")

    shutil.copy(basePath + "/mmc-instance-data.json", basePath + "/buildOut/mmc/mmc-pack.json")
    instanceFolder = input("What is your MultiMC instance folder:")
    instanceName = input("What do you want to call the instance:")
    os.symlink(basePath + "/buildOut/mmc/", instanceFolder + "/" + instanceName)
    print("you might need to add an instance.cfg for mmc to reconise it")'''



ManifestName = "manifest.json"

class PathTo:
    BuildDirectory = pathlib.Path(__file__).parent
    Repository = BuildDirectory.parent
    BuildOut = Repository / "buildOut"
    ClientOut = BuildOut / "client"
    ClientArchiveNoFormat = ClientOut
    ClientOverrides = ClientOut / "overrides"
    ServerOut = BuildOut / "server"
    ModCache = BuildOut / "modcache"
    Mods = Repository / "mods"
    Manifest = Repository / ManifestName



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
        try:
            shutil.copytree(directory, PathTo.ClientOverrides / directory.name)
        except FileNotFoundError:
            print(f"'{directory.name}' was not found, skipping")
        except FileExistsError:
            print(f"'{directory.name}' is already in client out directory, skipping")
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