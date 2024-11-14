from bench import benchmark_operation
from random_data_generator import generate_key_value_pairs 
from visualize import plot
from tinydb import TinyDB, Query

class TinyDBDatabase:
    def __init__(self):
        # Initialize TinyDB and specify the JSON file for storage
        self.db = TinyDB('test_db.json')
        self.collection = self.db.table('KeyValueStore')  # Use a separate table for testing

    def instantiate(self):
        """Clears all documents in the collection to start with a fresh dataset."""
        self.collection.truncate()

    def read(self, key):
        """Reads the value associated with the given key."""
        result = self.collection.get(Query().key == key)
        return result['value'] if result else None

    def write(self, key, value):
        """Writes a key-value pair to the collection or updates the value if the key exists."""
        self.collection.upsert({'key': key, 'value': value}, Query().key == key)

    def delete(self, key):
        """Deletes a key-value pair by key."""
        self.collection.remove(Query().key == key)

    def get_all_keys(self):
        """Fetches all keys from the collection."""
        return [doc['key'] for doc in self.collection.all()]

data = generate_key_value_pairs(1000)
print("Sample data:", list(data.items())[:5])

# Initialize TinyDB adapter
tiny_db = TinyDBDatabase()

# Step 5.1: Instantiate (clear all records)
instantiate_time = benchmark_operation(tiny_db, tiny_db.instantiate)
print(f"Instantiate Time: {instantiate_time:.5f} seconds")

# Step 5.2: Write (Insert all key-value pairs from generated data)
write_times = []
for key, value in data.items():
    write_times.append(benchmark_operation(tiny_db, tiny_db.write, key, value))
average_write_time = sum(write_times) / len(write_times)
print(f"Average Write Time: {average_write_time:.5f} seconds per record")

# Step 5.3: Read (Read all keys in the generated data)
read_times = []
for key in data.keys():
    read_times.append(benchmark_operation(tiny_db, tiny_db.read, key))
average_read_time = sum(read_times) / len(read_times)
print(f"Average Read Time: {average_read_time:.5f} seconds per record")

# Step 5.4: Delete (Delete all keys in the generated data)
delete_times = []
for key in data.keys():
    delete_times.append(benchmark_operation(tiny_db, tiny_db.delete, key))
average_delete_time = sum(delete_times) / len(delete_times)
print(f"Average Delete Time: {average_delete_time:.5f} seconds per record")

# Step 5.5: GetAllKeys (fetch all keys in one operation)
tiny_db.instantiate()  # Reset data
for key, value in data.items():  # Reinsert data to test GetAllKeys
    tiny_db.write(key, value)
get_all_keys_time = benchmark_operation(tiny_db, tiny_db.get_all_keys)
print(f"GetAllKeys Time: {get_all_keys_time:.5f} seconds")

# Create a dictionary of operation times for plotting
operation_times = {
    "Instantiate": instantiate_time,
    "Write": average_write_time,
    "Read": average_read_time,
    "Delete": average_delete_time,
    "GetAllKeys": get_all_keys_time
}

plot(operation_times)