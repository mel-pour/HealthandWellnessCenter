
from data_access.text_file_storage import TextFileStorage


storage = TextFileStorage()

data = storage.load()

print("File path:", storage.file_path)
print("Data loaded successfully:")
print(data)
