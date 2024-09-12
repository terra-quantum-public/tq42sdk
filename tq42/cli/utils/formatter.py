import json
from abc import ABCMeta, abstractmethod
from typing import List

from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    ExperimentRunStatusProto,
)
from com.terraquantum.experiment.v3alpha2.experimentrun.experiment_run_pb2 import (
    ExperimentRunProto,
)

from tq42.experiment_run import HardwareProto, ExperimentRun
from ...project import Project


class ItemWithIDFormatter(metaclass=ABCMeta):
    @abstractmethod
    def _prefix(self):
        pass

    @abstractmethod
    def _get_items(self, list_items):
        pass

    def format_by_id(self, id):
        return '{}="{}"'.format(self._prefix(), id)

    def format(self, item):
        return self.format_by_id(item.id)

    def format_by_list_object(self, list_items):
        return [self.format(item) for item in self._get_items(list_items)]


class ItemWithNameFormatterResourceClasses(ItemWithIDFormatter, metaclass=ABCMeta):
    def format_by_name_and_id(self, name, id):
        if name is None:
            return self.format_by_id(id)
        else:
            return '{}="{}" ({})'.format(self._prefix(), name, id)

    def format(self, item):
        return self.format_by_name_and_id(item.data.name, item.id)


class OrganizationFormatter(ItemWithIDFormatter):
    def _prefix(self):
        return "org"

    def format_by_project(self, proj: Project):
        return self.format_by_id(proj.data.organization_id)

    def _get_items(self, list_items):
        return list_items


class ProjectFormatter(ItemWithNameFormatterResourceClasses):
    def _prefix(self):
        return "proj"

    def _get_items(self, list_items):
        return list_items


class ExperimentFormatter(ItemWithNameFormatterResourceClasses):
    def _prefix(self):
        return "exp"

    def _get_items(self, list_items):
        return list_items


class ExpRunFormatter(ItemWithIDFormatter):
    def _prefix(self):
        return "run"

    def _get_items(self, list_items):
        return list_items

    def run_created_lines(self, run: ExperimentRunProto):
        status_line = 'status="{}"'.format(ExperimentRunStatusProto.Name(run.status))
        return [self.format(run), status_line]

    def run_checked_lines(self, run: ExperimentRun):
        data = run.data
        algo_line = 'algorithm="{}"'.format(data.algorithm)
        compute_line = 'compute="{}"'.format(HardwareProto.Name(data.hardware))

        result_line = ""
        outputs_line = ""
        if data.status == ExperimentRunStatusProto.COMPLETED:
            result_line = f'result="{json.dumps(run.result)}"'
            outputs_line = f'outputs="{json.dumps(run.outputs)}"'

        error_message = (
            'error_message="{}"'.format(data.error_message)
            if data.error_message
            else ""
        )

        return self.run_created_lines(data) + list(
            filter(
                None,
                [
                    algo_line,
                    compute_line,
                    result_line,
                    outputs_line,
                    error_message,
                ],
            )
        )


org_formatter = OrganizationFormatter()
proj_formatter = ProjectFormatter()
exp_formatter = ExperimentFormatter()
run_formatter = ExpRunFormatter()


def set_proj_lines(proj: Project) -> List[str]:
    org_line = org_formatter.format_by_project(proj)
    proj_line = proj_formatter.format(proj)
    return [org_line, proj_line]
