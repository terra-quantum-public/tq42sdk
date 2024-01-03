# Introduction

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
