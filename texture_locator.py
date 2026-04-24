"""locating"""
from pathlib import Path

class TextureLocator():
    """locator of textures"""
    def __init__(self, input_path: str):
        self.found = 0
        self.not_found = 0
        self.unassigned = []
        self.input_path = Path(input_path)

    def locate_texture(self, skyblock_id: str):
        """locates the texture for the id"""
        for texture_file in self.input_path.iterdir():
            if texture_file.stem.upper() == skyblock_id:
                print("")
                print(f"{skyblock_id} texture found")
                self.found += 1
                return texture_file

        print(f"{skyblock_id} texture not found")
        self.unassigned.append(skyblock_id)
        self.not_found += 1
        return False

    def log_unassigned(self, pack_name: str):
        """log unassigned textures"""
        self.unassigned.sort()

        with open(f"./log/{pack_name}_unassigned.txt", "w", encoding='utf-8') as log:
            log.truncate()
            for item in self.unassigned:
                log.write(f"{item}\n")
