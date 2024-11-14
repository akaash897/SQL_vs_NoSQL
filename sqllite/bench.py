import time

def benchmark_operation(database, operation, *args):
    """Runs a database operation five times and returns the average execution time."""
    times = []
    for _ in range(5):
        start_time = time.time()
        operation(*args)
        times.append(time.time() - start_time)
    return sum(times) / len(times)
