Software and Data Engineering -  Major Project

Group No.: 71

Collaborators (Name - Roll): 
- Akaash Chatterjee - M24CSE002
- Aman Saini - M24CSE003
- Bera Swaminath Ansuman Sabita - M24CSE007

This README will provide an organized guide for replicating the experiment across all these databases, summarizing installation steps, setup requirements, and other essential information for each of the databases tested. 
---

# Topic: A performance comparison of SQL and NoSQL databases

Based on the research paper: Y. Li and S. Manoharan, "A performance comparison of SQL and NoSQL databases," 2013 IEEE Pacific Rim Conference on Communications, Computers and Signal Processing (PACRIM), Victoria, BC, Canada, 2013, pp. 15-19, doi: 10.1109/PACRIM.2013.6625441. 

This repository contains the experimental setup for comparing the performance of various databases as key-value stores. The performance is measured on basic CRUD operations (Instantiate, Read, Write, Delete, GetAllKeys) for each database.

## Project Structure

The directories represent different databases tested in this experiment:

- **couchdb**
- **duck-db**
- **mongo**
- **ms-sql-server**
- **mysql**
- **sqlite**
- **tiny-db**

Each directory contains scripts and instructions specific to setting up and benchmarking that particular database.

---

## Setup Instructions

### Prerequisites

- Python 3.6+ installed
- Required Python packages: see [requirements.txt](requirements.txt)
- Access to install and start services like Oracle MySQL, MongoDB, CouchDB, and SQL Server Express, as necessary.

Install all dependencies:

```bash
pip install requirements.txt
```

---

## Database-Specific Setup and Installation

### 1. CouchDB

#### Installation

- **macOS**: `brew install couchdb`
- **Ubuntu**:
  ```bash
  sudo apt update
  sudo apt install couchdb
  ```
- **Windows**: Download and install CouchDB from [CouchDB's official site](https://couchdb.apache.org/).

#### Configuration

- After installation, access CouchDB’s admin console at `http://127.0.0.1:5984/_utils/`.
- Create a database named `KeyValueDB`.

#### Python Adapter within CouchDB database folder

To interact with CouchDB REST API. Ensure CouchDB is running on `localhost` at port `5984`.

---

### 2. DuckDB

DuckDB is an in-process SQL OLAP database that does not require a server or complex setup.

#### Installation

Install via `pip`:

```bash
pip install duckdb
```

#### Setup

DuckDB uses a local `.db` file. This file is created automatically when running DuckDB scripts.

#### Python Adapter

DuckDB is directly accessible via Python. Use the `duckdb` package for database operations.

---

### 3. MongoDB

#### Installation

- **macOS**: `brew install mongodb-community`
- **Ubuntu**:
  ```bash
  sudo apt update
  sudo apt install -y mongodb
  ```
- **Windows**: Download and install from [MongoDB’s official site](https://www.mongodb.com/).

#### Configuration

Start MongoDB:

```bash
mongod --dbpath <your-db-path>
```

#### Python Adapter

Uses `pymongo` to connect and interact with MongoDB. Ensure MongoDB is running on `localhost` at port `27017`.

---

### 4. Microsoft SQL Server Express

#### Installation

Download SQL Server Express from the [Microsoft SQL Server website](https://www.microsoft.com/sql-server/sql-server-downloads).

#### Configuration

- Use SQL Server Management Studio (SSMS) to create a new database `KeyValueDB`.
- Configure SQL Server to accept local connections.

#### Python Adapter

Install `pyodbc` to connect to SQL Server Express:

```bash
pip install pyodbc
```

---

### 5. MySQL

#### Installation

- **macOS**: `brew install mysql`
- **Ubuntu**:
  ```bash
  sudo apt update
  sudo apt install mysql-server
  ```
- **Windows**: Download and install MySQL from [MySQL’s official website](https://dev.mysql.com/downloads/installer/).

#### Configuration

Start MySQL server and create a database named `KeyValueDB`:

```sql
CREATE DATABASE KeyValueDB;
```

#### Python Adapter

Uses `mysql-connector-python` to connect to MySQL. Ensure MySQL is running on `localhost` at port `3306`.

---

### 6. SQLite

SQLite is a lightweight, serverless database engine that doesn’t require a separate server installation.

#### Installation

SQLite is usually bundled with Python. No additional installation is required.

#### Setup

SQLite operates directly on `.db` files, which are created automatically.

#### Python Adapter

The `sqlite3` module in Python allows direct interaction with SQLite databases.

---

### 7. TinyDB

TinyDB is an embedded document-oriented database written in Python. It does not require a server or any setup.

#### Installation

Install TinyDB with pip:

```bash
pip install tinydb
```

#### Setup

TinyDB operates directly on JSON files, which are created automatically when running scripts.

#### Python Adapter

TinyDB can be used directly within Python as it doesn’t require any server connection.

---

## Experiment Script

Each database adapter has been implemented in Python to support the following operations:

1. **Instantiate** - Initializes a fresh key-value store by creating a new database or collection.
2. **Read** - Fetches the value associated with a specific key.
3. **Write** - Inserts or updates a key-value pair.
4. **Delete** - Removes a key-value pair by key.
5. **GetAllKeys** - Retrieves all keys stored in the database.

The benchmark function `benchmark_operation` runs each operation five times and calculates the average execution time.

### Example Usage

```python
from your_database_adapter import DatabaseAdapter

# Initialize adapter
db = DatabaseAdapter()

# Benchmark each operation
instantiate_time = benchmark_operation(db, db.instantiate)
write_time = benchmark_operation(db, db.write, 'sample_key', 'sample_value')
read_time = benchmark_operation(db, db.read, 'sample_key')
delete_time = benchmark_operation(db, db.delete, 'sample_key')
get_all_keys_time = benchmark_operation(db, db.get_all_keys)

print(f"Instantiate Time: {instantiate_time}")
print(f"Write Time: {write_time}")
print(f"Read Time: {read_time}")
print(f"Delete Time: {delete_time}")
print(f"Get All Keys Time: {get_all_keys_time}")

# Close database connection if necessary
db.close()
```

---

## Results and Analysis

Once the benchmark script is executed across all databases, you will obtain average times for each operation. Plotting these results can provide a comparative view of the performance for each database.

### Optional: Visualize Results

To visualize results, use `matplotlib`:

```python
import matplotlib.pyplot as plt

operation_times = {
    "Instantiate": instantiate_time,
    "Write": write_time,
    "Read": read_time,
    "Delete": delete_time,
    "GetAllKeys": get_all_keys_time
}

plt.figure(figsize=(10, 6))
plt.bar(operation_times.keys(), operation_times.values(), color='skyblue')
plt.xlabel("Operations")
plt.ylabel("Average Time (seconds)")
plt.title("Database Operation Performance")
plt.show()
```

---

## Conclusion

This experiment provides a performance comparison of several popular databases used as key-value stores. Based on the results, you may identify which database best suits your project’s requirements based on the average execution times for each CRUD operation.

---

## References

Y. Li and S. Manoharan, "A performance comparison of SQL and NoSQL databases," 2013 IEEE Pacific Rim Conference on Communications, Computers and Signal Processing (PACRIM), Victoria, BC, Canada, 2013, pp. 15-19, doi: 10.1109/PACRIM.2013.6625441.
