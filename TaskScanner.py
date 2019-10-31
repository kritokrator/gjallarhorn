import os

import frontmatter

from settings import PATH_TO_ASANA_DIRECTORY

class TaskScanner():

    def __init__(self):
        self.path = PATH_TO_ASANA_DIRECTORY

    def get_file_list(self):

        file_list = []
        for path, dirnames, filenames in os.walk(self.path):
            file_list = file_list + [path + '/' + name for name in filenames]

        self.filelist = file_list
        return self.filelist

    def get_tasks_list(self):

        list_of_tasks = []
        for file in self.filelist:
            parser = file.split('/')
            title = parser[-1].strip('.md')
            post = frontmatter.load(file)
            tags = [tag.strip() for tag in post['tags'].split(',')]
            if parser[-2] != 'waiting_to_be_born':
                additional_tag = parser[-2]
                tags.append(additional_tag)
            ready_post = {'name': title, 'notes': post.content, 'tags': tags}
            list_of_tasks.append(ready_post)

        return list_of_tasks