import sys
import tkinter
from tkinter import filedialog
from pathlib import Path
import shutil
import json

tkinter.Tk().withdraw()

def init(data):
    """initializes an empty texture pack folder"""

    data_path = Path(data)

    pack_directory = Path("./packs/") / data_path.name
    pack_directory.mkdir(exist_ok=True)

    pack_assets = pack_directory / "assets"
    pack_assets.mkdir(exist_ok=True)

    pack_minecraft = pack_assets / "minecraft"
    pack_minecraft.mkdir(exist_ok=True)

    packgen = pack_assets / "packgen"
    packgen.mkdir(exist_ok=True)

    pack_minecraft_items = pack_minecraft / "items"
    pack_minecraft_items.mkdir(exist_ok=True)

    if (data_path / "pack.png").is_file():
        shutil.copy(data_path / "pack.png", pack_directory)

    meta = {
        "pack": {
            "pack_format": 55,
            "description": "1.21.11",
        }
    }
    with open(pack_directory/"pack.mcmeta", "w", encoding='utf-8') as pack_meta:
        json.dump(meta, pack_meta, indent = 4)

    return data_path, pack_assets

input_directory = filedialog.askdirectory()

if not input_directory:
    sys.exit("fuck you too")

input_path, assets = init(input_directory)

def locate_texture(skyblock_id):
    """locates the texture for the id"""
    for texture_file in input_path.iterdir():
        if texture_file.stem.upper() == skyblock_id:
            print(texture_file.stem)


with open("./id_models.json", "r", encoding='utf-8') as id_models_json:
    id_models = json.load(id_models_json)

for model_key, model_value in id_models.items():
    for item_id in model_value["skyblock_ids"]:
        locate_texture(item_id)
