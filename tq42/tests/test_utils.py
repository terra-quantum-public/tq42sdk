import json
import os
import unittest
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from unittest import mock

from keyring.errors import InitError, NoKeyringError, PasswordSetError, KeyringLocked

from tq42.client import _ConfigEnvironment, TQ42Client
from tq42.utils import dirs, file_handling
from tq42.utils.misc import (
    save_token,
    get_token,
)
from tq42.utils.token_manager import TokenManager


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.client = TQ42Client()

    @mock.patch("requests.post")
    def test_renew_expiring_token(self, post_mock):
        @dataclass
        class MockResponse:
            json_data: Any
            status_code: Any

            def json(self):
                return self.json_data

        data = {
            "access_token": "fake_access_token",
            "id_token": "fake_id_token",
            "scope": "fake_scopes",
            "expires_in": 86400,
            "token_type": "Bearer",
        }

        post_mock.return_value = MockResponse(json_data=data, status_code=200)

        token_timestamp = "2022-07-21 13:48:26.580403"
        token_timestamp = datetime.strptime(token_timestamp, "%Y-%m-%d %H:%M:%S.%f")
        # force expire timestamp
        file_handling.write_to_file(
            self.client._timestamp_file_path, str(token_timestamp)
        )

        # load config file
        alt_config_file = dirs.text_files_dir("config.json")
        with open(alt_config_file, encoding="utf-8") as f:
            config_data = json.load(f)

        environment = _ConfigEnvironment(
            config_data["base_url"],
            config_data["client_id"],
            config_data["scope"],
        )

        token_manager = TokenManager(environment, None)

        success = token_manager.renew_expring_token()
        # old token timestamp should renew token
        self.assertTrue(success)

        # renew should return false as timestamp has been updated already
        success = token_manager.renew_expring_token()
        # new token timestamp should NOT renew token
        self.assertFalse(success)

    def test_config_file_path(self):
        alternative_json_path = dirs.testdata("config.json")
        tq42 = TQ42Client(alternative_json_path)
        self.assertEqual(tq42.config_file, alternative_json_path)

    def test_save_get_token_with_keyring_enabled(self):
        # keyring is working on Mac Sonoma 14.4 and Windows 11
        token_file_path = os.path.join(dirs.testdata(), "keyring_test.json")
        save_token(
            service_name="tq42_access_token",
            backup_save_path=token_file_path,
            token="test_token",
        )
        token = get_token(
            service_name="tq42_access_token", backup_save_path=token_file_path
        )
        self.assertEqual(token, "test_token")

    @mock.patch("keyring.set_password")
    @mock.patch("keyring.get_password")
    def test_save_get_token_has_InitError(self, mock_set_password, mock_get_password):
        # keyring not working on Ubuntu 20.04.6LTS and causes InitError exception
        token_file_path = os.path.join(dirs.testdata(), "keyring_test.json")
        mock_set_password.side_effect = InitError()
        mock_get_password.side_effect = InitError()
        save_token(
            service_name="tq42_access_token",
            backup_save_path=token_file_path,
            token="test_token",
        )
        token = get_token(
            service_name="tq42_access_token", backup_save_path=token_file_path
        )
        os.remove(token_file_path)
        self.assertEqual(token, "test_token")

    @mock.patch("keyring.set_password")
    @mock.patch("keyring.get_password")
    def test_save_get_token_has_NoKeyringError(
        self, mock_set_password, mock_get_password
    ):
        # keyring not working on Debian and Redhat, NoKeyringError is raised
        token_file_path = os.path.join(dirs.testdata(), "keyring_test.json")
        mock_set_password.side_effect = NoKeyringError()
        mock_get_password.side_effect = NoKeyringError()
        save_token(
            service_name="tq42_access_token",
            backup_save_path=token_file_path,
            token="test_token",
        )
        token = get_token(
            service_name="tq42_access_token", backup_save_path=token_file_path
        )
        os.remove(token_file_path)
        self.assertEqual(token, "test_token")

    @mock.patch("keyring.get_password")
    @mock.patch("keyring.set_password")
    def test_should_return_token_even_if_keyring_locked_and_passwort_set_error_thrown(
        self, mock_set_password, mock_get_password
    ):
        token_file_path = os.path.join(dirs.testdata(), "keyring_test.json")
        mock_set_password.side_effect = PasswordSetError()
        mock_get_password.side_effect = KeyringLocked()

        save_token(
            service_name="tq42_access_token",
            backup_save_path=token_file_path,
            token="test_token",
        )

        token = get_token(
            service_name="tq42_access_token", backup_save_path=token_file_path
        )
        os.remove(token_file_path)
        self.assertEqual(token, "test_token")
