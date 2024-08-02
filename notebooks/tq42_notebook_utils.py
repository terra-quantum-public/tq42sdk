from tq42.organization import Organization, list_all as list_all_organizations
from tq42.project import Project, list_all as list_all_projects
from tq42.experiment import Experiment, list_all as list_all_experiments
from tq42.client import TQ42Client
from ipywidgets import interact


class Selector:
    organization: Organization = None
    project: Project = None
    experiment: Experiment = None

    def select_organization(self, client: TQ42Client):
        org_list = list_all_organizations(client=client)

        def f(organization):
            for o in org_list:
                if o.data.name == organization:
                    self.organization = o
                    print(
                        f"Using organization {organization}, {self.organization.data.id}"
                    )
                    return

        interact(f, organization=[o.data.name for o in org_list])

    def select_project(self, client: TQ42Client):
        if self.organization is None:
            print("First select an organization, and then select project.")
            return

        proj_list = list_all_projects(
            client=client, organization_id=self.organization.id
        )

        def f(project):
            for p in proj_list:
                if p.data.name == project:
                    self.project = p
                    print(f"Using project {project}, {self.project.data.id}")
                    return

        interact(f, project=[p.data.name for p in proj_list])

    def select_experiment(self, client: TQ42Client):
        if self.project is None:
            print("First select a project and then select an experiment")

        # List the experiments within that project and select one
        exp_list = list_all_experiments(client=client, project_id=self.project.id)

        def f(experiment):
            for e in exp_list:
                if e.data.name == experiment:
                    self.experiment = e
                    print(f"Using experiment {experiment}, {self.experiment.data.id}")
                    return

        interact(f, experiment=[e.data.name for e in exp_list])
