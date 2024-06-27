# Creating an Objective Function and Local Optimization Function for TQ42

An objective function serves as a foundational component for optimization algorithms, guiding the computation towards an optimal solution. It is a precise mathematical expression defining the criteria for the "best" outcome, which could include minimizing costs, maximizing revenue, finding the most efficient route, or other objectives. In cases of multi-objective optimization([1]), additional functions are added to accommodate several objectives simultaneously, balancing trade-offs and providing a set of optimal solutions known as the Pareto front.([2]) This approach allows the algorithm to evaluate potential solutions against a spectrum of criteria and converge on the one that best satisfies the composite set of predefined goals.

The TetraOpt algorithm can also optionally accept a local optimization function to refine optimization estimates. This is 
equivalent to running the TetraOpt optimization by itself, but following up each iteration with a second optimization 
algorithm. 

[1]: https://www.egr.msu.edu/~kdeb/papers/k2011003.pdf
[2]: https://en.wikipedia.org/wiki/Pareto_front

## Objective Function and Local Optimization Function Format
TetraOpt requires one of the following methods of communication for its objective and local optimization functions:
1. A communication channel (using the tq42 API)
2. An https endpoint

### Example Using Communication Channel
Below is an example of how to set up the TetraOpt parameter using a communication channel. Notice the `objective_function_channel_id` and `local_optimizer_channel_id` parameters:


```
from tq42.channel import Ask, Tell
from tq42.client import TQ42Client

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
       "objective_function_channel_id": objective_func_channel.id
       #local_optimizer_channel_id parameter is optional
      "local_optimizer_channel_id": local_opt_channel.id
  }
```

### Example Using HTTPS Endpoint
Below is an example of how to set up the TetraOpt parameter using an HTTPS endpoint. Notice the `objective_function` and `local_optimizer` parameters:

```
from tq42.client import TQ42Client

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
    'objective_function':'http://34.32.169.11:8000/test_func_eval/Ackley/',
     #local_optimizer parameter is optional  
    "local_optimizer": "http://34.32.169.11:8000/local_optimization/Ackley/",
    "polling": {"initial_delay": 1.0, "retries": 100, "delay": 1.0, "backoff_factor": 1.1}
}
```

### 1. To use the communications channel:
TetraOpt uses the Ask and Tell pattern to send and receive information as objects to its objective and local optimization function. It also uses a communication channel to stream the information to and from the server.

1. `Ask` - TetraOpt sends an Ask object to the objective and local optimization function
2. `Tell` - The objective and local optimization function needs to respond witn a Tell object to send information back to TetraOpt
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


### 2. To use an https endpoint:
The endpoint will have two API calls:
1. `eval`
2. `task_status`

A local optimization function can be specified using endpoint with the same API calls and payloads as an objective 
function endpoint. The difference will be in the results of the `task_status` call, as explained later. 

#### 1. `eval` API Call
The TQ42 optimization algorithms use pandas data frames internally and the `eval` endpoint will receive a json string containing a dictionary which is transformable to a pandas data frame and vice versa. The keys of the dictionary are the columns of the data frame, which are also the names of the input variables. The `eval` endpoint uses the `POST` verb for HTTP to evaluate these candidate solutions and return the same dictionary extended with the objective(s) as new key(s), e.g.

URL of the eval API endpoint
```
url = 'https://api.example.com/eval'
```

`eval` will expect JSON payload in the format of (optimizing a function f: (x1,x2) -> y):
```python
data = {
    "x1": [
            1.0,
            2.1,
            3.4,
        ],
    "x2": [
            4.8,
            5.7,
            6.6,
        ]
}
```

Making the POST request
```python
response = requests.post(url, json=data)
```

The result of this API call will be a task id, such as:

```json
{
  "task_id": "f5611b6e-4d1f-4247-b7de-252049efc2c9"
}
```


#### 2. `task_status` API Call
This will check for the task status using the `POST` verb for HTTP. It will expect the same as input the output from the `eval` function call, e.g.

