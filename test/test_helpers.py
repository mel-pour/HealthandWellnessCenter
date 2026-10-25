from pathlib import Path
import tempfile

from data_access.text_file_storage import TextFileStorage


class TemporaryStorageMixin:
    def make_storage(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        storage = TextFileStorage.__new__(TextFileStorage)
        storage.file_path = Path(self.temp_directory.name) / "healthcare_data.txt"
        storage.save({
            "customers": [],
            "offerings": [],
            "appointments": [],
            "centers": []
        })
        return storage

    def close_storage(self):
        self.temp_directory.cleanup()
