"""
RSA vs ML-KEM Performance Benchmark
-------------------------------------
This script compares classical RSA-2048 encryption against
NIST's post-quantum ML-KEM-768 algorithm.

We measure:
1. Key generation time
2. Encryption / Encapsulation time
3. Decryption / Decapsulation time
4. Key sizes

Results are saved to a CSV file and a comparison chart (PNG)
for use in reports or presentations.

Author: Hashem
"""

import time
import csv
import matplotlib.pyplot as plt
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from pqcrypto.kem.ml_kem_768 import generate_keypair, encrypt, decrypt

# Number of times we repeat each operation to get a reliable average
ITERATIONS = 100


def benchmark_rsa():
    """Benchmark RSA-2048 key generation, encryption, and decryption."""
    keygen_times = []
    encrypt_times = []
    decrypt_times = []

    for _ in range(ITERATIONS):
        # --- Key generation ---
        start = time.perf_counter()
        key = RSA.generate(2048)
        keygen_times.append(time.perf_counter() - start)

        cipher = PKCS1_OAEP.new(key.publickey())
        decipher = PKCS1_OAEP.new(key)

        message = b"Quantum-safe benchmark test message"

        # --- Encryption ---
        start = time.perf_counter()
        ciphertext = cipher.encrypt(message)
        encrypt_times.append(time.perf_counter() - start)

        # --- Decryption ---
        start = time.perf_counter()
        decipher.decrypt(ciphertext)
        decrypt_times.append(time.perf_counter() - start)

    public_key_size = len(key.publickey().export_key())

    return {
        "algorithm": "RSA-2048",
        "avg_keygen_ms": sum(keygen_times) / ITERATIONS * 1000,
        "avg_encrypt_ms": sum(encrypt_times) / ITERATIONS * 1000,
        "avg_decrypt_ms": sum(decrypt_times) / ITERATIONS * 1000,
        "public_key_bytes": public_key_size,
    }


def benchmark_mlkem():
    """Benchmark ML-KEM-768 key generation, encapsulation, and decapsulation."""
    keygen_times = []
    encrypt_times = []
    decrypt_times = []

    for _ in range(ITERATIONS):
        # --- Key generation ---
        start = time.perf_counter()
        public_key, secret_key = generate_keypair()
        keygen_times.append(time.perf_counter() - start)

        # --- Encapsulation (equivalent to "encryption" for a KEM) ---
        start = time.perf_counter()
        ciphertext, shared_secret = encrypt(public_key)
        encrypt_times.append(time.perf_counter() - start)

        # --- Decapsulation (equivalent to "decryption") ---
        start = time.perf_counter()
        decrypt(secret_key, ciphertext)
        decrypt_times.append(time.perf_counter() - start)

    return {
        "algorithm": "ML-KEM-768",
        "avg_keygen_ms": sum(keygen_times) / ITERATIONS * 1000,
        "avg_encrypt_ms": sum(encrypt_times) / ITERATIONS * 1000,
        "avg_decrypt_ms": sum(decrypt_times) / ITERATIONS * 1000,
        "public_key_bytes": len(public_key),
    }


def print_results(results):
    """Print a clean comparison table in the terminal."""
    print(f"\n{'Metric':<25}{'RSA-2048':<20}{'ML-KEM-768':<20}")
    print("-" * 65)
    print(f"{'Key generation (ms)':<25}{results[0]['avg_keygen_ms']:<20.4f}{results[1]['avg_keygen_ms']:<20.4f}")
    print(f"{'Encryption (ms)':<25}{results[0]['avg_encrypt_ms']:<20.4f}{results[1]['avg_encrypt_ms']:<20.4f}")
    print(f"{'Decryption (ms)':<25}{results[0]['avg_decrypt_ms']:<20.4f}{results[1]['avg_decrypt_ms']:<20.4f}")
    print(f"{'Public key size (bytes)':<25}{results[0]['public_key_bytes']:<20}{results[1]['public_key_bytes']:<20}")


def save_csv(results, filename="benchmark_results.csv"):
    """Save the benchmark results to a CSV file for documentation purposes."""
    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "RSA-2048", "ML-KEM-768"])
        writer.writerow(["Key generation (ms)", f"{results[0]['avg_keygen_ms']:.4f}", f"{results[1]['avg_keygen_ms']:.4f}"])
        writer.writerow(["Encryption (ms)", f"{results[0]['avg_encrypt_ms']:.4f}", f"{results[1]['avg_encrypt_ms']:.4f}"])
        writer.writerow(["Decryption (ms)", f"{results[0]['avg_decrypt_ms']:.4f}", f"{results[1]['avg_decrypt_ms']:.4f}"])
        writer.writerow(["Public key size (bytes)", results[0]['public_key_bytes'], results[1]['public_key_bytes']])
    print(f"\nResults saved to {filename}")


def plot_results(results, filename="benchmark_chart.png"):
    """Create a bar chart comparing RSA and ML-KEM across all metrics."""
    metrics = ["Key generation (ms)", "Encryption (ms)", "Decryption (ms)"]
    rsa_values = [results[0]['avg_keygen_ms'], results[0]['avg_encrypt_ms'], results[0]['avg_decrypt_ms']]
    mlkem_values = [results[1]['avg_keygen_ms'], results[1]['avg_encrypt_ms'], results[1]['avg_decrypt_ms']]

    x = range(len(metrics))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.bar([i - width / 2 for i in x], rsa_values, width, label="RSA-2048")
    ax.bar([i + width / 2 for i in x], mlkem_values, width, label="ML-KEM-768")

    ax.set_ylabel("Time (milliseconds, log scale)")
    ax.set_yscale("log")  # log scale because RSA keygen is much slower than the rest
    ax.set_title("RSA-2048 vs ML-KEM-768 Performance Comparison")
    ax.set_xticks(list(x))
    ax.set_xticklabels(metrics)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"Chart saved to {filename}")


if __name__ == "__main__":
    print(f"Running benchmark with {ITERATIONS} iterations per algorithm...")
    print("This may take a moment for RSA key generation...\n")

    rsa_results = benchmark_rsa()
    mlkem_results = benchmark_mlkem()

    all_results = [rsa_results, mlkem_results]

    print_results(all_results)
    save_csv(all_results)
    plot_results(all_results)