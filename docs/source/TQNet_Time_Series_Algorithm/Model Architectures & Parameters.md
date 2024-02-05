# Model Architectures & Parameters

## Pre-Defined Model Architectures

### Classical Models

#### Classical Multilayer Perceptron (MLP)

The Multilayer Perceptron (MLP) is a staple in the realm of artificial neural networks. This classical model is characterized by its layered structure, consisting of an input layer, one or more hidden layers, and an output layer. Each layer comprises numerous interconnected nodes or neurons, where the connections embody the weights that are adjusted during the learning process. MLPs utilize a feedforward architecture, meaning that data flows in one direction from input to output. They are well-suited for pattern recognition and regression tasks, making them a traditional choice for time series forecasting like predicting PV power output.

##### MLP Parameter Ranges and Descriptions:

###### For both training and evaluation:

- **input_width:** Integer (Default: 24) | Range: 1 to 72 | Defines the width or size of the input data, i.e., the number of hours for input.
- **label_width:** Integer (Default: 1) | Range: 1 to 72 | Specifies the width or size of the label data, i.e., the number of hours at the output of the model.
- **dim_list:** Integer (Default: [60, 40, 30]) | Range: 30 to 60 | The number of neurons or nodes in each hidden layer of the network.
- **act_func:** String (Default: 'ReLU') | Options: ['ReLU', 'LeakyReLU', 'Sigmoid'] | Activation function applied in the neural network.
- **dropout:** Boolean (Default: False) | Whether dropout regularization is used in the neural network or not.
- **dropout_p:** Float (Default: 0.2) | Range: 0 to 1 | The probability rate at which input units are dropped during training if dropout is enabled.
- **bn:** Boolean (Default: False) | Represents if batch normalization is applied or not.

###### Only for training:

- **num_epochs:** Integer (Default: 20) | Range: 5 to 50 | The number of epochs (iterations over the entire dataset) during training.
- **batch_size:** Integer (Default: 128) | Range: 16 to 512 | Specifies the size of data batches during training.
- **learning_rate:** Float (Default: 1e-3) | Range: 1e-4 to 1e-1 | The learning rate used during optimization.
- **optim:** String (Default: 'Adam') | Options: ['Adam', 'AdamW', 'SGD'] | The optimization algorithm used for training.
- **loss_func:** String (Default: 'MSE') | Options: ['MSE', 'MAE'] | The loss function used to evaluate the performance of the model.


#### Classical Long Short-Term Memory (LSTM)

The Long Short-Term Memory (LSTM) network is a type of recurrent neural network (RNN) specifically designed to remember information over extended periods. Unlike standard RNNs, LSTMs effectively combat the vanishing gradient problem, making them adept at learning from long sequences of data. An LSTM unit comprises three gates: the input gate, the forget gate, and the output gate. These gates regulate the flow of information, allowing the network to retain relevant data and discard irrelevant information. Classical LSTMs are particularly suitable for time series forecasting tasks, such as predicting PV power output, due to their ability to capture temporal dependencies and patterns over time.

##### LSTM Parameter Ranges and Descriptions:

###### For both training and evaluation:

- **input_width:** Integer (Default: 24) | Range: 1 to 72 | Defines the width or size of the input data, i.e., the number of hours for input.
- **label_width:** Integer (Default: 1) | Range: 1 to 72 | Specifies the width or size of the label data, i.e., the number of hours at the output of the model.
- **hidden_size:** Integer (Default: 17) | Range: 10 to 1000 | The size of the hidden layer in the neural network.
- **dropoutCoef:** Float (Default: 0.24) | Range: 0 to 1 | Percentage chance that a given neuron will be turned off during training

###### Only for training:

- **num_epochs:** Integer (Default: 20) | Range: 5 to 50 | The number of epochs (iterations over the entire dataset) during training.
- **batch_size:** Integer (Default: 128) | Range: 16 to 512 | Specifies the size of data batches during training.
- **learning_rate:** Float (Default: 1e-3) | Range: 1e-4 to 1e-1 | The learning rate used during optimization.
- **optim:** String (Default: 'Adam') | Options: ['Adam', 'AdamW', 'SGD'] | The optimization algorithm used for training.
- **loss_func:** String (Default: 'MSE') | Options: ['MSE', 'MAE'] | The loss function used to evaluate the performance of the model.

### Hybrid Quantum Models

#### Hybrid Quantum Multilayer Perceptron (HQMLP)

The Hybrid Quantum Multilayer Perceptron (HQMLP) represents an innovative leap from its classical counterpart. This model integrates one or more quantum layers within the standard MLP architecture. The quantum layers leverage the principles of quantum computing, employing qubits and quantum gates to process information. These layers can handle complex computations more efficiently and explore a broader solution space due to quantum superposition and entanglement. The hybrid nature of HQMLP allows it to harness both classical and quantum computational strengths, potentially offering enhanced predictive capabilities and efficiency in handling the nonlinear characteristics of PV power generation.

##### HQMLP Parameter Ranges and Descriptions:

###### For both training and evaluation:

