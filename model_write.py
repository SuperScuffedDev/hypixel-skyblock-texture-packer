"""model file writing"""
from pathlib import Path
import json

model_data = {}

class MinecraftModelFile():
    """class for creating minecraft model files"""
    def __init__(self, name: str):
        self.name = name
        self.data = {
            "model": {

            }
        }
        self.last_model = self.data["model"]

    def add_item_model(self, item_id: str):
        """adds a model to data object"""
        self.last_model["predicate"] = "custom_data"
        self.last_model["property"] = "component"
        self.last_model["type"] = "condition"

        self.last_model["value"] = {}
        self.last_model["value"]["id"] = item_id.upper()

        self.last_model["on_true"] = {}
        self.last_model["on_true"]["model"] = f"packgen:skyblock/{item_id.lower()}"
        self.last_model["on_true"]["type"] = "model"

        self.last_model["on_false"] = {}
        self.last_model = self.last_model["on_false"]

        print(f"{item_id} item model added to minecraft model object")

    def write_to_file(self, directory: Path):
        """write to a json file at dir"""

        if self.data == {"model": {}}:
            return

        self.last_model["model"] = "item/armor_stand"
        self.last_model["type"] = "model"

        with open(directory/f"{self.name}.json", "w", encoding='utf-8') as model_json:
            json.dump(self.data, model_json, indent = 4)

def item_model_write(item_id: str, model: str, directory: Path):
    """writes the model file for a texture"""
    data = {
        "parent": model,
        "textures": {
            "layer0": f"packgen:item/{item_id.lower()}"
        }
    }

    with open(directory/f"{item_id.lower()}.json", "w", encoding='utf-8') as model_json:
        json.dump(data, model_json, indent = 4)

    print(f"{item_id} item model created at {directory / item_id.lower()}.json")
