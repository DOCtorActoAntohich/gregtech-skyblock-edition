import pathlib


ManifestName = "manifest.json"

class PathTo:
    BuildDirectory = pathlib.Path(__file__).parent
    Repository = BuildDirectory.parent
    BuildOut = Repository / "buildOut"
    ClientOut = BuildOut / "client"
    ClientArchiveNoFormat = ClientOut
    ClientOverrides = ClientOut / "overrides"
    ClientOutScripts = ClientOverrides / "scripts"
    ServerOut = BuildOut / "server"
    ModCache = BuildOut / "modcache"
    Mods = Repository / "mods"
    Manifest = Repository / ManifestName