- **input_width:** Integer (Default: 24) | Range: 1 to 72 | Defines the width or size of the input data, i.e., the number of hours for input.
- **label_width:** Integer (Default: 1) | Range: 1 to 72 | Specifies the width or size of the label data, i.e., the number of hours at the output of the model.
- **hidden_size:** Integer (Default: 17) | Range: 10 to 1000 | The size of the hidden layer in the neural network.
- **num_qubits:** Integer (Default: 8) | Range: 2 to 8 | The number of qubits used in the quantum circuit.
- **depth:** Integer (Default: 7) | Range: 1 to 8 | Represents the number of variational layers in the quantum circuit.
- **measurement_mode:** String (Default: 'none') | Options: ['even', 'single', 'none'] | Dictates how measurements are taken in the quantum circuit.*
- **rotation:** String (Default: 'X') | Options: ['X', 'Y', 'Z'] | The type of quantum embedding rotation applied on qubits.
- **entangling:** String (Default: 'basic') | Options: ['basic', 'strong'] | Describes the type of entanglement used.
- **measure:** String (Default: 'Z') | Options: ['X', 'Y', 'Z'] | Specifies the type of quantum measurement applied to qubits.
- **diff_method:** String (Default: 'adjoint') | Options: ['adjoint', 'parameter-shift'] | Differentiation method used.
- **qubit_type:** String (Default: 'lightning.qubit') | Options: ['lightning.qubit'] | Defines the type of qubit device used.
- **act_func:** String (Default: 'ReLU') | Options: ['ReLU', 'LeakyReLU', 'Sigmoid'] | Activation function applied in the neural network.
- **dropout:** Boolean (Default: False) | Whether dropout regularization is used in the neural network or not.
- **dropout_p:** Float (Default: 0.2) | Range: 0 to 1 | The probability rate at which input units are dropped during training if dropout is enabled.
- **bn:** Boolean (Default: False) | Represents if batch normalization is applied or not.

\* When measurement_mode is set to 'single', CNOTs would be applied at the end of the quantum circuit and reduce the whole output dimension to 1. If set to 'even' only (0,2,4,...) qubits in the quantum circuit will be measured. If set to 'none' each qubit will be measured.

###### Only for training:

- **num_epochs:** Integer (Default: 20) | Range: 5 to 50 | The number of epochs (iterations over the entire dataset) during training.
- **batch_size:** Integer (Default: 128) | Range: 16 to 512 | Specifies the size of data batches during training.
- **learning_rate:** Float (Default: 1e-3) | Range: 1e-4 to 1e-1 | The learning rate used during optimization.
- **optim:** String (Default: 'Adam') | Options: ['Adam', 'AdamW', 'SGD'] | The optimization algorithm used for training.
- **loss_func:** String (Default: 'MSE') | Options: ['MSE', 'MAE'] | The loss function used to evaluate the performance of the model.

#### Hybrid Quantum Long Short-Term Memory (HQLSTM)

The Hybrid Quantum Long Short-Term Memory (HQLSTM) is an advanced version of the classical LSTM, incorporating quantum layers into its structure. In HQLSTM, the quantum layers are embedded within the LSTM cells, enriching the model’s capability to process and remember information over time. By integrating quantum computing principles, the HQLSTM can achieve more complex and nuanced data representations. This hybrid approach combines the temporal learning prowess of LSTMs with the computational advantages of quantum layers, potentially leading to more accurate and efficient forecasts, especially in scenarios with intricate patterns and high data complexity.

##### HQLSTM Parameter Ranges and Descriptions:

###### For both training and evaluation:

- **input_width:** Integer (Default: 24) | Range: 1 to 72 | Defines the width or size of the input data, i.e., the number of hours for input.
- **label_width:** Integer (Default: 1) | Range: 1 to 72 | Specifies the width or size of the label data, i.e., the number of hours at the output of the model.
- **hidden_size:** Integer (Default: 17) | Range: 10 to 1000 | The size of the hidden layer in the neural network.
- **num_qubits:** Integer (Default: 8) | Range: 2 to 8 | The number of qubits used in the quantum circuit.
- **depth:** Integer (Default: 7) | Range: 1 to 8 | Represents the number of variational layers in the quantum circuit.
- **n_qlayers:** Integer (Default: 3) | Range: 1 to 5 | The number of quantum layers
- **dropoutCoef:** Float (Default: 0.24) | Range: 0 to 1 | Percentage chance that a given neuron will be turned off during training

###### Only for training:

- **num_epochs:** Integer (Default: 20) | Range: 5 to 50 | The number of epochs (iterations over the entire dataset) during training.
- **batch_size:** Integer (Default: 128) | Range: 16 to 512 | Specifies the size of data batches during training.
- **learning_rate:** Float (Default: 1e-3) | Range: 1e-4 to 1e-1 | The learning rate used during optimization.
- **optim:** String (Default: 'Adam') | Options: ['Adam', 'AdamW', 'SGD'] | The optimization algorithm used for training.
- **loss_func:** String (Default: 'MSE') | Options: ['MSE', 'MAE'] | The loss function used to evaluate the performance of the model.

## Custom Model Architectures

### Building a Custom Model with Layers
Build a custom model containing a mix of classical, hybrid, and quantum layers. Learn more about each layer below, and construct a custom model using any combination of layers you choose, defining hyperparameters for each.

Stay tuned for a sample code block and further instructions here soon.

### Available Layers