import keyring
from keyring.errors import NoKeyringError, InitError, PasswordSetError, KeyringLocked

from tq42.utils import file_handling


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
