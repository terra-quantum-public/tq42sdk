import json
import os
import webbrowser
from datetime import datetime
import grpc
import requests
from tq42.utils import dirs, file_handling
from tq42.utils.token_manager import TokenManager
from tq42.exception_handling import handle_generic_sdk_errors
import time

from com.terraquantum.experiment.v1.experiment import (
    experiment_service_pb2_grpc as pb2_exp_grpc,
)
from com.terraquantum.experiment.v2.experimentrun import (
    experiment_run_service_pb2_grpc as pb2_exp_run_grpc,
)
from com.terraquantum.organization.v1.organization import (
    organization_service_pb2_grpc as pb2_org_grpc,
)
from com.terraquantum.project.v1.project import (
    project_service_pb2_grpc as pb2_proj_grpc,
)
from com.terraquantum.experiment.v1.dataset import (
    dataset_service_pb2_grpc as pb2_data_grpc,
)
from tq42.utils.environment_utils import environment_default_set


class ConfigEnvironment:
    """
    URLs determining environment
    """

    def __init__(self, base_url, client_id, scope):
        self.base_url = base_url
        self.client_id = client_id
        self.scope = scope

    @property
    def host(self):
        return "api.{}".format(self.base_url)

    @property
    def auth_url_token(self):
        return "https://auth.{}/oauth/token".format(self.base_url)

    @property
    def auth_url_code(self):
        return "https://auth.{}/oauth/device/code".format(self.base_url)

    @property
    def audience(self):
        return "https://graphql-gateway.{}/graphql".format(self.base_url)

    @property
    def headers(self):
        return {"Content-Type": "application/x-www-form-urlencoded"}

    @property
    def code_data(self):
        return {
            "client_id": self.client_id,
            "scope": self.scope,
            "audience": self.audience,
        }

    def token_data(self, device_code):
        return {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": device_code,
            "client_id": self.client_id,
        }

    def refresh_token_data(self, refresh_token):
        return {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
        }


class TQ42Client(object):
    """
    Visit tq42.com/help for more details on all commands.
    """

    def __call__(self, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __init__(self, alt_config_file=None):
        # check whether "alt_config_file" is the default filepath, if it is, token.json resides
        # in ~/.tqsdk/ and config.json inside utils/text_files/, if not using default,
        # config.json and token.json will reside in the same path
        # this happens when the user specifies a path during initialization of tq42 (usually for doing tests)

        self.default_config_file = dirs.text_files_dir("config.json")
        self.config_file = self.default_config_file
        self.config_folder = dirs.get_config_folder_path()

        if alt_config_file is not None and not self.is_config_filepath_default(
            alt_config_file
        ):
            self.config_file = alt_config_file
            self.config_folder = os.path.dirname(alt_config_file)

        with open(self.config_file, encoding="utf-8") as f:
            config_data = json.load(f)

        environment = ConfigEnvironment(
            config_data["base_url"], config_data["client_id"], config_data["scope"]
        )

        self.token_manager = TokenManager(environment, self.config_folder)

        self.environment = environment
        self.host = environment.host
        self.server_port = 443

        self.exp_run_id = None
        # instantiate a channel
        self.channel = grpc.secure_channel(self.host, grpc.ssl_channel_credentials())

        # bind the client and the server
        self.organization_client = pb2_org_grpc.OrganizationServiceStub(self.channel)
        self.project_client = pb2_proj_grpc.ProjectServiceStub(self.channel)
        self.experiment_client = pb2_exp_grpc.ExperimentServiceStub(self.channel)
        self.dataset_client = pb2_data_grpc.DatasetServiceStub(self.channel)
        self.experiment_run_client = pb2_exp_run_grpc.ExperimentRunServiceStub(
            self.channel
        )

    @handle_generic_sdk_errors
    def login(self):
        """
        This function will open a window in your browser where you must enter your TQ42 username and password to
        authenticate. To access TQ42 services with Python commands, you need a TQ42 account. When running TQ42 Python
        commands, your environment needs to have access to your TQ42 account credentials.

        For details, see
         https://terra-quantum-tq42sdk-docs.readthedocs-hosted.com/en/latest/README.html#authentication
        """
        # Send the POST request and print the response

        response = requests.post(
            self.environment.auth_url_code,
            data=self.environment.code_data,
            headers=self.environment.headers,
        )

        json_response = response.json()
        print(response.text)
        user_code = json_response["user_code"]
        device_code = json_response["device_code"]
        verification_uri_complete = json_response["verification_uri_complete"]
        interval = json_response["interval"]

        # Print the message to the user
        print(
            f"If a browser does not open, please access this URL: {verification_uri_complete} to login. Also check the code: {user_code}"
        )

        webbrowser.open(verification_uri_complete)

        data_token = self.environment.token_data(device_code)

        while True:
            # Send the POST request to get access token and extract the JSON response
            response_token = requests.post(
                self.environment.auth_url_token,
                data=data_token,
                headers=self.environment.headers,
            )
            json_token = response_token.json()
            # If we received an access token, print it and break out of the loop
            if "access_token" in json_token:
                access_token = json_token["access_token"]
                file_handling.write_to_file(self.token_file_path, access_token)
                print(
                    f"Authentication is successful, access token is saved in file: {self.token_file_path}"
                )
                env_set = environment_default_set(client=self)
                print(env_set)

            if "refresh_token" in json_token:
                refresh_token = json_token["refresh_token"]
                file_handling.write_to_file(self.refresh_token_file_path, refresh_token)
                current_datetime = datetime.now()
                file_handling.write_to_file(self.timestamp_file_path, current_datetime)
                break

            # Otherwise, wait for the specified interval before polling again
            time.sleep(interval)

    def is_config_filepath_default(self, config_file):
        return config_file == self.default_config_file

    @property
    def token_file_path(self):
        return self.token_manager.token_file_path

    @property
    def timestamp_file_path(self):
        return self.token_manager.timestamp_file_path

    @property
    def refresh_token_file_path(self):
        return self.token_manager.refresh_token_file_path

    @property
    def metadata(self):
        self.token_manager.renew_expring_token()
        token = file_handling.read_file(self.token_file_path)
        return (("authorization", "Bearer " + token),)
