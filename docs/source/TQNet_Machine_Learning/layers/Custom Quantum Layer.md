# Custom Quantum Layer
## Introduction to CQ

WIP - 3 sentence introduction text

# ANYA to get architecture, diagrams, reference from AR team's github pages. They should have published something there
# Update: no arxiv reference or achitecture diagram for CQ layer


## Key Benefits
- The main benefit of our custom quantum layer is that it __________.


## Hyperparameters and Default Settings
The following hyperparameters are included in the CQ layer. These are not necessarily the recommended settings for every application or use case; they may require tuning to find the optimal values for your specific use case.

| Hyperparameter | Description                                                                                                                                                           | Syntax           | Range                             | Default           |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|-----------------------------------|-------------------|
| n_qubits       | Number of qubits in each quantum circuit. <br/>For best results, formulate `n_qubits` as a power of 2.                                                                | int              | 2 to 8                            | 4                 |
| n_qubits       | Number of qubits each gate acts on. <br/>For best results, formulate `n_qubits` as a power of 2.                                                                      | int              | 2 to 8                            | 4                 |
| gates          | A list of quantum gates, where each gate has its own set of parameters. The choice and order of gates determines the quantum operations performed on the input data. Can be `Pauli`, `Hadamard` or `CNOT`. | list of objects |   --    |                   |


# 1-Qubit Gate Hyperparameters
| Hyperparameter | Description                                                                                                                                                                                                          | Syntax | Range    | Default  |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------|----------|
| variational    | Controls the number of iterations for the quantum algorithm used to train the quantum layer. The variational algorithm optimizes the quantum circuit parameters to minimize a cost function.                         | int    | 1 to 100 | 12       |
| encoding       | Specifies the encoding method used to represent classical data in the quantum circuit. Different encoding techniques may be suitable for different types of problems. Can be `method1`, `method2` or `method3`.      | int    | 1 to 3   | 2        |
| measurement    | The number of measurements to perform on the quantum circuit. The measurement process collapses the quantum state and projects it onto a classical outcome. More measurements may provide more accurate results but may also increase noise and uncertainty.  | int    | 1 to 100 | 10 |
 qubits in each circuit will be measured. If set to 'None' each qubit will be measured  | str    | 'single', 'even', 'None' | 'None' |
| wire           | Specifies which qubit(s) a particular gate should be applied to. Indicates the qubit index.                                                                                                                          | int   | [0, n_qubits-1] | 0 |

# 2-Qubit Gate Hyperparameters
| Hyperparameter | Description                                                                                                                                                                                                      | Syntax | Range    | Default  |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------|----------|
| variational    | Controls the number of iterations for the quantum algorithm used to train the quantum layer. The variational algorithm optimizes the quantum circuit parameters to minimize a cost function.                     | int    | 1 to 100 | 12       |
| encoding       | Specifies the encoding method used to represent classical data in the quantum circuit. Different encoding techniques may be suitable for different types of problems. Can be `method1`, `method2` or `method3`.  | int    | 1 to 3   | 2        |
| measurement    | The number of measurements to perform on the quantum circuit. The measurement process collapses the quantum state and projects it onto a classical outcome. More measurements may provide more accurate results but may also increase noise and uncertainty.  | int    | 1 to 100 | 10 |
| wire           | Specifies which qubit(s) a particular gate should be applied to. Indicates the indices of the two qubits.                                                                                                        | int    | [0, n_qubits-1] | 0 |

## UNCLEAR

1. 3 defitions for measurement?
| measurement    | The number of measurements to perform on the quantum circuit. The measurement process collapses the quantum state and projects it onto a classical outcome. More measurements may provide more accurate results but may also increase noise and uncertainty.  | int    | 1 to 100 | 10 |
| measurement    | type of CNOTs configuration before measurement. When set to 'single', CNOTs would be applied at the end of each circuit and reduce the whole output dimension by :math:`ext{n_qubits}` times. If set to 'even' only 
| measure        | Pauli measurement that will be used at the end of each circuit. Can be `X`, `Y` or `Z`.                                    | str    | `X` `Y` `Z`                       | `Y`               |

2. Should I add entangling, measure and rotation to qubit gate hyperparams?

## USE THESE DESCRIPTIONS FOR QUBIT GATE HYPERPARAMS
| Gate Parameter | Description                                                                                                                | Syntax | Range    | Default  |
| entangling     | Type of entangling layer used. Can be `strong` or `basic`.                                                                 | str    | `strong` `basic`                  | `strong`          |
| measure        | Pauli measurement that will be used at the end of each circuit. Can be `X`, `Y` or `Z`.                                    | str    | `X` `Y` `Z`                       | `Y`               |
| rotation       | ADD DETAILED EXPLANATION. Type of embedding rotations used. Can be `X`, `Y` or `Z`.                                        | str    | `X` `Y` `Z`                       | `Z`               |

## Quantum Circuit Representation
This circuit diagram reflects the default settings listed above, plus 12 input features. To visualize a dynamic graph, please use the TQ42 web interface.

![EFQ Circuit Diagram](../images/EFQ_Circuit_Diagram.png)

## Sample Python Code Block
# Sample code block from Domain Specs is wrong, but will be used as a placeholder

Here is an example of how to apply the CQ layer within a custom model architecture in the SDK.

The following example trains a custom time series prediction problem using a single EFQ layer:

```python
from tq42.client import TQ42Client

```
