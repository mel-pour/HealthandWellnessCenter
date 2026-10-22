
import json
from pathlib import Path


class TextFileStorage:
    def __init__(self):
        project_folder = Path(__file__).resolve().parent.parent
        data_folder = project_folder / "data"
        data_folder.mkdir(exist_ok=True)

        self.file_path = data_folder / "healthcare_data.txt"

        if not self.file_path.exists():
            self.save({
                "customers": [],
                "offerings": [],
                "appointments": [],
                "centers": []
            })

    def load(self):
        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    def save(self, data):
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
