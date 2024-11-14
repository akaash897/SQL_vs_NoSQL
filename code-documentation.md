Documentation for each of the Python files in each database directory, describing their purpose, main functions, and expected input/output. This should help provide a clear understanding of each file's role in the project.

---

# Code Documentation

This directory contains several Python scripts essential for benchmarking database performance on CRUD operations. The purpose of each script, its main functions, and its expected usage are detailed below.

---

## 1. `bench.py`

**Purpose**:  
`bench.py` is the main benchmarking script that measures the performance of CRUD operations on different databases. It runs each operation multiple times and calculates average execution times, enabling performance comparisons.

**Main Functions**:
- `benchmark_operation(adapter, operation, *args)`: Executes a specified operation (e.g., `instantiate`, `write`, `read`, etc.) multiple times and calculates the average execution time.
- `run_benchmarks()`: Initializes database connections and runs the benchmark for each CRUD operation.

**Expected Input**:  
No direct input is needed. The script interacts with pre-configured database adapters to run the benchmark.

**Expected Output**:  
Prints the average execution time for each operation on the console. The output can be redirected or saved for further analysis.

---

## 2. `*_adapter_run.py`

**Purpose**:  
adapter_run files for e.g. `mysql_adapter_run.py` is a specialized adapter script for interacting with a MySQL database. It defines functions to perform CRUD operations specific to MySQL, making it possible to benchmark MySQL as a key-value store.

**Main Functions**:
- `connect_to_mysql()`: Establishes a connection to the MySQL database.
- `instantiate()`: Initializes a MySQL database or table for benchmarking.
- `write(key, value)`: Inserts or updates a key-value pair.
- `read(key)`: Fetches the value associated with a specified key.
- `delete(key)`: Deletes a key-value pair from the database.
- `get_all_keys()`: Retrieves all keys from the database.

**Expected Input**:  
No command-line input is required, though database connection parameters (e.g., host, username, password) may be specified within the script.

**Expected Output**:  
Prints or logs confirmation of each CRUD operation, which can be helpful for debugging and monitoring. Used in conjunction with `bench.py` to obtain performance metrics.

---

## 4. `random_data_generator.py`

**Purpose**:  
Generates random key-value pairs that can be used as sample data for the benchmarking tests. This script ensures that each database operation is performed with realistic data.

**Main Functions**:
- `generate_data(n)`: Generates `n` random key-value pairs where keys are unique identifiers, and values are randomly generated strings or numbers.

**Expected Input**:  
Specify the number of key-value pairs to generate (`n`) as an argument within the script.

**Expected Output**:  
Returns a dictionary or list of key-value pairs, which can then be used by the benchmarking scripts to perform database operations.

**Usage Example**:
```python
data = generate_data(100)  # Generates 100 random key-value pairs
```

---

## 5. `visualize.py`

**Purpose**:  
`visualize.py` generates a visual representation of the benchmarking results, typically in the form of a bar chart or line graph. This file is used to analyze and compare the performance of each database.

**Main Functions**:
- `plot_results(results)`: Takes in a dictionary of results (e.g., average execution times for each operation) and plots them using a library like `matplotlib`.
- `save_figure(filename)`: Saves the generated plot as a PNG file (e.g., `Figure_1.png`).

**Expected Input**:  
A dictionary containing the results of each benchmark (e.g., `{"Instantiate": 0.1, "Write": 0.2, "Read": 0.05, "Delete": 0.03, "GetAllKeys": 0.04}`).

**Expected Output**:  
Displays a plot on the screen or saves it as `Figure_1.png` or a user-specified filename for inclusion in reports or presentations.

**Usage Example**:
```python
results = {
    "Instantiate": 0.1,
    "Write": 0.2,
    "Read": 0.05,
    "Delete": 0.03,
    "GetAllKeys": 0.04
}
plot_results(results)
save_figure("Figure_1.png")
```

This documentation provides a quick reference to the purpose and functions of each script in this project. By following these descriptions, users can understand how each component fits into the benchmarking experiment and how to use each script effectively.