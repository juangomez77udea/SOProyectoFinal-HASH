import os
import time
import matplotlib.pyplot as plt
from blake_hash import blake_file_parallel, blake_file_concurrent
from sha256_hash import sha256_file_parallel, sha256_file_concurrent
from md5_hash import md5_file_parallel, md5_file_concurrent

def create_test_file(size_mb):
    filename = f"test_file_{size_mb}MB.bin"
    with open(filename, "wb") as f:
        f.write(os.urandom(size_mb * 1024 * 1024))
    return filename

def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return end_time - start_time, result

def run_tests(sizes):
    results = {
        "blake": {"parallel": [], "concurrent": []},
        "sha256": {"parallel": [], "concurrent": []},
        "md5": {"parallel": [], "concurrent": []}
    }

    for size in sizes:
        filename = create_test_file(size)
        print(f"Testing with file size: {size} MB")

        for algo in ["blake", "sha256", "md5"]:
            parallel_func = globals()[f"{algo}_file_parallel"]
            concurrent_func = globals()[f"{algo}_file_concurrent"]

            parallel_time, _ = measure_time(parallel_func, filename)
            concurrent_time, _ = measure_time(concurrent_func, filename)

            results[algo]["parallel"].append(parallel_time)
            results[algo]["concurrent"].append(concurrent_time)

            print(f"{algo.upper()} - Parallel: {parallel_time:.4f}s, Concurrent: {concurrent_time:.4f}s")

        os.remove(filename)

    return results

def plot_results(sizes, results):
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    algorithms = ["blake", "sha256", "md5"]

    for i, algo in enumerate(algorithms):
        axs[i].plot(sizes, results[algo]["parallel"], label="Parallel", marker='o')
        axs[i].plot(sizes, results[algo]["concurrent"], label="Concurrent", marker='s')
        axs[i].set_xlabel("File Size (MB)")
        axs[i].set_ylabel("Time (seconds)")
        axs[i].set_title(f"{algo.upper()} Hash Performance")
        axs[i].legend()
        axs[i].grid(True)

    plt.tight_layout()
    plt.savefig("hash_performance_comparison.png")
    plt.close()

if __name__ == "__main__":
    sizes = [1, 5, 10, 50, 100]  # File sizes in MB
    results = run_tests(sizes)
    plot_results(sizes, results)
    print("Results have been plotted and saved as 'hash_performance_comparison.png'")