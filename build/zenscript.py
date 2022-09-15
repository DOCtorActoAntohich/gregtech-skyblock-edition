from __future__ import annotations

from typing import Generator
import abc
import pathlib

from build.paths import PathTo

ZenscriptFileExtension = "zs"


class Script:
    def __init__(self, path: pathlib.Path) -> None:
        self._text: str | None = None
        self._path = path

    @property
    def text(self) -> str | None:
        return self._text

    @property
    def path(self) -> pathlib.Path:
        return self._path

    def __enter__(self) -> Script:
        self.load()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.save()
        return True

    def replace(self, before: str, after: str) -> Script:
        self._text = self._text.replace(before, after)
        return self

    def load(self) -> None:
        if self._text is not None:
            return
        with self._path.open() as file:
            self._text = file.read()

    def save(self) -> None:
        with self._path.open(mode="w") as file:
            file.write(self._text)


class ScriptSpecialConstruct(abc.ABC):
    def __init__(self, script: Script) -> None:
        super().__init__()
        self._script = script

    @abc.abstractmethod
    def handle(self) -> Script:
        pass


class ScriptPathVariableConstruct(ScriptSpecialConstruct):
    @classmethod
    def variable(cls):
        return "$SCRIPT_PATH$"

    def __init__(self, script: Script) -> None:
        super().__init__(script)

    def handle(self) -> Script:
        script_path = self._script.path.relative_to(PathTo.ClientOutScripts)
        script_path = str(script_path).replace("\\", "/")
        return self._script.replace(self.variable(), str(script_path))


def list_all_scripts(folder: pathlib.Path) -> Generator[pathlib.Path, None, None]:
    for entry in folder.iterdir():
        if entry.is_dir():
            yield from list_all_scripts(entry)
            continue

        if entry.is_file() and entry.suffix.endswith(ZenscriptFileExtension):
            yield entry


def handle_special_constructs(script: Script) -> Script:
    constructs = [
        ScriptPathVariableConstruct,
    ]
    for construct in constructs:
        script = construct(script).handle()
    return script


def postprocess_scripts(folder_path: pathlib.Path) -> None:
    for script_path in list_all_scripts(folder_path):
        with Script(script_path) as script:
            script = handle_special_constructs(script)
