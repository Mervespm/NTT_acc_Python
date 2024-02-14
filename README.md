# Python-Based Performance-Optimized Number Theoretic Transform (NTT) for Post-Quantum Cryptography (PQC)
This repository presents a Python implementation of the Number Theoretic Transform (NTT), a crucial operation in Post-Quantum Cryptography (PQC) schemes, particularly in lattice-based cryptosystems. The efficient implementation of NTT is essential for the practicality of these systems. Our solution leverages the just-in-time compilation capabilities of Numba and optimizes the control flow of the NTT operation to exploit parallelism in modern CPUs.

## Key Features
Utilizes modern processor features such as Single Instruction Multiple Data (SIMD), multi-core, multi-thread, and cache memory.
Demonstrates usability beyond Internet of Things (IoT) devices, extending PQC implementation to Python-based applications like face recognition algorithms and digital health data management.
Achieves significant performance improvements over official C implementations, with results showcasing up to 138.83× enhancement on an Intel Core i7-8700 CPU.
### Usage
To use our implementation, follow these steps:

Clone this repository to your local machine.
Install the necessary dependencies, including Numba.
Run the provided Python scripts or integrate the NTT implementation into your Python-based applications.

## Contributing
We welcome contributions to further enhance the performance and functionality of our Python-based NTT implementation. Feel free to submit pull requests or open issues for discussion.

## License
This project is licensed under the MIT License.

## Acknowledgments
We would like to acknowledge the support and guidance received during the development of this implementation.

By leveraging modern processor features and Python's flexibility, our implementation paves the way for efficient and versatile PQC schemes in various applications and environments.
