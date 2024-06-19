import importlib
import json
from typing import Union
import keyring

from com.terraquantum.experiment.v3alpha1.experimentrun import (
    create_experiment_run_request_pb2 as create_exp_run,
)
from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    HardwareProto,
)
from com.terraquantum.experiment.v1.experimentrun.algorithm import shared_pb2

import tq42.utils.dirs as dirs
from tq42.utils import file_handling
from tq42.exceptions import NoMatchingAttributeError
from keyring.errors import NoKeyringError, InitError, PasswordSetError, KeyringLocked


def get_id(input):
    input = str(input)
    inputs = input.strip().splitlines()
    for input in inputs:
        pair_result = input.split(":")
        if len(pair_result) > 1 and pair_result[0] == "id":
            return pair_result[1].strip()

    return ""


def get_hw_configurations():
    hardware_configs_file_path = dirs.full_path(
        dirs.text_files_dir(), "hardware_configs.json"
    )
    with open(hardware_configs_file_path, "r") as json_file:
        loaded_data = json.load(json_file)
        return loaded_data


def get_hardware_num(name: Union[int, str]) -> int:
    try:
        if isinstance(name, str):
            return getattr(HardwareProto, name.upper())
        if isinstance(name, int):
            # TODO: we need to validate this is in range of the numbers we have in the enums
            return name
    except AttributeError:
        raise NoMatchingAttributeError("There is no hardware type {}".format(name))


def get_algo_num(name: Union[int, str]) -> int:
    try:
        if isinstance(name, str):
            return getattr(shared_pb2.AlgorithmProto, name.upper())
        if isinstance(name, int):
            # TODO: we need to validate this is in range of the numbers we have in the enums
            return name
    except AttributeError:
        raise NoMatchingAttributeError("There is no algorithm type {}".format(name))


def find_oneof_field_name(msg_type: str) -> str:
    """
    For the ExperimentRun we need to find out which field name matches our message type.
    This function looks for the matching oneof field in the CreateExperimentRunRequest protobuf message.
    """
    for oneof_field in create_exp_run.CreateExperimentRunRequest.DESCRIPTOR.oneofs:
        if oneof_field.name == "metadata":
            for field in oneof_field.fields:
                if field.message_type.name == msg_type:
                    return field.name


def dynamic_create_exp_run_request(
    parameters: dict, algo: int, exp_id: str, hardware: int
) -> create_exp_run.CreateExperimentRunRequest:
    """
    Dynamically creates a CreateExpRunRequest using the mapping provided as custom options of the AlgorithmProto enum.
    Tries dynamic import of this type and parses the parameters.
    """
    in_type = (
        shared_pb2.AlgorithmProto.DESCRIPTOR.values_by_number[algo]
        .GetOptions()
        .Extensions[shared_pb2.in_type]
    )
    path, msg_type = in_type.split(":")
    path = path.replace(".proto", "_pb2")
    path = path.replace("/", ".")
    module = importlib.import_module(path)

    # try parsing locally to reduce errors when communicating with the API
    try:
        getattr(module, msg_type)(**parameters)
    except Exception as e:
        raise NoMatchingAttributeError(str(e))

    # if parsing worked pass the params with the corresponding field name dynamically as keyword arguments
    field_name = find_oneof_field_name(msg_type=msg_type)
    keyword_args = {field_name: parameters}

    experiment_request = create_exp_run.CreateExperimentRunRequest(
        algorithm=algo,
        experiment_id=exp_id,
        hardware=hardware,
        **keyword_args,
    )
    return experiment_request


def save_token(service_name: str, backup_save_path: str, token: str) -> str:
    try:
        save_location = "keyring"
        keyring.set_password(
            service_name=service_name,
            username="username",
            password=token,
        )
        return save_location

    except (NoKeyringError, InitError, PasswordSetError):
        file_handling.write_to_file(backup_save_path, token)
        return backup_save_path


def get_token(service_name: str, backup_save_path: str) -> str:
    try:
        return keyring.get_password(
            service_name=service_name,
            username="username",
        )

    except (NoKeyringError, InitError, KeyringLocked):
        return file_handling.read_file(backup_save_path)
