# GregTech - Skyblock Edition

GSE is a lightweight Skyblock modpack focused around GTCEu and Ex Nihilo with some QoL mods.

Inspired by [GregBlock](https://www.curseforge.com/minecraft/modpacks/gregblock) and [Gregicality Skyblock Edition](https://www.curseforge.com/minecraft/modpacks/gregicality-skyblock-edition), this pack is intended to fix GregBlock's issues and avoid some of Gregicality's grind.

## Building

You have to have Python 3.10 or newer installed.

1. Run `pip3 install -r build/requirements.txt` to install required libraries.
2. Run `python -m build.main` in command line.

#### Note: updating external mods

To update external mods, you need to download the updated version and run `python build/getHash.py <mod location>`
and copy the output to the `hash` field for the mod in `mainifest.json`

## Credits

Thanks to the whole [GTCEu team](https://github.com/GregTechCEu) for making this awesome mod.
Thanks to [Prototype Trousers](https://github.com/PrototypeTrousers) for making [AE2 extended life](https://github.com/PrototypeTrousers/Applied-Energistics-2).
Thanks to [UserNM](https://github.com/Usernm0) for his awesome [circuit textures](https://github.com/Usernm0/Gregtech-5-Circuits-32x32-Usernm).
Thanks to [Colored GT Casings](https://www.curseforge.com/minecraft/texture-packs/colored-gt-casings) and [ZedTech](https://www.curseforge.com/minecraft/texture-packs/zedtech) texturepacks.
Thanks to all the people who made mods used in this pack.
