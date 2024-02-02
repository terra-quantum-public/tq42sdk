# Introduction

## Overview of Machine Learning Algorithms
Whether you are new to machine learning, looking to solve a complex business problem, or you are a machine learning or quantum scientist, the TQml functionality in TQ42 puts sophisticated capabilities directly into your hands. Our machine learning features are powered by TQnet, the library for creating quantum neural networks, which include both classical and quantum layers.

Hybrid quantum neural networks can capture the performance metrics of either classical neural networks (by minimizing the quantum components) or quantum neural networks (by minimizing the classical components). Genuinely hybrid systems are still being actively explored and researched to find out how to get the very best of both worlds.

With TQnet, you can train machine learning models using pre-defined model architectures or custom model architectures.

### Pre-Defined Model Architectures
Pre-defined model architectures consist of layers chosen and proven by Terra Quantum to be performant for a specific use case. These models include pre-defined hyperparameters, which can be tuned if desired. To use a pre-defined model:
1. Prepare a training dataset that matches the template. Templates for different use cases can be found on the TQ42 web interface under Projects > Datasets.
2. Connect your dataset to the appropriate project.
3. Train your model using the pre-defined architecture of your choice, with the option to tune the default hyperparameters.
4. Evaluate the model on prediction and loss metrics (for time series prediction problems).
5. Apply the trained model to an unlabeled dataset.

### Custom Model Architectures
Custom model architectures can be built by constructing different stacks of layers to find the best compilation for your model. To build a custom model:
1. Prepare a training dataset.
2. Connect your dataset to the appropriate project and define your input and output columns.
3. Learn about the different classical, hybrid, and quantum layers available in TQnet.
4. Construct your layers as desired, defining hyperparameters for each.
5. Train your model using the custom architecture.
6. Evaluate the model on prediction and loss metrics (for time series prediction problems).
7. Apply the trained model to an unlabeled dataset.

## TQnet Layers
TQnet includes classical, hybrid, and quantum layers, which are built into the pre-defined model architectures or can be used to build custom model architectures. You can find more information about each under Model Architectures & Parameters > Custom Model Architectures > Available Layers.

### Classical Layers
1. Classical Dense Layer
2. Classical Long Short-Term Memory (LSTM) Layer
3. Dropout Layer
4. Batch Normalization Layer

### Hybrid Quantum Layers
1. Parallel Hybrid Network (PHN) Layer
2. Custom Parallel Hybrid Network (CPHN) Layer
3. Double Hybrid Network (DHN) Layer
4. Quantum Long Short-Term Memory (QLSTM) Layer

### Quantum Layers
1. Quantum Depth Infused (QDI) Layer
2. Parallel Quantum Network (PQN) Layer
3. Exponential Fourier Quantum Layer (EFQ) Layer
4. Custom Quantum (CQ) Layer
