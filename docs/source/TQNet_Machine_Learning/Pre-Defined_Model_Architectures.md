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
- **time_column:** String (Default: 'Time') | The time column for the specific dataset.

###### Only for training:

- **num_epochs:** Integer (Default: 20) | Range: 5 to 50 | The number of epochs (iterations over the entire dataset) during training.
- **batch_size:** Integer (Default: 128) | Range: 16 to 512 | Specifies the size of data batches during training.
- **learning_rate:** Float (Default: 1e-3) | Range: 1e-4 to 1e-1 | The learning rate used during optimization.
- **optim:** String (Default: 'Adam') | Options: ['Adam', 'AdamW', 'SGD'] | The optimization algorithm used for training.
- **loss_func:** String (Default: 'MSE') | Options: ['MSE', 'MAE'] | The loss function used to evaluate the performance of the model.
- **target_column:** String (Default: 'Power, kW') | The target column that the model should learn for this specific dataset.

###### Example
```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun
from tq42.compute import HardwareProto
from tq42.algorithm import (
    AlgorithmProto, 
    OptimProto, 
    LossFuncProto, 
    DatasetStorageInfoProto, 
    MLTrainInputsProto,
    TSMLPTrainMetadataProto, 
    TSMLPTrainParametersProto,
    ActFuncProto
)
from google.protobuf.json_format import MessageToDict

with TQ42Client() as client:
    params = MessageToDict(TSMLPTrainMetadataProto(
        parameters=TSMLPTrainParametersProto(
            input_width=1,
            label_width=1,
            dim_list=[30, 45, 60],
            act_func=ActFuncProto.SIGMOID,
            dropout=True,
            dropout_p=0.5,
            bn=True,
            num_epochs=20,
            batch_size=32,
            learning_rate=0.001,
            loss_func=LossFuncProto.MAE,
            optim=OptimProto.ADAM,
            time_column="your_time_column",
            target_column="your_target_column"
        ),
        inputs=MLTrainInputsProto(data=DatasetStorageInfoProto(storage_id="your_storage_id"))), 
        preserving_proto_field_name=True)
                
    ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.TS_MLP_TRAIN,
        experiment_id="your_experiment_id",
        compute=HardwareProto.SMALL,
        parameters=params
    )
```

#### Classical Long Short-Term Memory (LSTM)

The Long Short-Term Memory (LSTM) network is a type of recurrent neural network (RNN) specifically designed to remember information over extended periods. Unlike standard RNNs, LSTMs effectively combat the vanishing gradient problem, making them adept at learning from long sequences of data. An LSTM unit comprises three gates: the input gate, the forget gate, and the output gate. These gates regulate the flow of information, allowing the network to retain relevant data and discard irrelevant information. Classical LSTMs are particularly suitable for time series forecasting tasks, such as predicting PV power output, due to their ability to capture temporal dependencies and patterns over time.

##### LSTM Parameter Ranges and Descriptions:

###### For both training and evaluation:

- **input_width:** Integer (Default: 24) | Range: 1 to 72 | Defines the width or size of the input data, i.e., the number of hours for input.
- **label_width:** Integer (Default: 1) | Range: 1 to 72 | Specifies the width or size of the label data, i.e., the number of hours at the output of the model.
- **hidden_size:** Integer (Default: 17) | Range: 10 to 1000 | The size of the hidden layer in the neural network.
- **dropoutCoef:** Float (Default: 0.24) | Range: 0 to 1 | Percentage chance that a given neuron will be turned off during training
- **time_column:** String (Default: 'Time') | The time column for the specific dataset.

###### Only for training:

- **num_epochs:** Integer (Default: 20) | Range: 5 to 50 | The number of epochs (iterations over the entire dataset) during training.
- **batch_size:** Integer (Default: 128) | Range: 16 to 512 | Specifies the size of data batches during training.
- **learning_rate:** Float (Default: 1e-3) | Range: 1e-4 to 1e-1 | The learning rate used during optimization.
- **optim:** String (Default: 'Adam') | Options: ['Adam', 'AdamW', 'SGD'] | The optimization algorithm used for training.
- **loss_func:** String (Default: 'MSE') | Options: ['MSE', 'MAE'] | The loss function used to evaluate the performance of the model.
- **target_column:** String (Default: 'Power, kW') | The target column that the model should learn.

