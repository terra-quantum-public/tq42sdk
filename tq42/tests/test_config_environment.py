import unittest

from tq42.client import ConfigEnvironment


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
        self.assertEqual(
            "https://graphql-gateway.int.terraquantum.io/graphql", env.audience
        )
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
        self.assertEqual(
            "https://graphql-gateway.staging.terraquantum.io/graphql", env.audience
        )
        self.assertEqual(
            "https://auth.staging.terraquantum.io/oauth/device/code", env.auth_url_code
        )
        self.assertEqual(
            "https://auth.staging.terraquantum.io/oauth/token", env.auth_url_token
        )
        self.code_data_test(env)
        self.token_data_test(env)
