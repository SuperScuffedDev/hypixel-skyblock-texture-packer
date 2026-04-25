"""model file writing"""
from pathlib import Path
import json
from logger import logger

model_data = {}

def item_model_write(texture_name: str, model: str, directory: Path):
    """writes the model file for a texture"""
    data = {
        "parent": model,
        "textures": {
            "layer0": f"packgen:item/{texture_name}"
        }
    }

    with open(directory/f"{texture_name}.json", "w", encoding='utf-8') as model_json:
        json.dump(data, model_json, indent = 4)

        logger.info(
            "%s item model created at %s", texture_name, directory/f"{texture_name}"
        )

class MinecraftModelFile():
    """class for creating minecraft model files"""
    def __init__(self, name: str, model: str, item_model_directory: Path):
        self.name = name
        self.model = model
        self.item_model_directory = item_model_directory
        self.data = {
            "model": {}
        }
        self.parent = self.data
        self.current = "model"

    def _check_configs(self, item_id: str, configs: dict):
        """handles configs"""

        if not "held" in configs and not "modifier" in configs and not "model" in configs:
            return False

        item_data = {
            "data": {}
        }
        parent = item_data
        current = "data"

        model = self.model

        has_held = False
        if "held" in configs:
            has_held = True
            model = f"packgen:item/{configs["held"]}"
        elif "model" in configs:
            model = f"packgen:item/{configs["model"]}"

        if not "modifier" in configs:
            if not has_held:
                print("no")
                parent[current] = {
                    "model": f"packgen:item/{item_id}",
                    "type": "model"
                }

                item_model_write(item_id, model, self.item_model_directory)
            else:
                parent[current] = {
                    "cases": [
                            {
                                "model": {
                                    "model": f"packgen:skyblock/{item_id}",
                                    "type": "model"
                                },
                                "when": "gui"
                            }
                        ],
                    "fallback": {
                        "model": f"packgen:skyblock/{item_id}_held",
                        "type": "model"
                    },
                    "property": "display_context",
                    "type": "select"
                }

                item_model_write(item_id, self.model, self.item_model_directory)
                item_model_write(f"{item_id}_held", model, self.item_model_directory)
        else:
            if not has_held:
                for mod, prefix in configs["modifier"].items():
                    parent[current] = {
                        "predicate": "custom_data",
                        "property": "component",
                        "type": "condition",
                        "value": {
                            "modifier": mod
                        },
                        "on_false": {},
                        "on_true": {}
                    }

                    parent[current]["on_true"] = {
                        "model": f"packgen:item/{prefix}_{item_id}",
                        "type": "model"
                    }

                    parent = parent[current]
                    current = "on_false"
                    item_model_write(f"{prefix}_{item_id}", model, self.item_model_directory)

                parent[current] = {
                    "model": f"packgen:item/{item_id}",
                    "type": "model"
                }

                item_model_write(f"{item_id}", model, self.item_model_directory)

            else:
                for mod, prefix in configs["modifier"].items():
                    parent[current] = {
                        "predicate": "custom_data",
                        "property": "component",
                        "type": "condition",
                        "value": {
                            "modifier": mod
                        },
                        "on_true": {},
                        "on_false": {}
                    }

                    parent[current]["on_true"] = {
                        "cases": [
                                {
                                    "model": {
                                        "model": f"packgen:skyblock/{prefix}_{item_id}",
                                        "type": "model"
                                    },
                                    "when": "gui"
                                }
                            ],
                        "fallback": {
                            "model": f"packgen:skyblock/{prefix}_{item_id}_held",
                            "type": "model"
                        },
                        "property": "display_context",
                        "type": "select"
                    }

                    parent = parent[current]
                    current = "on_false"
                    item_model_write(f"{prefix}_{item_id}", self.model, self.item_model_directory)
                    item_model_write(f"{prefix}_{item_id}_held", model, self.item_model_directory)

                parent[current] = {
                    "cases": [
                            {
                                "model": {
                                    "model": f"packgen:skyblock/{item_id}",
                                    "type": "model"
                                },
                                "when": "gui"
                            }
                        ],
                    "fallback": {
                        "model": f"packgen:skyblock/{item_id}_held",
                        "type": "model"
                    },
                    "property": "display_context",
                    "type": "select"
                }

                item_model_write(f"{item_id}", self.model, self.item_model_directory)
                item_model_write(f"{item_id}_held", model, self.item_model_directory)

        return item_data["data"]

    def add_item_model(self, item_id: str, configs: Path | None):
        """adds a item model to data object"""
        item_model_data = {
            "predicate": "custom_data",
            "property": "component",
            "type": "condition",
            "value": {
                "id": item_id.upper()
            },
            "on_true": {},
            "on_false": {}
        }

        if configs:
            configs_data = {}
            with open(configs, "r", encoding='utf-8') as configs_json:
                configs_data = json.load(configs_json)

            true_configs = self._check_configs(item_id, configs_data)

            if not true_configs:
                true_configs = {
                    "model": f"packgen:skyblock/{item_id}",
                    "type": "model"
                }

            item_model_data["on_true"] = true_configs

        else:
            item_model_data["on_true"] = {
                "model": f"packgen:skyblock/{item_id}",
                "type": "model"
            }

            item_model_write(item_id, self.model, self.item_model_directory)

        self.parent[self.current] = item_model_data

        self.parent = self.parent[self.current]
        self.current = "on_false"

    def write_to_file(self, directory: Path):
        """write to a json file at dir"""

        if self.data == {"model": {}}:
            return

        self.parent["on_false"]["model"] = f"item/{self.name}"
        self.parent["on_false"]["type"] = "model"

        with open(directory/f"{self.name}.json", "w", encoding='utf-8') as model_json:
            json.dump(self.data, model_json, indent = 4)
