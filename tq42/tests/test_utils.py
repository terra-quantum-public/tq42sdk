import unittest
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from unittest import mock
from keyring.errors import InitError, NoKeyringError, PasswordSetError, KeyringLocked

from tq42 import exceptions
from tq42.utils import dirs, utils, file_handling
from tq42.utils.token_manager import TokenManager
import json
from tq42.client import ConfigEnvironment, TQ42Client
from tq42.exceptions import NoMatchingAttributeError
from tq42.algorithm import AlgorithmProto
from tq42.compute import HardwareProto
from com.terraquantum.experiment.v1.experimentrun import (
    create_experiment_run_request_pb2 as create_exp_run,
)


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.client = TQ42Client()

    def test_utils_get_id(self):
        filepath = dirs.full_path(dirs.test_data_dir(), "test_utils_get_id.txt")
        content = file_handling.read_file(filepath)
        res = utils.get_id(content)
        self.assertEqual('"64a35a73-3da2-4f44-bce3-9e5a8eac6d30"', res)

    def test_get_matching_algorithm(self):
        self.assertEqual(AlgorithmProto.TOY, utils.get_algo_num("toy"))
        self.assertEqual(AlgorithmProto.TOY, utils.get_algo_num("ToY"))
        self.assertEqual(AlgorithmProto.TOY, utils.get_algo_num("TOY"))

        self.assertEqual(1, utils.get_algo_num(1))

        self.assertEqual(AlgorithmProto.TOY, utils.get_algo_num(AlgorithmProto.TOY))
        self.assertEqual(
            AlgorithmProto.TOY,
            utils.get_algo_num(AlgorithmProto.Name(AlgorithmProto.TOY)),
        )

    def test_no_matching_algorithm(self):
        self.assertRaises(
            exceptions.NoMatchingAttributeError,
            utils.get_algo_num,
            "no-way-this-is-an-algo",
        )
        self.assertRaises(exceptions.NoMatchingAttributeError, utils.get_algo_num, "")

    def test_get_matching_hardware(self):
        self.assertEqual(HardwareProto.SMALL, utils.get_hardware_num("small"))
        self.assertEqual(HardwareProto.SMALL, utils.get_hardware_num("SmAlL"))
        self.assertEqual(HardwareProto.SMALL, utils.get_hardware_num("SMALL"))

        self.assertEqual(1, utils.get_hardware_num(1))

        self.assertEqual(
            HardwareProto.SMALL,
            utils.get_hardware_num(HardwareProto.SMALL),
        )
        self.assertEqual(
            HardwareProto.SMALL,
            utils.get_hardware_num(HardwareProto.Name(HardwareProto.SMALL)),
        )

    def test_no_matching_hardware(self):
        self.assertRaises(
            exceptions.NoMatchingAttributeError,
            utils.get_hardware_num,
            "no-way-this-is-a-hardware-config",
        )
        self.assertRaises(
            exceptions.NoMatchingAttributeError, utils.get_hardware_num, ""
        )

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
            self.client.timestamp_file_path, str(token_timestamp)
        )

        # load config file
        alt_config_file = dirs.text_files_dir("config.json")
        with open(alt_config_file, encoding="utf-8") as f:
            config_data = json.load(f)

        environment = ConfigEnvironment(
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

    def test_dynamic_request_valid_params(self):
        params = {
            "parameters": {"n": 4, "r": 1.1, "msg": "this is optimus prime"},
            "inputs": {},
        }
        result = utils.dynamic_create_exp_run_request(
            parameters=params,
            algo=AlgorithmProto.TOY,
            exp_id="random-uuid",
            hardware=HardwareProto.SMALL,
        )
        self.assertIsNot(result.SerializeToString(), b"")

    def test_dynamic_request_invalid_params_field_name(self):
        params = {
            "parameters": {
                "msg": "this is bumblebee",
                "unknown field name": "this field should not be here",
            },
            "inputs": {},
        }
        with self.assertRaises(NoMatchingAttributeError) as context:
            utils.dynamic_create_exp_run_request(
                parameters=params,
                algo=AlgorithmProto.TOY,
                exp_id="random-uuid",
                hardware=HardwareProto.SMALL,
            )

        self.assertEqual(
            str(context.exception.details),
            'Protocol message ToyParametersProto has no "unknown field name" field.',
        )

    def test_dynamic_request_invalid_params_grid(self):
        params = {
            "parameters": {
                "dimensionality": 4,
                "iteration_number": 1,
                "maximal_rank": 4,
                "points_number": 1,
                "quantization": True,
                "tolerance": 0.001,
                "lower_limits": [0, 0.2, 0.5, 0.2],
                "upper_limits": [30, 0.5, 1.5, 0.6],
                "grd": [5, 5, 5, 5],
                "objectivefunction": "http://34.141.232.153:8000/ymixer/eval",
            },
            "inputs": {},
        }

        with self.assertRaises(NoMatchingAttributeError) as context:
            utils.dynamic_create_exp_run_request(
                parameters=params,
                algo=AlgorithmProto.TETRA_OPT,
                exp_id="random-uuid",
                hardware=HardwareProto.SMALL,
            )

        self.assertEqual(
            str(context.exception.details),
            'Protocol message TetraOptParametersProto has no "grd" field.',
        )

    def test_dynamic_request_params(self):
        parameters = {
            "parameters": {
                "dimensionality": 4,
                "iteration_number": 1,
                "maximal_rank": 4,
                "points_number": 1,
                "quantization": True,
                "tolerance": 0.001,
                "lower_limits": [0, 0.2, 0.5, 0.2],
                "upper_limits": [30, 0.5, 1.5, 0.6],
                "grid": [5, 5, 5, 5],
                "objective_function": "http://34.141.232.153:8000/ymixer/eval",
            },
            "inputs": {},
        }

        result = utils.dynamic_create_exp_run_request(
            parameters=parameters,
            algo=AlgorithmProto.TETRA_OPT,
            exp_id="random-uuid",
            hardware=HardwareProto.SMALL,
        )

        expected = create_exp_run.CreateExperimentRunRequest(
            request_id=None,
            algorithm=AlgorithmProto.TETRA_OPT,
            experiment_id="random-uuid",
            hardware=HardwareProto.SMALL,
            tetra_opt_metadata=parameters,
        )

        self.assertEqual(str(result), str(expected))

    def test_config_file_path(self):
        alternative_json_path = dirs.testdata("config.json")
        tq42 = TQ42Client(alternative_json_path)
        self.assertEqual(tq42.config_file, alternative_json_path)

    def test_find_oneof_field_name(self):
        res = utils.find_oneof_field_name("ToyMetadataProto")
        self.assertEqual(res, "toy_metadata")

    def test_save_get_token_with_keyring_enabled(self):
        # keyring is working on Mac Sonoma 14.4 and Windows 11
        token_file_path = os.path.join(dirs.testdata(), "keyring_test.json")
        utils.save_token(
            service_name="access_token",
            backup_save_path=token_file_path,
            token="test_token",
        )
        token = utils.get_token(
            service_name="access_token", backup_save_path=token_file_path
        )
        self.assertEqual(token, "test_token")

    @mock.patch("keyring.set_password")
    @mock.patch("keyring.get_password")
    def test_save_get_token_has_InitError(self, mock_set_password, mock_get_password):
        # keyring not working on Ubuntu 20.04.6LTS and causes InitError exception
        token_file_path = os.path.join(dirs.testdata(), "keyring_test.json")
        mock_set_password.side_effect = InitError()
        mock_get_password.side_effect = InitError()
        utils.save_token(
            service_name="access_token",
            backup_save_path=token_file_path,
            token="test_token",
        )
        token = utils.get_token(
            service_name="access_token", backup_save_path=token_file_path
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
        utils.save_token(
            service_name="access_token",
            backup_save_path=token_file_path,
            token="test_token",
        )
        token = utils.get_token(
            service_name="access_token", backup_save_path=token_file_path
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

        utils.save_token(
            service_name="access_token",
            backup_save_path=token_file_path,
            token="test_token",
        )

        token = utils.get_token(
            service_name="access_token", backup_save_path=token_file_path
        )
        os.remove(token_file_path)
        self.assertEqual(token, "test_token")
