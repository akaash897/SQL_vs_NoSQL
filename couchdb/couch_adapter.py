import couchdb
from bench import benchmark_operation
from random_data_generator import generate_key_value_pairs 
from visualize import plot

class CouchDBDatabase:
    def __init__(self):
        # Connect to CouchDB server
        self.couch = couchdb.Server("http://admin:admin@127.0.0.1:5984/")
        self.db_name = "test_database"
        
        # Create or open the database
        if self.db_name in self.couch:
            self.db = self.couch[self.db_name]
        else:
            self.db = self.couch.create(self.db_name)

    def instantiate(self):
        """Clears all documents in the database to start with a fresh dataset."""
        for doc_id in list(self.db):
            self.db.delete(self.db[doc_id])

    def read(self, key):
        """Reads the value associated with the given key."""
        try:
            doc = self.db[key]
            return doc['value']
        except couchdb.ResourceNotFound:
            return None

    def write(self, key, value):
        """Writes a key-value pair to the database or updates the value if the key exists."""
        if key in self.db:
            doc = self.db[key]
            doc['value'] = value
            self.db.save(doc)
        else:
            self.db[key] = {'value': value}

    def delete(self, key):
        """Deletes a key-value pair by key."""
        try:
            doc = self.db[key]
            self.db.delete(doc)
        except couchdb.ResourceNotFound:
            pass

    def get_all_keys(self):
        """Fetches all keys from the database."""
        return [doc.id for doc in self.db.view('_all_docs')]

data = generate_key_value_pairs(1000)
print("Sample data:", list(data.items())[:5])

# Initialize CouchDB adapter
couch_db = CouchDBDatabase()

# Step 5.1: Instantiate (clear all records)
instantiate_time = benchmark_operation(couch_db, couch_db.instantiate)
print(f"Instantiate Time: {instantiate_time:.5f} seconds")

# Step 5.2: Write (Insert all key-value pairs from generated data)
write_times = []
for key, value in data.items():
    write_times.append(benchmark_operation(couch_db, couch_db.write, key, value))
average_write_time = sum(write_times) / len(write_times)
print(f"Average Write Time: {average_write_time:.5f} seconds per record")

# Step 5.3: Read (Read all keys in the generated data)
read_times = []
for key in data.keys():
    read_times.append(benchmark_operation(couch_db, couch_db.read, key))
average_read_time = sum(read_times) / len(read_times)
print(f"Average Read Time: {average_read_time:.5f} seconds per record")

# Step 5.4: Delete (Delete all keys in the generated data)
delete_times = []
for key in data.keys():
    delete_times.append(benchmark_operation(couch_db, couch_db.delete, key))
average_delete_time = sum(delete_times) / len(delete_times)
print(f"Average Delete Time: {average_delete_time:.5f} seconds per record")

# Step 5.5: GetAllKeys (fetch all keys in one operation)
couch_db.instantiate()  # Reset data
for key, value in data.items():  # Reinsert data to test GetAllKeys
    couch_db.write(key, value)
get_all_keys_time = benchmark_operation(couch_db, couch_db.get_all_keys)
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