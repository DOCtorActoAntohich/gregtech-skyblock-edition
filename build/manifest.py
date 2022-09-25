from __future__ import annotations

import json
import pathlib

from pydantic import BaseModel, Field, parse_obj_as, parse_raw_as

from build.paths import PathTo


class ModLoader(BaseModel):
    id: str = Field("forge-14.23.5.2860")
    primary: bool = Field(True)

    @classmethod
    def forge_2860(cls) -> list[ModLoader]:
        default_modloader = list()
        default_modloader.append(cls())
        return default_modloader


class Minecraft(BaseModel):
    version: str = Field("1.12.2")
    mod_loaders: list[ModLoader] = Field(
        default_factory=ModLoader.forge_2860, alias="modLoaders"
    )


class ModData(BaseModel):
    project_id: int = Field(..., alias="projectID")
    file_id: int = Field(..., alias="fileID")

class CurseForgeMod(ModData):
    comment: str | None = Field(None)
    required: bool = Field(True)

    @classmethod
    def from_mod_data(cls, mod_data: ModData, name: str = None) -> CurseForgeMod:
        cf_mod = parse_obj_as(cls, mod_data)
        cf_mod.comment = name
        return cf_mod

    class Config:
        allow_population_by_field_name = True


class Manifest(BaseModel):
    minecraft: Minecraft = Field(default_factory=Minecraft)
    manifest_type: str = Field("minecraftModpack", alias="manifestType")
    overrides: str = Field("overrides")
    manifest_version: int = Field(1, alias="manifestVersion")
    version: str = Field(...)
    author: str = Field(...)
    name: str = Field(...)
    files: list[CurseForgeMod] = Field(default_factory=list)

    def save(self, path: pathlib.Path):
        with path.open(mode="w") as manifest_json:
            json.dump(self.dict(by_alias=True), manifest_json, indent=2)


def read_mods() -> list[CurseForgeMod]:
    with PathTo.ModsJson.open() as file:
        mods: dict[str, dict] = json.load(file)

    return [
        CurseForgeMod.from_mod_data(data, name)
        for name, data in mods.items()
    ]


def generate_manifest() -> Manifest:
    cf_mods = read_mods()
    manifest = Manifest(
        version="1.12.2",
        author="Irgendwer1",
        name="GregTech - Skyblock Edition"
    )
    manifest.files.extend(cf_mods)

    return manifest

'''
with PathTo.ModsJson.open() as file:
    mods: dict[str, dict] = json.load(file)

with (PathTo.Repository / "manifest.json").open() as file:
    good_manifest = Manifest.parse_obj(json.load(file))

for name, data in mods.items():
    project_id = data["projectID"]
    file_id = data["fileID"]
    for mod in good_manifest.files:
        if mod.project_id == project_id and mod.file_id != file_id:
            print(f"bad: {file_id}", "\t", f"good: {mod.file_id}", "\t\t\t", name)
'''