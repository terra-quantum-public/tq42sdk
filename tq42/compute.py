from dataclasses import dataclass
from typing import Dict, List

from tq42.exception_handling import handle_generic_sdk_errors
from tq42.utils.utils import get_hw_configurations

# this import is also important for re-export!
from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    HardwareProto,
)


@dataclass
class HardwareConfig:
    name: str
    cpu: str
    memory: str
    storage: str
    gpu: str


class Compute:
    hardware: HardwareProto
    config: HardwareConfig

    @handle_generic_sdk_errors
    def __init__(self, hardware: HardwareProto = HardwareProto.HARDWARE_UNSPECIFIED):
        self.hardware = hardware
        hardware_name = HardwareProto.Name(hardware)
        configuration = self._find_matching_hardware(hardware_name)
        self.config = HardwareConfig(
            name=hardware_name,
            cpu=configuration.get("CPUs", ""),
            memory=configuration.get("Memory", ""),
            storage=configuration.get("Storage", ""),
            gpu=configuration.get("GPU", ""),
        )

    @staticmethod
    def _find_matching_hardware(hardware_name) -> Dict[str, str]:
        data = get_hw_configurations()
        if hardware_name in data:
            return data.get(hardware_name)

        return {}

    @handle_generic_sdk_errors
    def show_details(self) -> HardwareConfig:
        """
        Show details of compute configurations.

        For details, see
        https://terra-quantum-tq42sdk-docs.readthedocs-hosted.com/en/latest/Python_Developer_Guide/Selecting_Compute_Resources.html#viewing-available-compute-resources-and-configuration-details
        """
        return self.config


@handle_generic_sdk_errors
def list_all() -> List[Compute]:
    """
    Show available compute configurations.

    For details, see
    https://terra-quantum-tq42sdk-docs.readthedocs-hosted.com/en/latest/Python_Developer_Guide/Selecting_Compute_Resources.html#viewing-available-compute-resources-and-configuration-details
    """
    return [Compute(hardware=val) for key, val in HardwareProto.items() if val != 0]
