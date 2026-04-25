"""main"""
import sys
import shutil
import json
import tkinter
from tkinter import filedialog
from pathlib import Path
from logger import logger

import model_write
import texture_locator

sys.setrecursionlimit(2000)
tkinter.Tk().withdraw()

def init(data_input: str, data_output) -> tuple[Path, Path, Path]:
    """initializes an empty texture pack folder"""

    data_path = Path(data_input)

    pack_directory = Path(data_output) / data_path.name
    pack_directory.mkdir(exist_ok=True)

    pack_assets = pack_directory / "assets"
    pack_assets.mkdir(exist_ok=True)

    pack_minecraft = pack_assets / "minecraft"
    pack_minecraft.mkdir(exist_ok=True)

    packgen_directory = pack_assets / "packgen"
    packgen_directory.mkdir(exist_ok=True)

    packgen_textures = packgen_directory / "textures"
    packgen_textures.mkdir(exist_ok=True)

    packgen_textures_item = packgen_textures / "item"
    packgen_textures_item.mkdir(exist_ok=True)

    packgen_models = packgen_directory / "models"
    packgen_models.mkdir(exist_ok=True)

    packgen_models_skyblock = packgen_models / "skyblock"
    packgen_models_skyblock.mkdir(exist_ok=True)

    pack_minecraft_items = pack_minecraft / "items"
    pack_minecraft_items.mkdir(exist_ok=True)

    pack_png = data_path / "pack.png"

    if pack_png.is_file():
        shutil.copy(pack_png, pack_directory)
        # this still runs if no pack.png

    meta = {
        "pack": {
            "min_format": [75, 0],
            "max_format": [75, 0],
            "description": "hypixel skyblock"
        }
    }
    with open(pack_directory/"pack.mcmeta", "w", encoding='utf-8') as pack_meta:
        json.dump(meta, pack_meta, indent = 4)


    logger.info(
        "created pack folder at %s", pack_directory.resolve()
    )
    return data_path, pack_assets, packgen_directory

logger.info("select an input directory(your textures)")
input_directory = filedialog.askdirectory()
logger.warning(
    "selected %s as input directory", input_directory
)

logger.info("select output directory(folder to put generated texture pack in)")
output_directory = filedialog.askdirectory()
logger.warning(
    "selected %s as output directory", output_directory
)


if not input_directory or not output_directory:
    sys.exit("goodbye")

locator = texture_locator.TextureLocator(input_directory)
input_path, assets, packgen = init(input_directory, output_directory)

item_model_directory = packgen / "models" / "skyblock"
texture_copy_directory = packgen / "textures" / "item"
minecraft_model_directory = assets / "minecraft" / "items"

custom_models_path = input_path / "models/"

if custom_models_path.exists():
    shutil.copytree(input_path / "models", packgen / "models" / "item")

with open("./id_models.json", "r", encoding='utf-8') as id_models_json:
    id_models = json.load(id_models_json)

for model_key, model_value in id_models.items():
    model_object = model_write.MinecraftModelFile(
        model_key,
        model_value["model"],
        item_model_directory
    )

    for item_id in model_value["skyblock_ids"]:
        texture = locator.locate_texture(item_id)

        if not texture:
            continue

        if texture.is_file():
            shutil.copy(texture, texture_copy_directory)
            logger.info(
                "%s texture file copied to %s", item_id, texture_copy_directory / texture.name
            )

            model_object.add_item_model(texture.stem, None)
            logger.info(
                "%s added to minecraft model object", item_id
            )

        elif texture.is_dir():
            for mc_meta_file in texture.glob("*.png.mcmeta"):
                shutil.copy(mc_meta_file, texture_copy_directory)

                logger.info(
                    "%s mcmeta file copied to %s",
                    mc_meta_file.stem,
                    texture_copy_directory / mc_meta_file.name
                )

            for png_file in texture.glob("*.png"):
                shutil.copy(
                    png_file,
                    texture_copy_directory
                )

                logger.info(
                    "%s texture file copied to %s",
                    png_file.stem,
                    texture_copy_directory / png_file.name
                )

            configs = texture / "configs.json"
            if configs.is_file():
                model_object.add_item_model(texture.stem, configs)
            else:
                model_object.add_item_model(texture.stem, None)

        else:
            logger.error(
                "%s input is not valid", texture
            )

    model_object.write_to_file(assets / "minecraft" / "items")


sys.setrecursionlimit(1000)
locator.log_unassigned(input_path.stem)
print("")
logger.info(
    "loaded %d textures into pack", locator.found
)
logger.info(
    "%d textures unassigned.", locator.not_found
)
logger.info(
    "check log folder for full list of unassigned textures."
)
