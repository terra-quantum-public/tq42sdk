from tq42.utils import dirs, file_handling, utils
from datetime import datetime
import requests


class TokenManager:
    def __init__(self, environment, alt_config_folder):
        self.alt_config_folder = alt_config_folder
        self.environment = environment

    @property
    def token_file_path(self):
        token_folder = dirs.create_or_get_config_dir(self.alt_config_folder)
        return dirs.full_path(token_folder, "token.json")

    @property
    def timestamp_file_path(self):
        token_folder = dirs.create_or_get_config_dir(self.alt_config_folder)
        return dirs.full_path(token_folder, "timestamp.json")

    @property
    def refresh_token_file_path(self):
        token_folder = dirs.create_or_get_config_dir(self.alt_config_folder)
        return dirs.full_path(token_folder, "refresh_token.json")

    def renew_expring_token(self):
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
        refresh_token = utils.get_token(
            service_name="refresh_token", backup_save_path=self.refresh_token_file_path
        )
        data = self.environment.refresh_token_data(refresh_token)
        response = requests.post(
            self.environment.auth_url_token,
            data=data,
            headers=self.environment.headers,
        )
        json_response = response.json()
        if "access_token" in json_response:
            access_token = json_response["access_token"]
            utils.save_token(
                service_name="access_token",
                backup_save_path=self.token_file_path,
                token=access_token,
            )
            current_datetime = datetime.now()
            file_handling.write_to_file(self.timestamp_file_path, current_datetime)
