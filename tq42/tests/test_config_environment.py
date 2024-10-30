import unittest
from unittest import mock

from tq42.utils.environment import ConfigEnvironment


class TestConfigEnvironment(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def code_data_test(self, env: ConfigEnvironment):
        expected = {
            "client_id": env.client_id,
            "scope": env.scope,
            "audience": env.audience,
        }
        actual = env.code_data
        self.assertEqual(expected, actual)

        expected = {"Content-Type": "application/x-www-form-urlencoded"}
        actual = env.headers
        self.assertEqual(expected, actual)

    def token_data_test(self, env: ConfigEnvironment):
        expected = {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": "DEVICE CODE",
            "client_id": env.client_id,
        }
        actual = env.token_data("DEVICE CODE")
        self.assertEqual(expected, actual)

    def test_int_urls(self):
        env = ConfigEnvironment(
            "int.terraquantum.io",
            "CLIENT ID",
            "openid profile email",
        )
        self.assertEqual("api.int.terraquantum.io", env.api_host)
        self.assertEqual("https://web-api.int.terraquantum.io", env.audience)
        self.assertEqual(
            "https://auth.int.terraquantum.io/oauth/device/code", env.auth_url_code
        )
        self.assertEqual(
            "https://auth.int.terraquantum.io/oauth/token", env.auth_url_token
        )
        self.code_data_test(env)
        self.token_data_test(env)

    def test_staging_urls(self):
        env = ConfigEnvironment(
            "staging.terraquantum.io",
            "CLIENT ID",
            "openid profile email",
        )

        self.assertEqual("api.staging.terraquantum.io", env.api_host)
        self.assertEqual("https://web-api.staging.terraquantum.io", env.audience)
        self.assertEqual(
            "https://auth.staging.terraquantum.io/oauth/device/code", env.auth_url_code
        )
        self.assertEqual(
            "https://auth.staging.terraquantum.io/oauth/token", env.auth_url_token
        )
        self.code_data_test(env)
        self.token_data_test(env)

    @mock.patch.dict(
        "os.environ",
        {
            "TQ42_BASE_URL": "base_url",
            "TQ42_CLIENT_ID": "client_id",
            "TQ42_SCOPE": "scope",
        },
    )
    def test_environment_name(self):
        env = ConfigEnvironment.from_env()

        self.assertEqual("base_url", env.base_url)
        self.assertEqual("client_id", env.client_id)
        self.assertEqual("scope", env.scope)

    def test_default_environment(self):
        env = ConfigEnvironment.from_env()

        self.assertEqual("terraquantum.io", env.base_url)
        self.assertEqual("gvBa4BHKOTlotDuE6E2HSQBzBDlM00F4", env.client_id)
        self.assertEqual("openid profile email offline_access tq42", env.scope)
