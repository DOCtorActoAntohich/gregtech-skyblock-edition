import pathlib


class PathTo:
    BuildDirectory = pathlib.Path(__file__).parent
    Repository = BuildDirectory.parent

    ModsJson = Repository / "mods.json"
    LocalModsFolder = Repository / "mods"

    BuildOut = Repository / "buildOut"
    OutModCache = BuildOut / "modcache"

    OutClient = BuildOut / "client"
    OutServer = BuildOut / "server"

    OutClientManifest = OutClient / "manifest.json"
    OutClientOverrides = OutClient / "overrides"
    OutClientScripts = OutClientOverrides / "scripts"
    OutClientMods = OutClientOverrides / "mods"

    OutClientArchive = BuildOut / "client.zip"
    OutServerArchive = BuildOut / "server.zip"

    OutServerMods = OutServer / "mods"
