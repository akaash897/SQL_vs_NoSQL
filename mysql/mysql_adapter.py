import mysql.connector
from bench import benchmark_operation
from random_data_generator import generate_key_value_pairs 
from visualize import plot

class MySQLDatabase:
    def __init__(self, host='localhost', user='root', password='', database='KeyValueDB'):
        # Connect to MySQL database
        self.conn = mysql.connector.connect(
            host=host,
            port=3306,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        
        # Create database if it doesn't exist
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        self.conn.database = database

    def instantiate(self):
        """Drops and recreates the KeyValueStore table to start with a fresh dataset."""
        # Drop the table if it exists to start from scratch
        self.cursor.execute("DROP TABLE IF EXISTS KeyValueStore")
        
        # Recreate the KeyValueStore table
        self.cursor.execute("""
            CREATE TABLE KeyValueStore (
                `key` VARCHAR(255) PRIMARY KEY,
                `value` TEXT
            )
        """)
        self.conn.commit()

    def read(self, key):
        """Reads the value associated with the given key."""
        self.cursor.execute("SELECT `value` FROM KeyValueStore WHERE `key` = %s", (key,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def write(self, key, value):
        """Writes a key-value pair to the table or updates the value if the key exists."""
        self.cursor.execute("""
            INSERT INTO KeyValueStore (`key`, `value`) VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE `value` = VALUES(`value`)
        """, (key, value))
        self.conn.commit()

    def delete(self, key):
        """Deletes a key-value pair by key."""
        self.cursor.execute("DELETE FROM KeyValueStore WHERE `key` = %s", (key,))
        self.conn.commit()

    def get_all_keys(self):
        """Fetches all keys from the KeyValueStore table."""
        self.cursor.execute("SELECT `key` FROM KeyValueStore")
        return [row[0] for row in self.cursor.fetchall()]

    def close(self):
        """Closes the database connection."""
        self.cursor.close()
        self.conn.close()

# Generate 1000 key-value pairs
data = generate_key_value_pairs(1000)
print("Sample data:", list(data.items())[:5])  

# Initialize MySQL adapter
mysql_db = MySQLDatabase(user='root', password='admin')  # Replace 'your_password' with your MySQL root password

# Step 4.1: Instantiate (drop and recreate table)
instantiate_time = benchmark_operation(mysql_db, mysql_db.instantiate)
print(f"Instantiate Time: {instantiate_time:.5f} seconds")

# Step 4.2: Write (Insert all key-value pairs from generated data)
write_times = []
for key, value in data.items():
    write_times.append(benchmark_operation(mysql_db, mysql_db.write, key, value))
average_write_time = sum(write_times) / len(write_times)
print(f"Average Write Time: {average_write_time:.5f} seconds per record")

# Step 4.3: Read (Read all keys in the generated data)
read_times = []
for key in data.keys():
    read_times.append(benchmark_operation(mysql_db, mysql_db.read, key))
average_read_time = sum(read_times) / len(read_times)
print(f"Average Read Time: {average_read_time:.5f} seconds per record")

# Step 4.4: Delete (Delete all keys in the generated data)
delete_times = []
for key in data.keys():
    delete_times.append(benchmark_operation(mysql_db, mysql_db.delete, key))
average_delete_time = sum(delete_times) / len(delete_times)
print(f"Average Delete Time: {average_delete_time:.5f} seconds per record")

# Step 4.5: GetAllKeys (fetch all keys in one operation)
mysql_db.instantiate()  # Reset data
for key, value in data.items():  # Reinsert data to test GetAllKeys
    mysql_db.write(key, value)
get_all_keys_time = benchmark_operation(mysql_db, mysql_db.get_all_keys)
print(f"GetAllKeys Time: {get_all_keys_time:.5f} seconds")

# Close MySQL connection
mysql_db.close()

# Create a dictionary of operation times for plotting
operation_times = {
    "Instantiate": instantiate_time,
    "Write": average_write_time,
    "Read": average_read_time,
    "Delete": average_delete_time,
    "GetAllKeys": get_all_keys_time
}

plot(operation_times)