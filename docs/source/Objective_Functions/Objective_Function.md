# Creating an Objective Function for TQ42

An objective function serves as a foundational component for optimization algorithms, guiding the computation towards an optimal solution. It is a precise mathematical expression defining the criteria for the "best" outcome, which could include minimizing costs, maximizing revenue, finding the most efficient route, or other objectives. In cases of multi-objective optimization([1]), additional functions are added to accommodate several objectives simultaneously, balancing trade-offs and providing a set of optimal solutions known as the Pareto front.([2]) This approach allows the algorithm to evaluate potential solutions against a spectrum of criteria and converge on the one that best satisfies the composite set of predefined goals.

[1]: https://www.egr.msu.edu/~kdeb/papers/k2011003.pdf
[2]: https://en.wikipedia.org/wiki/Pareto_front

### Objective Function Format
A TQ42 optimization algorithm must be provided with one or more real-valued functions to be optimized. The objective function(s) must be provided in the format of an endpoint accessible through https.

The endpoint will have two API calls:
1. `eval`
2. `task_status`

## 1. `eval` API Call
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

```python
{
  "task_id": "f5611b6e-4d1f-4247-b7de-252049efc2c9"
}
```


## 2. `task_status` API Call
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
`task_status` will return a status and possible result, such as:
```python
{
    "status": "SUCCESS",
    "result": {
        "x1": [
            1.0,
            2.1,
            3.4,
        ],
        "x2": [
            4.8,
            5.7,
            6.6,
        ],
        "y": [
            5.8,
            7.8,
            10.0,
        ]
    }   
}
```

The status field will include `FAILURE`,`PENDING`,`RECEIVED`,`RETRY`,`REVOKED`,`STARTED` or `SUCCESS`.

If the status is `SUCCESS` then it will also return the results, which is the data given to the `eval` API call extended by the evaluation.

## Example

Creating an objective function for TQ42 optimization algorithms requires that your solution be available online. So we recommend creating virtual machine in Google Cloud Platform or any cloud provider with your desired specifications. Install the desired operating system and enable http or https traffic. Any programming language can be used to interface with the TQ42 optimization algorithms. We recommend starting with python for simplicity.

Your exposed endpoint should satisfy these two functions.

#### Function 1: Task generation

```python
URL: http://[IP_ADDRESS]:8000/endpoint_name/eval
Example Argument:  {"x1":[10, 0.3, 9, 0.4], "x2":[4, 0.3, 9, 0.4]}
Sample Result: {"task_id": "017cdd63-be37-49e6-8463-0e8491349d8f"}
```

##### Description
This function takes a JSON object containing all parameters as keys as input and returns a UUID (Universal Unique Identifier) corresponding to that task.

##### Input
- JSON object containing all parameters as keys and arrays with int / floats as values. Make sure all parameter values have the same length.

##### Output
- `task_id`: A UUID string representing the task ID.

#### Function 2: Solution retrieval

```python
URL: http://[IP_ADDRESS]:8000/endpoint_name/task_status
Example Argument:  {"task_id": "017cdd63-be37-49e6-8463-0e8491349d8f"}
Sample Result:{"status": "SUCCESS","result": { "x1": [10, 0.3], "x2": [4, 0.3], "y": [0.19878316, 0.33940784] }}
```

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
