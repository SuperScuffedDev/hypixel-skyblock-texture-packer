import tkinter
from tkinter import filedialog
from pathlib import Path
import shutil
import json

tkinter.Tk().withdraw()

def init(data):
    """initializes an empty texture pack"""

    data_path = Path(data)

    pack_folder = Path("./packs/") / data_path.name
    pack_folder.mkdir(exist_ok=True)

    pack_assets = pack_folder / "assets"
    pack_assets.mkdir(exist_ok=True)

    if (data_path / "pack.png").is_file():
        shutil.copy(data_path / "pack.png", pack_folder)

    meta = {
        "pack": {
            "pack_format": 55,
            "description": "1.21.11",
        }
    }
    with open(pack_folder/"pack.mcmeta", "w", encoding='utf-8') as pack_meta:
        json.dump(meta, pack_meta, indent = 4)


creation_data = filedialog.askdirectory()

if creation_data:
    init(creation_data)
else:
    print("fuck you too")