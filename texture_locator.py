"""locating"""
from pathlib import Path
from logger import logger

class TextureLocator():
    """locator of textures"""
    def __init__(self, input_path: str):
        self.found = 0
        self.not_found = 0
        self.unassigned = []
        self.input_path = Path(input_path)

    def locate_texture(self, skyblock_id: str) -> Path | None:
        """locates the texture for the id"""
        for texture_file in self.input_path.iterdir():
            if texture_file.stem.upper() == skyblock_id:
                logger.info(
                    "%s texture found", skyblock_id
                )
                self.found += 1
                return texture_file

        logger.warning(
            "%s texture not found", skyblock_id
        )
        self.unassigned.append(skyblock_id)
        self.not_found += 1

    def log_unassigned(self, pack_name: str) -> None:
        """log unassigned textures"""
        self.unassigned.sort()

        with open(f"./log/{pack_name}_unassigned.txt", "w", encoding='utf-8') as log:
            log.truncate()
            for item in self.unassigned:
                log.write(f"{item}\n")
