import unittest

from tq42.functional_tests.functional_test_config import FunctionalTestConfig
from tq42.utils.utils_for_cache import clear_cache, get_current_value

from tq42.utils.environment_utils import environment_default_set


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
