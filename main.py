"""main"""
import time
import sys
import tkinter
from tkinter import filedialog
from pathlib import Path
import shutil
import json

import model_write
import texture_locator

start = time.perf_counter()

sys.setrecursionlimit(2000)

tkinter.Tk().withdraw()

def init(data_input: str, data_output):
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
    
    if (data_path / "pack.png").is_file():
        shutil.copy(data_path / "pack.png", pack_directory)

    meta = {
        "pack": {
            "min_format": [75, 0],
            "max_format": [75, 0],
            "description": "hypixel skyblock"
        }
    }
    with open(pack_directory/"pack.mcmeta", "w", encoding='utf-8') as pack_meta:
        json.dump(meta, pack_meta, indent = 4)


    print(f"created pack folder at {pack_directory.resolve()}")
    return data_path, pack_assets, packgen_directory

print("select input directory")
input_directory = filedialog.askdirectory()
print("select output directory")
output_directory = filedialog.askdirectory()

if not input_directory or not output_directory:
    sys.exit("fuck you too")

locator = texture_locator.TextureLocator(input_directory)
input_path, assets, packgen = init(input_directory, output_directory)

custom_models_path = input_path / "models/"

if custom_models_path.exists():
    shutil.copytree(input_path / "models", packgen / "models" / "item")

with open("./id_models.json", "r", encoding='utf-8') as id_models_json:
    id_models = json.load(id_models_json)

for model_key, model_value in id_models.items():
    new_model = model_write.MinecraftModelFile(model_key)

    texture_copy_directory = packgen / "textures" / "item"
    item_model_directory = packgen / "models" / "skyblock"
    for item_id in model_value["skyblock_ids"]:
        texture = locator.locate_texture(item_id)

        if texture and texture.is_file():
            shutil.copy(texture, texture_copy_directory)
            print(f"{item_id} texture file copied to {texture_copy_directory / texture.name}")

            model_write.item_model_write(item_id, model_value["model"], item_model_directory)
            new_model.add_item_model(item_id)
        elif texture and texture.is_dir:
            config_path = texture / "config.json"

            if config_path.exists():
                with open(config_path, "r", encoding='utf-8') as configs_json:
                    config_data = json.load(configs_json)
                if "held" in config_data or "model" in config_data:
                    if "held" in config_data:
                        shutil.copy(texture / f"{texture.name}.png", texture_copy_directory)
                        shutil.copy(texture / f"{texture.name}_held.png", texture_copy_directory)
                        model_write.item_model_write(
                            item_id, "minecraft:item/generated", item_model_directory
                        )
                        model_write.item_model_write(
                            f"{item_id}_HELD",
                            f"packgen:item/{config_data["held"]}",
                            item_model_directory
                        )
                        new_model.add_held_model(item_id)
                    elif "model" in config_data:
                        shutil.copy(texture / f"{texture.name}.png",texture_copy_directory)
                        model_write.item_model_write(
                            f"{item_id}_HELD",
                            f"packgen:item/{config_data["model"]}",
                            item_model_directory
                        )
                        new_model.add_item_model(item_id)
                else:
                    texture_file = texture / f"{texture.name}.png"
                    mc_meta_file = texture /  f"{texture.name}.png.mcmeta"
                    if texture_file.exists():
                        shutil.copy(texture_file, texture_copy_directory)
                        print(
                            f"{item_id} texture file copied to {texture_copy_directory / texture.name}"
                        )
                    model_write.item_model_write(
                        item_id,
                        model_value["model"],
                        item_model_directory)

                    if mc_meta_file.exists():
                        shutil.copy(mc_meta_file, texture_copy_directory)
                        print(
                            f"{item_id} texture file copied to {texture_copy_directory / texture.name}"
                        )

                    new_model.add_item_model(item_id)
            else:
                texture_file = texture / f"{texture.name}.png"
                mc_meta_file = texture /  f"{texture.name}.png.mcmeta"
                if texture_file.exists():
                    shutil.copy(texture_file, texture_copy_directory)
                    print(
                        f"{item_id} texture file copied to {texture_copy_directory / texture.name}"
                    )
                model_write.item_model_write(item_id, model_value["model"], item_model_directory)

                if mc_meta_file.exists():
                    shutil.copy(mc_meta_file, texture_copy_directory)
                    print(
                        f"{item_id} texture file copied to {texture_copy_directory / texture.name}"
                    )

                new_model.add_item_model(item_id)

    minecraft_model_directory = assets / "minecraft" / "items"
    new_model.write_to_file(assets / "minecraft" / "items")


sys.setrecursionlimit(1000)
end = time.perf_counter()
locator.log_unassigned(input_path.stem)
elapsed = end - start
print("")
print(f"loaded {locator.found} textures into pack.\n{locator.not_found} textures unassigned.")
print("check log folder for full list of unassigned textures.")
