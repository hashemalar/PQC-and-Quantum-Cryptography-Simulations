# Post-Quantum Cryptography Simulation

Evaluating the performance of classical and post-quantum cryptography algorithms in light of emerging threats from quantum computing.

## Overview

This project compares the RSA-2048 algorithm with the ML-KEM-768 algorithm.

**RSA-2048** is named after its inventors (Rivest, Shamir, and Adleman). It's a classic public-key algorithm based on a simple but powerful idea: it's easy to multiply two large prime numbers together, but extremely hard to do the reverse. If you take two prime numbers, P and q, and multiply them, you get a huge number N. Anyone can do that multiplication in an instant. But if you only have N and try to figure out which two primes were multiplied to get it, there's no fast way to do that — even for a computer. N becomes the public key (the part visible to everyone), while P and q stay private and are used to decrypt. This is what makes RSA secure today. The problem is that quantum computers, using Shor's algorithm, can solve this kind of problem extremely fast, which breaks RSA's security.

**ML-KEM-768** (formerly known as Kyber) is a post-quantum key encapsulation mechanism standardized by NIST. Instead of relying on prime numbers, it's built on a different hard problem called LWE (Learning With Errors). Picture a grid of points in space, like graph paper, where some points are "correct" intersections and others aren't. The algorithm takes a correct point and adds a small amount of random noise to it, just enough to push it slightly off the grid. The result looks almost like the original point, but not quite. Without knowing the structure of the grid (the private key), there's no efficient way to tell which "real" point the noisy one came from. That small bit of noise is what makes the math hard to reverse, and it's also why this approach is believed to resist quantum attacks.

The goal of this project is to actually measure these differences, not just describe them. Using open-source libraries, the script benchmarks both algorithms and records real performance numbers.

## Metrics

- Key generation time
- Encryption / Encapsulation time
- Decryption / Decapsulation time
- Public key size

## Technologies Used

- Python 3.10
- `pycryptodome` for RSA
- `pqcrypto` for ML-KEM (NIST PQC standard)
- `matplotlib` for visualizing the results

## Project Status

Under development. This is part of an ongoing research project on post-quantum cryptography. More algorithms, analysis, and a full research paper are planned next.

## How to Run


pip install pycryptodome pqcrypto matplotlib
python compare_rsa_mlkem.py
```

The script produces:
- A comparison table in the terminal
- `benchmark_results.csv` with the raw results
- `benchmark_chart.png` with a visual comparison

## Background

Classical public-key algorithms like RSA rely on the difficulty of factoring large numbers. Shor's algorithm, run on a sufficiently powerful quantum computer, threatens to break that security model. NIST responded by standardizing a new generation of post-quantum algorithms, including ML-KEM, designed to resist quantum attacks while still running efficiently on today's hardware.

## Author

Hashem Al-Araeed — Computer Science student aiming to work as a SOC Analyst. Interested in the intersection of cybersecurity and quantum computing.