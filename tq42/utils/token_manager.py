import os

from tq42.utils import file_handling
from tq42.utils.environment import ConfigEnvironment
from tq42.utils.misc import get_token, save_token
from datetime import datetime
import requests

_REFRESH_TOKEN_KEY = "tq42_refresh_token"


class TokenManager:
    def __init__(self, environment: ConfigEnvironment):
        self._config_dir = os.path.expanduser("~/.config/tq42")
        self._environment = environment

        if not os.path.exists(self._config_dir):
            os.makedirs(self._config_dir)

    @property
    def token_file_path(self):
        return os.path.join(self._config_dir, "token")

    @property
    def timestamp_file_path(self):
        return os.path.join(self._config_dir, "timestamp")

    @property
    def refresh_token_file_path(self):
        return os.path.join(self._config_dir, "refresh_token")

    def renew_expiring_token(self):
        token_timestamp = file_handling.read_file(self.timestamp_file_path)
        if token_timestamp == "":
            return False
        token_timestamp = datetime.strptime(token_timestamp, "%Y-%m-%d %H:%M:%S.%f")
        diff = datetime.now() - token_timestamp
        # get new access token if token timestamp more than 23 hours(82800 seconds)
        # refresh token is valid for 30 days
        renew_limit = 82800
        if diff.total_seconds() > renew_limit:
            self.request_new_access_token()
            return True

        return False

    def request_new_access_token(self):
        refresh_token = get_token(
            service_name=_REFRESH_TOKEN_KEY,
            backup_save_path=self.refresh_token_file_path,
        )
        data = self._environment.refresh_token_data(refresh_token)
        response = requests.post(
            self._environment.auth_url_token,
            data=data,
            headers=self._environment.headers,
        )
        json_response = response.json()
        if "access_token" in json_response:
            access_token = json_response["access_token"]
            save_token(
                service_name="tq42_access_token",
                backup_save_path=self.token_file_path,
                token=access_token,
            )
            current_datetime = datetime.now()
            file_handling.write_to_file(self.timestamp_file_path, current_datetime)