###### Example
```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun
from tq42.compute import HardwareProto
from tq42.algorithm import (
    AlgorithmProto, 
    OptimProto, 
    LossFuncProto, 
    DatasetStorageInfoProto, 
    TSLSTMTrainMetadataProto, 
    TSLSTMTrainParametersProto,
    MLTrainInputsProto
)
from google.protobuf.json_format import MessageToDict

with TQ42Client() as client:
    params = MessageToDict(TSLSTMTrainMetadataProto(
        parameters=TSLSTMTrainParametersProto(
            input_width=20,
            label_width=1,
            hidden_size=5,
            dropout_coef=0.4,
            num_epochs=20,
            batch_size=32,
            learning_rate=0.001,
            optim=OptimProto.ADAM,
            loss_func=LossFuncProto.MAE
            ),
        inputs=MLTrainInputsProto(data=DatasetStorageInfoProto(storage_id="your_storage_id"))), 
        preserving_proto_field_name=True)
        
    ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.TS_LSTM_TRAIN,
        experiment_id="your_experiment_id",
        compute=HardwareProto.SMALL,
        parameters=params
    )
```

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
- **time_column:** String (Default: 'Time') | The time column for the specific dataset.

\* When measurement_mode is set to 'single', CNOTs would be applied at the end of the quantum circuit and reduce the whole output dimension to 1. If set to 'even' only (0,2,4,...) qubits in the quantum circuit will be measured. If set to 'none' each qubit will be measured.

###### Only for training:

- **num_epochs:** Integer (Default: 20) | Range: 5 to 50 | The number of epochs (iterations over the entire dataset) during training.
- **batch_size:** Integer (Default: 128) | Range: 16 to 512 | Specifies the size of data batches during training.
- **learning_rate:** Float (Default: 1e-3) | Range: 1e-4 to 1e-1 | The learning rate used during optimization.
- **optim:** String (Default: 'Adam') | Options: ['Adam', 'AdamW', 'SGD'] | The optimization algorithm used for training.
- **loss_func:** String (Default: 'MSE') | Options: ['MSE', 'MAE'] | The loss function used to evaluate the performance of the model.
- **target_column:** String (Default: 'Power, kW') | The target column that the model should learn.

###### Example
```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun
from tq42.compute import HardwareProto
from tq42.algorithm import (
    AlgorithmProto, 
    ActFuncProto,
    OptimProto, 
    LossFuncProto, 
    MeasurementModeProto,
    MeasureProto,
    EntanglingProto,
    DiffMethodProto,
    QubitTypeProto,
    DatasetStorageInfoProto, 
    MLTrainInputsProto,
    TSHQMLPTrainMetadataProto, 
    TSHQMLPTrainParametersProto
)
from google.protobuf.json_format import MessageToDict

with TQ42Client() as client:
    params = MessageToDict(TSHQMLPTrainMetadataProto(
        parameters=TSHQMLPTrainParametersProto(
            input_width=1,
            label_width=1,
            hidden_size=17,
            num_qubits=8,
            depth=7,
            measurement_mode=MeasurementModeProto.NONE,
            rotation=MeasureProto.X,
            entangling=EntanglingProto.BASIC,
            measure=MeasureProto.Z,
            diff_method=DiffMethodProto.ADJOINT,
            qubit_type=QubitTypeProto.LIGHTNING_QUBIT,
            act_func=ActFuncProto.SIGMOID,
            dropout=True,
            dropout_p=0.5,
            bn=False,
            num_epochs=20,
            batch_size=32,
            learning_rate=0.001,
            loss_func=LossFuncProto.MAE,
            optim=OptimProto.ADAM,
            time_column="your_time_column",
            target_column="your_target_column"
            ),
        inputs=MLTrainInputsProto(data=DatasetStorageInfoProto(storage_id="your_storage_id"))), 
        preserving_proto_field_name=True)
                
    ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.TS_HQMLP_TRAIN,
        experiment_id="your_experiment_id",
        compute=HardwareProto.SMALL,
        parameters=params
    )
```

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
- **time_column:** String (Default: 'Time') | The time column for the specific dataset.

