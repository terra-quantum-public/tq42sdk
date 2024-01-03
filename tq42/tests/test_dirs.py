import os
import unittest

from tq42.utils import dirs


class TestDirs(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_code(self):
        self.assertTrue(os.path.exists(dirs.code()))
        self.assertTrue(os.path.isfile(dirs.code("__init__.py")))

    def test_testdata(self):
        self.assertTrue(os.path.exists(dirs.testdata()))
        self.assertTrue(os.path.isfile(dirs.testdata("README.md")))

    def test_cache(self):
        self.assertTrue(os.path.exists(dirs.cache_dir()))
        self.assertIsNotNone(dirs.cache_file())

    def test_text_files(self):
        self.assertTrue(os.path.exists(dirs.text_files_dir()))
        self.assertTrue(
            os.path.isfile(
                dirs.full_path(dirs.text_files_dir(), "hardware_configs.json")
            )
        )
        self.assertTrue(
            os.path.isfile(dirs.full_path(dirs.text_files_dir(), "tq42_commands.txt"))
        )
        self.assertTrue(
            os.path.isfile(dirs.full_path(dirs.text_files_dir(), "cpu_configs.json"))
        )
        self.assertTrue(
            os.path.isfile(
                dirs.full_path(dirs.text_files_dir(), "unauthenticated_error.txt")
            )
        )
        self.assertTrue(
            os.path.isfile(
                dirs.full_path(
                    dirs.text_files_dir(), "insufficient_permission_error.txt"
                )
            )
        )

    def test_create_or_get_package_folder_path(self):
        config_dir = dirs.create_or_get_config_dir()
        self.assertTrue(os.path.exists(config_dir))
        self.assertEqual(dirs.CONFIG_FOLDER_NAME, os.path.basename(config_dir))

    def test_config(self):
        expected = os.path.join(dirs.create_or_get_config_dir(), "token.json")
        actual = dirs.config("token.json")
        self.assertEqual(expected, actual)
