import unittest

from tq42.utils import dirs, file_handling
from tq42.utils.utils_for_cache import (
    clear_cache,
    write_key_value_to_cache,
    get_current_value,
)
from tq42.functional_tests.functional_test_config import FunctionalTestConfig


class TestCacheUtils(unittest.TestCase, FunctionalTestConfig):
    def setUp(self):
        pass

    def test_get_current_id(self):
        clear_cache()
        write_key_value_to_cache("org", "RANDOM_ORG_ID")
        org_id = get_current_value("org")
        self.assertEqual("RANDOM_ORG_ID", org_id)
        clear_cache()

    def test_clear_cache(self):
        write_key_value_to_cache("org", "RANDOM_ORG_ID")
        content = file_handling.read_file(dirs.cache_file())
        self.assertNotEqual(content, "")
        clear_cache()
        content = file_handling.read_file(dirs.cache_file())
        self.assertEqual(content, "")
