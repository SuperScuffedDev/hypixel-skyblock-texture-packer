"""main"""
import sys
import tkinter
from tkinter import filedialog
from pathlib import Path
import shutil
import json

import model_write

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

    packgen_models_item = packgen_models / "item"
    packgen_models_item.mkdir(exist_ok=True)

    pack_minecraft_items = pack_minecraft / "items"
    pack_minecraft_items.mkdir(exist_ok=True)

    if (data_path / "pack.png").is_file():
        shutil.copy(data_path / "pack.png", pack_directory)

    meta = {
        "pack": {
            "pack_format": 75,
            "description": "1.21.11",
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

input_path, assets, packgen = init(input_directory, output_directory)

def locate_texture(skyblock_id: str):
    """locates the texture for the id"""
    for texture_file in input_path.iterdir():
        if texture_file.stem.upper() == skyblock_id:
            print(f"{skyblock_id} texture found")
            return texture_file

    print(f"{skyblock_id} texture not found")
    return False


with open("./id_models.json", "r", encoding='utf-8') as id_models_json:
    id_models = json.load(id_models_json)

for model_key, model_value in id_models.items():
    new_model = model_write.MinecraftModelFile(model_key)

    texture_copy_directory = packgen / "textures" / "item"
    item_model_directory = packgen / "models" / "skyblock"
    for item_id in model_value["skyblock_ids"]:
        texture = locate_texture(item_id)

        if texture:
            shutil.copy(texture, texture_copy_directory)
            print(f"{item_id} texture file copied to {texture_copy_directory / texture.name}")

            model_write.item_model_write(item_id, model_value["model"], item_model_directory)
            new_model.add_item_model(item_id)
        print("")
    minecraft_model_directory = assets / "minecraft" / "items"
    new_model.write_to_file(assets / "minecraft" / "items")
