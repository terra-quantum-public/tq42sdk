# Creating an Objective Function and Local Optimization Function for TQ42

An objective function serves as a foundational component for optimization algorithms, guiding the computation towards an optimal solution. It is a precise mathematical expression defining the criteria for the "best" outcome, which could include minimizing costs, maximizing revenue, finding the most efficient route, or other objectives. In cases of multi-objective optimization([1]), additional functions are added to accommodate several objectives simultaneously, balancing trade-offs and providing a set of optimal solutions known as the Pareto front.([2]) This approach allows the algorithm to evaluate potential solutions against a spectrum of criteria and converge on the one that best satisfies the composite set of predefined goals.

The TetraOpt algorithm can also optionally accept a local optimization function to refine optimization estimates. This is 
equivalent to running the TetraOpt optimization by itself, but following up each iteration with a second optimization 
algorithm. 

[1]: https://www.egr.msu.edu/~kdeb/papers/k2011003.pdf
[2]: https://en.wikipedia.org/wiki/Pareto_front

## Objective Function and Local Optimization Function Format
TQ42 optimizers require the usage of a communication channel for its objective and local optimization functions.
Please note that only TetraOpt may be configured with a local optimizer.

Below is an example of how to set up the TetraOpt parameter using a communication channel.
Notice the `objective_function_channel_id` and `local_optimizer_channel_id` parameters:


```python
from tq42.client import TQ42Client
from tq42.channel import Channel

with TQ42Client() as client:
    objective_func_channel = await Channel.create(client=client)
    local_opt_channel = await Channel.create(client=client)
    
    tetra_opt_parameter = {
        "dimensionality": 2,
        "iteration_number": 2,
        "maximal_rank": 4,
        "points_number": 1,
        "quantization": False,
        "tolerance": 0.0010000000474974513,
        "lower_limits": [0, 0],
        "upper_limits": [9, 9],
        "grid": [10, 10],
        "objective_function_channel_id": objective_func_channel.id,
        #local_optimizer_channel_id parameter is optional
        "local_optimizer_channel_id": local_opt_channel.id
    }
```

### 1. To use the communications channel:
TetraOpt uses the Ask and Tell pattern to send and receive information as objects to its objective and local optimization function. It also uses a communication channel to stream the information to and from the server.

1. `Ask` - TetraOpt sends an Ask object to the objective and local optimization function
2. `Tell` - The objective and local optimization function needs to respond with a Tell object to send information back to TetraOpt
3. `Channel`- This is used to connect the functions running locally to TetraOpt running in the cloud.


You can import these classes from the tq42 library by:

`from tq42.channel import Channel, Ask, Tell`


####  Below are the Python types for the Ask and Tell parameters you need to know:
  - `ask.headers` -> list of strings
  - `ask.parameter.values` -> list of floats
  - `tell.results` -> list of floats
  - `tell.candidates.values` -> list of floats


#### The `Ask` Class
An example of an `Ask` object values passed by TetraOpt:
```
{
    "parameters": [
        {"values": [1, 3]},
        {"values": [2, 7]}
    ],
    "headers": ["h0", "h1"]
}
```

#### The `Tell` Class 
An example of `Tell` object values for an objective and local optimization function:

Note:
1. You need an extra `candidates` parameter for the Tell object of the local optimization function:.
2. Before adding results to the `candidate` list, map them to a string called "values".
```
{
    "parameters": [
        {"values": [1, 3]},
        {"values": [2, 7]}
    ],
    "headers": ["h0", "h1"],
    "results": [6.59359884, 7.86938667],
    #parameter candidates is only used for local optimization function
    "candidates": [
        {"values": [0., 0.]},
        {"values": [-8.18565023e-09, -8.18565023e-09]},
        {"values": [5.02359648e-08, 5.02359648e-08]}, 
        {"values": [9., 9.]}
    ]
}
```

For a full working example, please refer to the notebooks section in the tq42sdk repo: https://github.com/terra-quantum-public/tq42sdk/tree/main/notebooks.
