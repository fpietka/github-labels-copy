from github import Github
from getpass import getpass


class Labels(object):
    def __init__(self, token=None, login=None):
        self.src_labels = list()
        self.dst_labels = list()
        self._identify(token, login)

    def _identify(self, token=None, login=None):
        if token:
            self.github = Github(token)
        elif login:
            try:
                self.github = Github(login, getpass())
            except github.GithubException.TwoFactorException as e:
                print(e.message)
                exit(1)
            except github.GithubException.BadCredentialsException as e:
                print(e.message)
                exit(1)
        else:
            self.github = Github()

    def setSrcRepo(self, repository):
        self.src_repo = self.github.get_repo(repository)
        src_original_labels = self.src_repo.get_labels()
        self.src_labels = {label.name: label.color
                           for label in src_original_labels}

    def setDstRepo(self, repository):
        self.dst_repo = self.github.get_repo(repository)
        self.dst_original_labels = self.dst_repo.get_labels()
        self.dst_labels = {label.name: label.color
                           for label in self.dst_original_labels}

    def listLabels(self):
        return self.src_labels

    def getMissing(self):
        "Get missing labels from source repository into destination."
        return {name: color for name, color in self.src_labels.items()
                if name not in self.dst_labels.keys()}

    def getWrong(self):
        "Get labels with wrong color in destination repository from source."
        return {name: color for name, color in self.src_labels.items()
                if name in self.dst_labels.keys() and
                color != self.dst_labels[name]}

    def getBad(self):
        "Get labels from destination repository not in source."
        return {name: color for name, color in self.dst_labels.items()
                if name not in self.src_labels.keys()}

    def createMissing(self):
        "Create all missing labels from source repository in destination."
        for name, color in self.getMissing().items():
            print("Creating {}".format(name))
            self.dst_repo.create_label(name, color)

    def updateWrong(self):
        for name, color in self.getWrong().items():
            print("Updating {}".format(name))
            working_label = next((x for x in self.dst_original_labels
                                  if x.name == name), None)
            working_label.edit(name, color)

    def deleteBad(self):
        for name, color in self.getBad().items():
            print("Deleting {}".format(name))
            working_label = next((x for x in self.dst_original_labels
                                  if x.name == name), None)
            working_label.delete()

    def fullCopy(self):
        self.createMissing()
        self.updateWrong()
        self.deleteBad()