URL of the task_status API endpoint:
```python
url = 'https://api.example.com/task_status'
```

Data to be sent in the POST request:
```python
data = {
    "task_id": "f5611b6e-4d1f-4247-b7de-252049efc2c9"
}
```

Making the POST request:
```python
response = requests.post(url, json=data)
```

Response:
`task_status` for an objective function will return a status and possible result, such as:
```json
{
    "status": "SUCCESS",
    "result": {
        "x1": [
            1.0,
            2.1,
            3.4
        ],
        "x2": [
            4.8,
            5.7,
            6.6
        ],
        "y": [
            5.8,
            7.8
        ]
    }   
}
```

Here the values of `"y"`, `5.8` and `7.8` are the objective function evaluated at `"x1"` and `"x2"`.


The API results for a successful call to a local optimization function will have a similar structure, such as
```json
{
    "status": "SUCCESS",
    "result": {
        "x1": [
            1.0,
            2.1,
            3.4
        ],
        "x2": [
            4.8,
            5.7,
            6.6
        ],
        "y": [
            [5.8, [1.1, 2.0, 3.5]],
            [7.8, [4.9, 5.6, 6.5]]
        ]
    }   
}
```

Here the values of `"y"` represent local minimum close to the original points. For example, close to `"x1"`, there is a 
local minimum at `[1.1, 2.0, 3.5]` where the objective function takes value `5.8`.

The status field will include `FAILURE`,`PENDING`,`RECEIVED`,`RETRY`,`REVOKED`,`STARTED` or `SUCCESS`.

If the status is `SUCCESS` then it will also return the results, which is the data given to the `eval` API call extended by the evaluation.

### Example

Creating an objective function for TQ42 optimization algorithms requires that your solution be available online. So we recommend creating virtual machine in Google Cloud Platform or any cloud provider with your desired specifications. Install the desired operating system and enable http or https traffic. Any programming language can be used to interface with the TQ42 optimization algorithms. We recommend starting with python for simplicity.

Your exposed endpoint should satisfy these two functions.

#### Function 1: Task generation

- URL: `http://[IP_ADDRESS]:8000/endpoint_name/eval`
- Example Argument:  `{"x1":[10, 0.3, 9, 0.4], "x2":[4, 0.3, 9, 0.4]}`
- Sample Result: `{"task_id": "017cdd63-be37-49e6-8463-0e8491349d8f"}`

##### Description
This function takes a JSON object containing all parameters as keys as input and returns a UUID (Universal Unique Identifier) corresponding to that task.

##### Input
- JSON object containing all parameters as keys and arrays with int / floats as values. Make sure all parameter values have the same length.

##### Output
- `task_id`: A UUID string representing the task ID.

#### Function 2: Solution retrieval

- URL: `http://[IP_ADDRESS]:8000/endpoint_name/task_status`
- Example Argument: `{"task_id": "017cdd63-be37-49e6-8463-0e8491349d8f"}`
- Sample Result: `{"status": "SUCCESS","result": { "x1": [10, 0.3], "x2": [4, 0.3], "y": [0.19878316, 0.33940784] }}`

##### Description
This function takes a UUID and retrieves the task solution as a array of floating-point numbers. It provides a status update to indicate the progress of the task.

##### Input
- `task_id`: The UUID string identifying the optimization task.

##### Output
- `result`: The resulting array of float values, matching the dimensions of the original input array.
- `status`: A string indicating the status of the optimization task, which can be one of the following:  
  - `FAILURE` - Task failed.
  - `PENDING` - Task state is unknown (assumed pending since you know the id).
  - `RECEIVED` - Task was received by a worker (only used in events).
  - `RETRY` - Task is waiting for retry.
  - `REVOKED` - Task was revoked.
  - `STARTED` -  Task was started by a worker.
  - `SUCCESS` - Task succeeded.

##### Usage
The `status` output can be queried periodically to monitor the progress of the asynchronous task. This function is critical for scenarios where immediate execution is not possible, and the task is subject to processing time.