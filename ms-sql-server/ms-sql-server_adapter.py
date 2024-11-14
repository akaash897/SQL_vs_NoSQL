import pyodbc
from bench import benchmark_operation
from random_data_generator import generate_key_value_pairs 
from visualize import plot
import pyodbc

import pyodbc

class SQLServerDatabase:
    def __init__(self):
        # Connect to the SQL Server database AKAASH897\SQLEXPRESS -E
        self.connection = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"  # Update with instance name if different
            "DATABASE=TestDatabase;"
            "Trusted_Connection=yes;"
        )
        self.cursor = self.connection.cursor()

    def instantiate(self):
        """Clears all records in the KeyValueStore table to start with a fresh dataset."""
        self.cursor.execute("DELETE FROM KeyValueStore")
        self.connection.commit()

    def read(self, key):
        """Reads the value associated with the given key."""
        self.cursor.execute("SELECT value FROM KeyValueStore WHERE store_key = ?", (key,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def write(self, key, value):
        """Writes a key-value pair to the table or updates the value if the key exists."""
        self.cursor.execute("""
            BEGIN
                IF EXISTS (SELECT 1 FROM KeyValueStore WHERE store_key = ?)
                    UPDATE KeyValueStore SET value = ? WHERE store_key = ?
                ELSE
                    INSERT INTO KeyValueStore (store_key, value) VALUES (?, ?)
            END
        """, (key, value, key, key, value))
        self.connection.commit()

    def delete(self, key):
        """Deletes a key-value pair by key."""
        self.cursor.execute("DELETE FROM KeyValueStore WHERE store_key = ?", (key,))
        self.connection.commit()

    def get_all_keys(self):
        """Fetches all keys from the KeyValueStore table."""
        self.cursor.execute("SELECT store_key FROM KeyValueStore")
        return [row[0] for row in self.cursor.fetchall()]

data = generate_key_value_pairs(1000)
print("Sample data:", list(data.items())[:5])

# Initialize SQL Server adapter
sql_server_db = SQLServerDatabase()

# Step 6.1: Instantiate (clear all records)
instantiate_time = benchmark_operation(sql_server_db, sql_server_db.instantiate)
print(f"Instantiate Time: {instantiate_time:.5f} seconds")

# Step 6.2: Write (Insert all key-value pairs from generated data)
write_times = []
for key, value in data.items():
    write_times.append(benchmark_operation(sql_server_db, sql_server_db.write, key, value))
average_write_time = sum(write_times) / len(write_times)
print(f"Average Write Time: {average_write_time:.5f} seconds per record")

# Step 6.3: Read (Read all keys in the generated data)
read_times = []
for key in data.keys():
    read_times.append(benchmark_operation(sql_server_db, sql_server_db.read, key))
average_read_time = sum(read_times) / len(read_times)
print(f"Average Read Time: {average_read_time:.5f} seconds per record")

# Step 6.4: Delete (Delete all keys in the generated data)
delete_times = []
for key in data.keys():
    delete_times.append(benchmark_operation(sql_server_db, sql_server_db.delete, key))
average_delete_time = sum(delete_times) / len(delete_times)
print(f"Average Delete Time: {average_delete_time:.5f} seconds per record")

# Step 6.5: GetAllKeys (fetch all keys in one operation)
sql_server_db.instantiate()  # Reset data
for key, value in data.items():  # Reinsert data to test GetAllKeys
    sql_server_db.write(key, value)
get_all_keys_time = benchmark_operation(sql_server_db, sql_server_db.get_all_keys)
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