import duckdb
from bench import benchmark_operation
from random_data_generator import generate_key_value_pairs 
from visualize import plot

class DuckDBDatabase:
    def __init__(self):
        # Connect to DuckDB (in-memory database)
        self.conn = duckdb.connect(database=':memory:')
        # Create table if it does not exist
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS KeyValueStore (
                key VARCHAR PRIMARY KEY,
                value VARCHAR
            )
        """)

    def instantiate(self):
        """Clears all records in the KeyValueStore table to start with a fresh dataset."""
        self.conn.execute("DELETE FROM KeyValueStore")

    def read(self, key):
        """Reads the value associated with the given key."""
        result = self.conn.execute("SELECT value FROM KeyValueStore WHERE key = ?", (key,)).fetchone()
        return result[0] if result else None

    def write(self, key, value):
        """Writes a key-value pair to the table or updates the value if the key exists."""
        self.conn.execute("""
            INSERT INTO KeyValueStore (key, value) 
            VALUES (?, ?)
            ON CONFLICT(key) 
            DO UPDATE SET value = excluded.value
        """, (key, value))

    def delete(self, key):
        """Deletes a key-value pair by key."""
        self.conn.execute("DELETE FROM KeyValueStore WHERE key = ?", (key,))

    def get_all_keys(self):
        """Fetches all keys from the KeyValueStore table."""
        result = self.conn.execute("SELECT key FROM KeyValueStore").fetchall()
        return [row[0] for row in result]

data = generate_key_value_pairs(1000)
print("Sample data:", list(data.items())[:5])

# Initialize DuckDB adapter
duck_db = DuckDBDatabase()

# Step 5.1: Instantiate (clear all records)
instantiate_time = benchmark_operation(duck_db, duck_db.instantiate)
print(f"Instantiate Time: {instantiate_time:.5f} seconds")

# Step 5.2: Write (Insert all key-value pairs from generated data)
write_times = []
for key, value in data.items():
    write_times.append(benchmark_operation(duck_db, duck_db.write, key, value))
average_write_time = sum(write_times) / len(write_times)
print(f"Average Write Time: {average_write_time:.5f} seconds per record")

# Step 5.3: Read (Read all keys in the generated data)
read_times = []
for key in data.keys():
    read_times.append(benchmark_operation(duck_db, duck_db.read, key))
average_read_time = sum(read_times) / len(read_times)
print(f"Average Read Time: {average_read_time:.5f} seconds per record")

# Step 5.4: Delete (Delete all keys in the generated data)
delete_times = []
for key in data.keys():
    delete_times.append(benchmark_operation(duck_db, duck_db.delete, key))
average_delete_time = sum(delete_times) / len(delete_times)
print(f"Average Delete Time: {average_delete_time:.5f} seconds per record")

# Step 5.5: GetAllKeys (fetch all keys in one operation)
duck_db.instantiate()  # Reset data
for key, value in data.items():  # Reinsert data to test GetAllKeys
    duck_db.write(key, value)
get_all_keys_time = benchmark_operation(duck_db, duck_db.get_all_keys)
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