###### Only for training:

- **num_epochs:** Integer (Default: 20) | Range: 5 to 50 | The number of epochs (iterations over the entire dataset) during training.
- **batch_size:** Integer (Default: 128) | Range: 16 to 512 | Specifies the size of data batches during training.
- **learning_rate:** Float (Default: 1e-3) | Range: 1e-4 to 1e-1 | The learning rate used during optimization.
- **optim:** String (Default: 'Adam') | Options: ['Adam', 'AdamW', 'SGD'] | The optimization algorithm used for training.
- **loss_func:** String (Default: 'MSE') | Options: ['MSE', 'MAE'] | The loss function used to evaluate the performance of the model.
- **target_column:** String (Default: 'Power, kW') | The target column that the model should learn.

###### Example
```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun
from tq42.compute import HardwareProto
from tq42.algorithm import (
    AlgorithmProto, 
    OptimProto, 
    LossFuncProto, 
    DatasetStorageInfoProto, 
    TSHQLSTMTrainMetadataProto, 
    TSHQLSTMTrainParametersProto,
    MLTrainInputsProto
)
from google.protobuf.json_format import MessageToDict

with TQ42Client() as client:
    params = MessageToDict(TSHQLSTMTrainMetadataProto(
        parameters=TSHQLSTMTrainParametersProto(
            input_width=20,
            label_width=1,
            hidden_size=5,
            dropout_coef=0.4,
            num_epochs=20,
            batch_size=32,
            learning_rate=0.001,
            depth=2,
            n_qlayers=2,
            num_qubits=2,
            optim=OptimProto.ADAM,
            loss_func=LossFuncProto.MAE
            ),
        inputs=MLTrainInputsProto(data=DatasetStorageInfoProto(storage_id="your_storage_id"))),
        preserving_proto_field_name=True)

    ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.TS_HQLSTM_TRAIN,
        experiment_id="your_experiment_id",
        compute=HardwareProto.SMALL,
        parameters=params
    )
```

### Loss functions  
A loss function is a function that compares the output values predicted by the network with the target values provided by the user.   
It estimates how well the neural network models the training data and during the training phase, the aim is to minimise the loss between the expected and predicted output values.  
In supervised learning, the loss functions are classified into two classes according to the type of learning task: regression and classification loss functions  

##### Regression
A regression loss function predicts a continuous quantity  

###### Mean Squared Error (MSE)  
The MSE measures the average square of the errors, namely the average difference between the target values and the predicted outputs.  

$$ \text{MSE}= \frac{1}{N}\sum_{i=1} ^{N} (y_i-\hat{y_i})^2 $$

where     
- $$ y=\text{Target Value} $$      
- $$ \hat{y}=\text{Predicted Output} $$  

It is sensitive to the outlier, which are the data point (i.e.: sample of the dataset) that stands out a lot from the other data points in a set  

###### Mean Absolute Error (MAE)
The MAE measures the average of the absolute differences between the target values and the predicted outputs.  

$$ \text{MAE}= \frac{1}{N}\sum_{i=1} ^{N} |y_i-\hat{y_i}| $$    
where     
- $$ y=\text{Target Value} $$      
- $$ \hat{y}=\text{Predicted Output} $$  

It is preferable to the MSE in cases where the training data have a large number of outliers to mitigate this problem, but in general terms the MAE is less preferable to the MSE  
because when the mean distance approaches 0, the optimisation of the gradient descent will not work, since the derivative of the function at 0 is undefined (which will lead to an error).  

##### Classification
A classification loss function predicts a label   

###### Binary Cross-Entropy (BCE)  
In general terms, cross entropy, or log loss, measures the performance of a classification model by calculating the difference between the probability distribution predicted by a classification model and the expected values.  

$$ \text{BCE Loss} = -\frac{1}{N}\sum_{i=1} ^{N} y_i\log(p(y_i))+(1-y_i)\log(1-p(y_i)) $$  
where   
- $$ p(y_i)=\text{Probability of True} $$      
- $$ 1-p(y_i)=\text{Probability of False} $$  

