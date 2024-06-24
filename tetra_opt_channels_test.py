import asyncio

from scipy import optimize

from tq42.channel import Channel, Ask, Tell
from tq42.client import TQ42Client
from tq42.algorithm import AlgorithmProto
from tq42.compute import HardwareProto
import numpy as np
import OptimizationTestFunctions as otf

from tq42.experiment_run import ExperimentRun


async def main():
    with TQ42Client() as client:
        channel = await Channel.create(client=client)
        print(channel)
        channel_local = await Channel.create(client=client)
        print(channel_local)

        tetra_opt_params = {
            "dimensionality": 2,
            "iteration_number": 2,
            "maximal_rank": 4,
            "points_number": 1,
            "quantization": False,
            "tolerance": 0.0010000000474974513,
            "lower_limits": [0, 0],
            "upper_limits": [9, 9],
            "grid": [10, 10],
             "objective_function_channel_id": channel.id,
            #"objective_function": "http://34.32.169.11:8000/test_func_eval/Ackley/",
            #"local_optimizer": "http://34.32.169.11:8000/local_optimization/Ackley/",
            "local_optimizer_channel_id": channel_local.id,
            "polling": {"initial_delay": 1.0, "retries": 100, "delay": 1.0, "backoff_factor": 1.1}
        }

        run = ExperimentRun.create(
            client=client,
            algorithm=AlgorithmProto.TETRA_OPT,
            experiment_id="0ba18e6f-65e6-4c0a-bda3-091c5a45312d",  # PROD
            compute=HardwareProto.SMALL,
            parameters={'parameters': tetra_opt_params, 'inputs': {}}
        )

        print(f"Experiment run id: {run.id}")

        async def objective_function_callback(ask: Ask) -> Tell:
            print("obj func len(ask.headers): ", len(ask.headers))
            dim = len(ask.headers)
            func = otf.Ackley(dim)
            y = []
            for parameter in ask.parameters:
                print("obj func ask parameter: ", parameter.values)
                y.append(float(func(np.array(parameter.values))))
            # add result to data

            tell = Tell(
                parameters=ask.parameters,
                headers=ask.headers,
                results=y
            )
            print("obj func tell: ", tell)
            return tell

        async def local_optimization_function_callback(ask: Ask) -> Tell:
            print("local opt len(ask.headers): ", len(ask.headers))
            dim = len(ask.headers)
            func = otf.Ackley(dim)
            y = []
            new_x = []
            print("local opt ask: ", ask)
            print("local opt ask.parameters: ", ask.parameters)
            for parameter in ask.parameters:
                print("local opt ask parameter: ", parameter)
                res = optimize.minimize(func, np.array(parameter.values))
                print("res.x: ", res.x)
                new_x.append({"values": res.x})
                print("res.fun: ", res.fun)
                y.append(float(res.fun))

            tell = Tell(
                parameters=ask.parameters,
                headers=ask.headers,
                results=y,
                candidates=new_x
            )
            print("local opt tell: ", tell)
            return tell

        def success():
            print("Experiment done!")

        await asyncio.gather(
            channel.connect(
                 callback=objective_function_callback, finish_callback=success, max_duration_in_sec=None, message_timeout_in_sec=500
            ),
            channel_local.connect(
                callback=local_optimization_function_callback, finish_callback=success, max_duration_in_sec=None, message_timeout_in_sec=500
            )
        )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        main()
    )