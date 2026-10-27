
from data_access.text_file_storage import TextFileStorage


storage = TextFileStorage()

test_data = {
    "customers": [],
    "offerings": [],
    "appointments": [],
    "centers": []
}

# Save the data
storage.save(test_data)
print("Data saved successfully!")

# Load the data
loaded_data = storage.load()
print("Data loaded successfully!")

# Check whether the loaded data matches
assert loaded_data == test_data

print("Test passed!")
print(loaded_data)
