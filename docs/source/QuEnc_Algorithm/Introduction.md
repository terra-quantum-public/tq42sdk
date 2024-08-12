# Introduction

The QuEnc (Quantum Encoding) algorithm is a gradient-based quantum algorithm designed to solve Quadratic Unconstrained Binary Optimization (QUBO) problems efficiently using a minimal number of qubits. It is particularly useful for large-scale optimization problems, such as the MaxCut problem, where the goal is to find an optimal solution by leveraging quantum computing's ability to handle complex probability distributions.

## Key Concepts
- **QUBO**: A mathematical problem where the objective is to minimize a quadratic function of binary variables. This function typically represents the "cost" or "energy" of different possible solutions.
- **Quantum Encoding**: QuEnc encodes the binary variables of a QUBO problem into quantum states using a logarithmic number of qubits, which allows for more efficient computation compared to traditional methods.
- **Hybrid Optimization**: QuEnc combines quantum computing for gradient evaluation and classical methods like ADAM for parameter optimization, making it a hybrid approach suitable for noisy intermediate-scale quantum (NISQ) devices.

The output of the QuEnc algorithm is a circuit which must then be run on a gate-based QPU or simulator. The number of 

[Reference](https://quantum-journal.org/papers/q-2023-11-21-1186/)
