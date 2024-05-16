# Introduction

QuEnc, short for Quantum Encoding, is a gradient-based optimization algorithm tailored for hardware-efficient quantum circuits utilizing amplitude encoding. This method addresses two critical challenges in quantum optimization: efficient training of circuits and incorporating constraints without resorting to penalty terms, as commonly done in classical and quantum annealing approaches. The key innovation of QuEnc lies in its ability to directly embed simple linear constraints into the circuit structure, streamlining the optimization process.

By leveraging numerical simulations and experimental validation on superconducting quantum processors, QuEnc has demonstrated its efficacy on solving MaxCut problems with thousands of nodes. Moreover, by combining QuEnc with classical solvers like CPLEX, the hybrid approach showcases superior performance in finding optimal solutions for unconstrained MaxCut instances, showcasing the potential of quantum algorithms to augment classical optimization techniques for enhanced efficiency and accuracy.

[Reference](https://quantum-journal.org/papers/q-2023-11-21-1186/)

# Circuit Formats and Libraries  
Quantum computing circuits are a graphical representation of quantum operations and their connectivity. They are essential for describing and programming quantum algorithms. Several circuit formats exist, each with its own advantages and limitations.  



Here's a table summarizing the libraries and their supported circuit formats:

| Library      | Supported Circuit Formats                               |
| ------------ | -------------------------------------------------------- |
| Pennylane    | Native Pennylane format, OpenQASM, TensorFlow Quantum's Cirq |
| OpenChasm    | OpenQASM                                                |
| Qiskit       | QASM (Quantum Assembly Language)                         |
| Cirq         | Native Cirq format, OpenQASM, TensorFlow Quantum's Cirq  |

Note: TQ42 currently support only Qiskit and Cirq for circuit creation and IBM and IONQ backends to run them.
