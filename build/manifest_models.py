from pydantic import BaseModel, Field


class ModLoader(BaseModel):
    id: str = Field(...)
    primary: bool = Field(...)

class Minecraft(BaseModel):
    version: str = Field(...)
    mod_loaders: list[ModLoader] = Field(..., alias="modLoaders")

class Dependency(BaseModel):
    project_id: int = Field(..., alias="projectID")
    file_id: int = Field(..., alias="fileID")
    required: bool = Field(...)

class Manifest(BaseModel):
    minecraft: Minecraft = Field(...)
    manifest_type: str = Field(..., alias="manifestType")
    overrides: str = Field(...)
    manifest_version: int = Field(..., alias="manifestVersion")
    version: str = Field(...)
    author: str = Field(...)
    name: str = Field(...)
    files: list[Dependency] = Field(...)
