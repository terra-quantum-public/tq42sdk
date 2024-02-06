import unittest

from tq42.compute import Compute, list_all, HardwareProto


class TestCompute(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_compute_list_all(self):
        all_details = list_all()
        self.assertIsNotNone(all_details)
        self.assertLess(3, len(all_details))
        self.assertNotIn(
            "HARDWARE_UNSPECIFIED", [hw.show_details().name for hw in all_details]
        )

    def test_compute_show_details(self):
        details = Compute(hardware=HardwareProto.SMALL).show_details()
        self.assertEqual(details.name, HardwareProto.Name(HardwareProto.SMALL))

    def test_compute_invalid_type(self):
        with self.assertRaises(AttributeError):
            Compute(hardware=HardwareProto.NOT_A_HARDWARE)
