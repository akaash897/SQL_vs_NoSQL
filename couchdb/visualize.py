import matplotlib.pyplot as plt

def plot(operation_times):
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(operation_times.keys(), operation_times.values(), color='skyblue')
    plt.xlabel("Operations")
    plt.ylabel("Average Time (seconds)")
    plt.title("CouchDB Operation Performance")
    plt.show()