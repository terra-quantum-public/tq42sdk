import json

import keyring
from keyring.errors import NoKeyringError, InitError, PasswordSetError, KeyringLocked

import tq42.utils.dirs as dirs
from tq42.utils import file_handling


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
