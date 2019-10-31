import sys

from progressbar import ProgressBar

from helper import user_select_option

toolbar_width = 40

class AsanaOperations():

    def __init__(self, client):

        self.client = client
        self.get_workspace()

    def get_workspace(self):

        workspaces = self.client.workspaces.find_all()
        workspace = user_select_option("Please choose a workspace", workspaces)
        self.workspace_id = workspace["id"]

        return self.workspace_id


    def get_tasks(self, id):

        tasks = self.client.tasks.find_all({"project": id},
                                           fields=["completed", "due_on", "notes", "tags", "name", "assignee"])

        self.tasks = [val for i, val in enumerate(tasks)]

        return self.tasks

    def post_on_asana(self, task_list):

        project_id = self.get_project("Pick project to upload tasks from PC to Asana:")
        print("Adding posts to Asana...")
        pbar = ProgressBar()
        for task in pbar(task_list):
            self.get_tasks(project_id)
            task_on_asana = list(filter(lambda x: x['name'] == task['name'], self.tasks))
            if not task_on_asana:
                tags = task['tags']
                tag_ids = []
                for tag in tags:
                    self.load_tags()
                    tag_on_asana = list(filter(lambda x: x['name'] == tag, self.tags))
                    if not tag_on_asana:
                        tag_post = self.client.tags.create_in_workspace(self.workspace_id, {"name": tag})
                        tag_ids.append(tag_post["id"])
                    else:
                        tag_ids.append(tag_on_asana[0]['id'])
                task['tags'] = tag_ids
                task['projects'] = [project_id]
                self.client.tasks.create_in_workspace(self.workspace_id, task)


    def load_tags(self):

        tags = self.client.tags.find_all({"workspace": self.workspace_id})

        self.tags = [val for i, val in enumerate(tags)]

        return self.tags

    def get_project(self, message):

        projects = self.client.projects.find_all({"workspace": self.workspace_id})
        project = user_select_option(message, projects)
        project_id = project["id"]

        return project_id
