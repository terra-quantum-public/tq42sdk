import json
import os
import webbrowser
from datetime import datetime

import grpc
from grpc import aio
import requests

from tq42.utils import file_handling, misc
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

from tq42.utils.environment import ConfigEnvironment, environment_default_set
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

    def __init__(self):
        self._environment = ConfigEnvironment.from_env()
        self._token_manager = TokenManager(self._environment)

        self.server_port = 443

        # instantiate a channel
        self._api_channel = grpc.secure_channel(
            self._environment.api_host,
            grpc.ssl_channel_credentials(),
            options=[
                ("grpc.max_receive_message_length", 10_000_000),
                ("grpc.enable_retries", 1),
                ("grpc.service_config", json.dumps(_service_config)),
            ],
        )
        self.channels_channel = aio.secure_channel(
            self._environment.channels_host, grpc.ssl_channel_credentials()
        )

        # bind the client and the server
        self.organization_client = pb2_org_grpc.OrganizationServiceStub(
            self._api_channel
        )
        self.project_client = pb2_proj_grpc.ProjectServiceStub(self._api_channel)
        self.experiment_client = pb2_exp_grpc.ExperimentServiceStub(self._api_channel)
        self.storage_client = pb2_data_grpc.StorageServiceStub(self._api_channel)
        self.experiment_run_client = pb2_exp_run_grpc.ExperimentRunServiceStub(
            self._api_channel
        )
        self.plan_client = pb2_plan_grpc.PlanServiceStub(self._api_channel)
        self.channel_client = pb2_channel_grpc.ChannelServiceStub(self.channels_channel)

    @handle_generic_sdk_errors
    def login(self):
        """
        Trigger authentication flow. This opens a new browser window to authenticate the sdk.

        If the environment variables `TQ42_AUTH_CLIENT_ID` and `TQ42_AUTH_CLIENT_SECRET` are set the flow is performed without user interaction.
        """
        credential_flow_client_id = os.getenv("TQ42_AUTH_CLIENT_ID")
        credential_flow_client_secret = os.getenv("TQ42_AUTH_CLIENT_SECRET")

        if credential_flow_client_id and credential_flow_client_secret:
            self._login_without_user_interaction(
                client_id=credential_flow_client_id,
                client_secret=credential_flow_client_secret,
            )
        else:
            self._login_with_user_interaction()

    @handle_generic_sdk_errors
    def _login_without_user_interaction(self, client_id: str, client_secret: str):
        response = requests.post(
            self._environment.auth_url_token,
            data=self._environment.client_credentials_data(
                client_id=client_id,
                client_secret=client_secret,
                audience=self._environment.client_credential_flow_audience,
            ),
            headers=self._environment.headers,
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
            self._environment.auth_url_code,
            data=self._environment.code_data,
            headers=self._environment.headers,
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

        data_token = self._environment.token_data(device_code)

        while True:
            # Send the POST request to get access token and extract the JSON response
            response_token = requests.post(
                self._environment.auth_url_token,
                data=data_token,
                headers=self._environment.headers,
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

    @property
    def _token_file_path(self):
        return self._token_manager.token_file_path

    @property
    def _timestamp_file_path(self):
        return self._token_manager.timestamp_file_path

    @property
    def _refresh_token_file_path(self):
        return self._token_manager.refresh_token_file_path

    @property
    def metadata(self):
        """
        :meta private:
        """

        self._token_manager.renew_expiring_token()
        token = misc.get_token(
            service_name="tq42_access_token", backup_save_path=self._token_file_path
        )
        return (("authorization", "Bearer " + token),)