The BCE is used in binary classification models, where the model has to classify a given input into one of two predefined categories. It is the negative average of the log of corrected predicted probabilities.  
It compares the expected probability with the actual output of the class, which can be 0 or 1, and consequently calculates a score that penalises the probabilities according to their distance from the expected value.  

###### Categorical Cross-Entropy (CROSSENTROPY)
The Categorical Cross-Entropy is used in multi-class classification tasks with more than two mutually exclusive classes.  

$$ \text{CROSSENTROPY Loss} = -\sum_{c=1} ^{C}q(y_c)\log(p(y_c) $$    
where   
- $$ p(y)=\text{True Probability Distribution} $$    
- $$ q(y)=\text{Predicted Probability Distribution} $$    

Similarly to the binary, this type of cross-entropy loss function quantifies the dissimilarity between the predicted probabilities and the true categorical labels.  

### Metrics  
Metrics evaluate the model and depend on the model itself. Their choice influences how the performance of machine learning algorithms is measured and compared.    

#### Classification  
In classification problems, the model is evaluated by measuring the degree to which an estimated category corresponds to the actual category.
The following metrics refer to the binary case. Thus in the multiclass case they refer to a single class, so to obtain an overall measurement the user must calculate average values according to macro-averaging or micro-averaging formula

##### True Positive (tp)  
Cases where the classifier has associated an input with the correct class, so the input belongs to class A and the classifier has classified it as belonging to class A  

##### True Negative (tn)  
Cases where the classifier has correctly associated an input to not belonging to a certain class, so the input does not belong to class A and the classifier has classified it as not belonging to class A  

##### False Positive (fp)  
Cases where the classifier has wrongly associated an input with a class, so the input does not belong to class A and the classifier has classified it as belonging to class A.  

##### False Negative (fn)  
Cases in which the classifier has wrongly associated an input to not belonging to a certain class, so the input belongs to class A and the classifier has classified it as not belonging to class A.  

##### Confusion matrix  
The confusion matrix is not a metric in itself, but describes the complete performance of the model.  

|                   | Predicted Negative | Predicted Positive |
|-------------------|---------------------|---------------------|
| **Actual Negative** | tn                  | fp                  |
| **Actual Positive** | fn                  | tp                  |


##### Accuracy  
Accuracy is the ratio of number of correct predictions to the total number of input samples. It works well only if the class are balanced, which means that there are the same number of samples in each class.  

$$ \text{Accuracy} = \frac{t_p+t_n}{t_p+t_n+f_p+f_n} $$  

##### Precision  
Precision is the number of correct positive results divided by the number of positive results predicted.  
It indicates how precise is the classifier, namely how many instances it classifies correctly  

$$ \text{Precision} = \frac{t_p}{t_p+f_p} $$  

##### Recall  
Recall,also called sensitivity, is the number of correct positive results divided by the number of all samples that should have been identified as positive.   
It indicates how robust is the classifier, namely it does not miss a significant number of instances  

$$ \text{Recall} = \frac{t_p}{t_p+f_n} $$  

##### Specificity  
Specificity is the number of predicted corrected negative results divided by the number of expected negative results  

$$ \text{Specificity} = \frac{t_n}{t_n+f_p} $$  

##### F1-score  
F1 Score is the Harmonic Mean between precision and recall and indicates how precise and robust the classifier is.  

$$ \text{F1} = 2*\frac{1}{\frac{1}{\text{precision}}+\frac{1}{\text{recall}}} $$  

#### Regression   
Regression models have a continuous output so the metrics are based on calculating some sort of distance between the prediction and the ground truth.  

#### Mean Squared Error  
The MSE indicates how to close a regression line to a set of test data values by taking the distances from the points to the regression line (these distances are the E errors) and squaring them.  

#### Mean Absolute Error (MAE)  
The MAE measures the closeness of estimates to actual results. It corresponds to the average of all model errors, where a model error is the distance between the estimated and correct label value.   
This estimation error is calculated for each element in the test data set. Finally, the mean value is calculated for all recorded absolute errors.
