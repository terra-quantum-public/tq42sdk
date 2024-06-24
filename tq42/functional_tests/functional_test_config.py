from dataclasses import dataclass
from typing import Any

from tq42.client import TQ42Client
from tq42.organization import list_all as list_all_organizations
from tq42.project import list_all as list_all_projects
from tq42.experiment import list_all as list_all_experiments
from tq42.experiment_run import list_all as list_all_experiment_runs


@dataclass()
class Args:
    org: str
    proj: str
    exp: str
    run: str
    export_path: str
    config: Any


class FunctionalTestConfig:
    args: Args = None
    _client = None

    @property
    def org(self):
        return self.args.org

    @property
    def proj(self):
        return self.args.proj

    @property
    def exp(self):
        return self.args.exp

    @property
    def exp_run(self):
        return self.args.run

    @property
    def export_path(self):
        return self.args.export_path

    @property
    def config(self):
        return self.args.config

    def get_client(self) -> TQ42Client:
        if self._client is None:
            self._client = TQ42Client(self.config)
        return self._client

    @staticmethod
    def prepare_defaults():
        auto_pick = False
        client = TQ42Client()
        arguments = Args(org="", proj="", exp="", run="", export_path="", config=None)

        choices = [
            "{} ({})".format(org.id, org.data.name)
            for org in list_all_organizations(client=client)
        ]
        arguments.org = FunctionalTestConfig.provide_choice_id(
            "org", choices, auto_pick
        )

        choices = [
            "{} ({})".format(proj.id, proj.data.name)
            for proj in list_all_projects(client=client, organization_id=arguments.org)
        ]
        arguments.proj = FunctionalTestConfig.provide_choice_id(
            "proj", choices, auto_pick
        )
        choices = [
            "{} ({})".format(exp.id, exp.data.name)
            for exp in list_all_experiments(client=client, project_id=arguments.proj)
        ]
        arguments.exp = FunctionalTestConfig.provide_choice_id(
            "exp", choices, auto_pick
        )
        choices = [
            "{}".format(runs.id)
            for runs in list_all_experiment_runs(
                client=client, experiment_id=arguments.exp
            )
        ]
        arguments.run = FunctionalTestConfig.provide_choice_id(
            "exp run", choices, auto_pick
        )
        arguments.export_path = FunctionalTestConfig.question_with_default(
            "Which export path to use?", ".", auto_pick
        )
        return arguments

    @staticmethod
    def question_with_default(question: str, default: str, auto_pick: bool) -> str:
        if auto_pick:
            return default

        choice = str(input(f"{question} ({default})"))
        if choice.strip() == "":
            return default

        return choice

    @staticmethod
    def custom_select(question: str, choices: list) -> str:
        print(question)
        for index, choice in enumerate(choices, start=1):
            print(f"{index}. {choice}")

        while True:
            try:
                choice_index = int(input("Enter the number of your choice: ")) - 1
                if 0 <= choice_index < len(choices):
                    return choices[choice_index]
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    @staticmethod
    def provide_choice_id(arg_type: str, choices: [str], auto_pick: bool) -> str:
        if auto_pick:
            return choices[0].split(" ")[0]

        choice = FunctionalTestConfig.custom_select(
            "Which {} do you want to use?".format(arg_type), choices=choices
        )
        return choice.split(" ")[0]


class FunctionalCLITestConfig(FunctionalTestConfig):
    @property
    def client(self):
        return self.get_client()
