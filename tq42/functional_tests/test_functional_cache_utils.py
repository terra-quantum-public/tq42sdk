import unittest

from tq42.functional_tests.functional_test_config import FunctionalTestConfig
from tq42.utils.utils_for_cache import clear_cache, get_current_value

from tq42.utils.environment_utils import environment_default_set
from tq42.utils import utils
import os
from tq42.utils import dirs


class TestFunctionalCacheUtils(unittest.TestCase, FunctionalTestConfig):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_default_ids(self):
        environment_default_set(client=self.get_client())
        org_id = get_current_value("org")
        proj_id = get_current_value("proj")
        self.assertIsNotNone(org_id, "org_id is None")
        self.assertIsNotNone(proj_id, "proj_id is None")
        clear_cache()

    def test_save_access_token(self):
        # This test is placed here as save_access_token calls environment_default_set().

        token_file_path = os.path.join(dirs.get_config_folder_path(), "token.json")
        prev_token = utils.get_token(
            service_name="access_token", backup_save_path=token_file_path
        )

        response = {"access_token": prev_token}
        is_refresh_token_saved = self.get_client().save_access_token(response=response)
        self.assertEqual(is_refresh_token_saved, True)
        clear_cache()

        response = {"wrong_key": "dummy_refresh_token"}
        is_refresh_token_saved = self.get_client().save_access_token(response=response)
        self.assertEqual(is_refresh_token_saved, False)
        clear_cache()

    def test_save_refresh_token(self):
        response = {"refresh_token": "dummy_refresh_token"}
        is_refresh_token_saved = self.get_client().save_refresh_token(response=response)
        self.assertEqual(is_refresh_token_saved, True)
        response = {"wrong_key": "dummy_refresh_token"}
        is_refresh_token_saved = self.get_client().save_refresh_token(response=response)
        self.assertEqual(is_refresh_token_saved, False)
