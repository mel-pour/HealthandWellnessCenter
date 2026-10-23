
import json
from pathlib import Path


class TextFileStorage:
    def __init__(self):
        project_folder = Path(__file__).resolve().parent.parent

        self.file_path = (
            project_folder / "data" / "healthcare_data.txt"
        )

    def load(self):
        with self.file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, data):
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )
