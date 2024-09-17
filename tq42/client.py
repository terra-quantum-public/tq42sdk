import json
import os
import webbrowser
from datetime import datetime
import grpc
from grpc import aio
import requests
from tq42.utils import dirs, file_handling, misc
from tq42.utils.token_manager import TokenManager
from tq42.utils.exception_handling import handle_generic_sdk_errors
import time

from com.terraquantum.experiment.v3alpha1.experiment import (
    experiment_service_pb2_grpc as pb2_exp_grpc,
)
from com.terraquantum.experiment.v3alpha2.experimentrun import (
    experiment_run_service_pb2_grpc as pb2_exp_run_grpc,
)
from com.terraquantum.organization.v1.organization import (
    organization_service_pb2_grpc as pb2_org_grpc,
)
from com.terraquantum.project.v1.project import (
    project_service_pb2_grpc as pb2_proj_grpc,
)
from com.terraquantum.storage.v1alpha1 import (
    storage_service_pb2_grpc as pb2_data_grpc,
)
from com.terraquantum.channel.v1alpha1 import (
    channel_service_pb2_grpc as pb2_channel_grpc,
)
import com.terraquantum.plan.v1.plan.plan_service_pb2_grpc as pb2_plan_grpc
from tq42.utils.environment import environment_default_set
from tq42.exceptions import AuthenticationError

_service_config = {
    "methodConfig": [
        {
            "name": [
                {
                    "service": "com.terraquantum.channel.v1alpha1.ChannelService",
                    "method": "ConnectChannelCustomer",
                }
            ],
            "retryPolicy": {
                "maxAttempts": 5,
                "initialBackoff": "1s",
                "maxBackoff": "10s",
                "backoffMultiplier": 2,
                "retryableStatusCodes": ["UNAVAILABLE", "INTERNAL", "DATA_LOSS"],
            },
        }
    ]
}


class _ConfigEnvironment:
    """
    URLs determining environment
    """

    def __init__(self, base_url, client_id, scope):
        self.base_url = base_url
        self.client_id = client_id
        self.scope = scope

    @property
    def api_host(self):
        return "api.{}".format(self.base_url)

    @property
    def channels_host(self):
        return "channels.{}".format(self.base_url)

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
    def client_credential_flow_audience(self):
        return "https://api.{}".format(self.base_url)

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

    def client_credentials_data(self, client_id, client_secret, audience):
        return {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "audience": audience,
        }


class TQ42Client:
    """
    Create a new instance of the TQ42Client to pass to any resource

    Example:
        >>> from tq42.experiment import list_all
        ...
        ... with TQ42Client() as client:
        ...     print(list_all(client=client, project_id="some-project-id"))
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

        if alt_config_file is not None and not self._is_config_filepath_default(
            alt_config_file
        ):
            self.config_file = alt_config_file
            self.config_folder = os.path.dirname(alt_config_file)

        with open(self.config_file, encoding="utf-8") as f:
            config_data = json.load(f)

        environment = _ConfigEnvironment(
            config_data["base_url"], config_data["client_id"], config_data["scope"]
        )

        self.token_manager = TokenManager(environment, self.config_folder)

        self.environment = environment
        self.api_host = environment.api_host
        self.channels_host = environment.channels_host
        self.server_port = 443

        # instantiate a channel
        self.api_channel = grpc.secure_channel(
            self.api_host,
            grpc.ssl_channel_credentials(),
            options=[
                ("grpc.max_receive_message_length", 10_000_000),
                ("grpc.enable_retries", 1),
                ("grpc.service_config", json.dumps(_service_config)),
            ],
        )
        self.channels_channel = aio.secure_channel(
            self.channels_host, grpc.ssl_channel_credentials()
        )

        # bind the client and the server
        self.organization_client = pb2_org_grpc.OrganizationServiceStub(
            self.api_channel
        )
        self.project_client = pb2_proj_grpc.ProjectServiceStub(self.api_channel)
        self.experiment_client = pb2_exp_grpc.ExperimentServiceStub(self.api_channel)
        self.storage_client = pb2_data_grpc.StorageServiceStub(self.api_channel)
        self.experiment_run_client = pb2_exp_run_grpc.ExperimentRunServiceStub(
            self.api_channel
        )
        self.plan_client = pb2_plan_grpc.PlanServiceStub(self.api_channel)
        self.channel_client = pb2_channel_grpc.ChannelServiceStub(self.channels_channel)
        self.credential_flow_client_id = os.getenv("TQ42_AUTH_CLIENT_ID")
        self.credential_flow_client_secret = os.getenv("TQ42_AUTH_CLIENT_SECRET")

    @handle_generic_sdk_errors
    def login(self):
        """
        Trigger authentication flow. This opens a new browser window to authenticate the sdk.

        If the environment variables `TQ42_AUTH_CLIENT_ID` and `TQ42_AUTH_CLIENT_SECRET` are set the flow is performed without user interaction.
        """
        if self.credential_flow_client_id and self.credential_flow_client_secret:
            self._login_without_user_interaction()
        else:
            self._login_with_user_interaction()

    @handle_generic_sdk_errors
    def _login_without_user_interaction(self):
        response = requests.post(
            self.environment.auth_url_token,
            data=self.environment.client_credentials_data(
                client_id=self.credential_flow_client_id,
                client_secret=self.credential_flow_client_secret,
                audience=self.environment.client_credential_flow_audience,
            ),
            headers=self.environment.headers,
        )

        response_json = response.json()
        access_token = response_json.get("access_token")

        if not access_token:
            raise AuthenticationError()

        self._save_access_token(access_token)

    def _login_with_user_interaction(self):
        """
        This method will open a window in your browser where you must confirm the MFA code, then enter your TQ42
        username and password to authenticate. The authentication validity will keep extending as long as you are
        using it within a 30 day period. To access TQ42 services with Python commands, you need a TQ42 account.
        When running TQ42 Python commands, your environment needs to have access to your TQ42 account credentials.
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
            response_json = response_token.json()

            refresh_token = response_json.get("refresh_token")
            access_token = response_json.get("access_token")

            # If we received an access token, print it and break out of the loop
            if refresh_token and access_token:
                self._save_access_token(access_token)
                self._save_refresh_token(refresh_token)
                break

            # Otherwise, wait for the specified interval before polling again
            time.sleep(interval)

    def _save_access_token(self, access_token: str):
        save_location = misc.save_token(
            service_name="tq42_access_token",
            backup_save_path=self._token_file_path,
            token=access_token,
        )

        print(
            f"Authentication is successful, access token is saved in: {save_location}."
        )

        env_set = environment_default_set(client=self)
        print(env_set)

    def _save_refresh_token(self, refresh_token: str):
        misc.save_token(
            service_name="tq42_refresh_token",
            backup_save_path=self._refresh_token_file_path,
            token=refresh_token,
        )
        current_datetime = datetime.now()
        file_handling.write_to_file(self._timestamp_file_path, current_datetime)

    def _is_config_filepath_default(self, config_file):
        return config_file == self.default_config_file

    @property
    def _token_file_path(self):
        return self.token_manager.token_file_path

    @property
    def _timestamp_file_path(self):
        return self.token_manager.timestamp_file_path

    @property
    def _refresh_token_file_path(self):
        return self.token_manager.refresh_token_file_path

    @property
    def metadata(self):
        """
        :meta private:
        """

        self.token_manager.renew_expring_token()
        token = misc.get_token(
            service_name="tq42_access_token", backup_save_path=self._token_file_path
        )
        return (("authorization", "Bearer " + token),)
