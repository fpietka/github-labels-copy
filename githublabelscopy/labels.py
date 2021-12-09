from github import Github
from getpass import getpass
import yaml


class Labels(object):
    def __init__(self, token=None, login=None):
        self.src_labels = dict()
        self.dst_labels = dict()
        self._identify(token, login)
        self._dumpMode = False
        self._labels = dict()

    def _identify(self, token=None, login=None):
        if token:
            self.github = Github(token)
        elif login:
            self.github = Github(login, getpass())
        else:
            self.github = Github()

    def setSrcRepo(self, repository):
        self.src_repo = self.github.get_repo(repository)
        src_original_labels = self.src_repo.get_labels()
        self.src_labels = {label.name: {'color': label.color, 'description': label.description}
                           for label in src_original_labels}

    def setDstRepo(self, repository):
        self.dst_repo = self.github.get_repo(repository)
        self.dst_original_labels = self.dst_repo.get_labels()
        self.dst_labels = {label.name: {'color': label.color, 'description': label.description}
                           for label in self.dst_original_labels}

    def load(self, filename):
        with open(filename, 'r') as fh:
            self.src_labels = yaml.load(fh.read())

    def activateDumpMode(self):
        self._dumpMode = True

    def dump(self):
        return yaml.dump(self._labels)

    def listLabels(self):
        return self.src_labels

    def getMissing(self):
        "Get missing labels from source repository into destination."
        return {label_name: label_data for label_name, label_data in self.src_labels.items()
                if label_name not in self.dst_labels.keys()}

    def getWrongColor(self):
        "Get labels with wrong color in destination repository from source."
        return {label_name: label_data for label_name, label_data in self.src_labels.items()
                if label_name in self.dst_labels.keys() and
                label_data['color'] != self.dst_labels[label_name]['color']}
    
    def getWrongDescription(self):
        "Get labels with wrong description in destination repository from source."
        return {label_name: label_data for label_name, label_data in self.src_labels.items()
                if label_name in self.dst_labels.keys() and
                label_data['description'] != self.dst_labels[label_name]['description']}

    def getBad(self):
        "Get labels from destination repository not in source."
        return {label_name: label_data for label_name, label_data in self.dst_labels.items()
                if label_name not in self.src_labels.keys()}

    def createMissing(self):
        "Create all missing labels from source repository in destination."
        missings = self.getMissing()
        self._labels.update(missings)
        if not self._dumpMode:
            for label_name, label_data in missings.items():
                print("Creating {}".format(label_name))
                self.dst_repo.create_label(label_name, label_data['color'], label_data['description'])

    def updateWrongColor(self):
        wrongs = self.getWrongColor()
        self._labels.update(wrongs)
        if not self._dumpMode:
            for label_name, label_data in wrongs.items():
                print("Updating {}".format(label_name))
                working_label = next((x for x in self.dst_original_labels
                                     if x.name == label_name), None)
                working_label.edit(label_name, label_data['color'], working_label.description)
                
    def updateWrongDescription(self):
        wrongs = self.getWrongDescription()
        self._labels.update(wrongs)
        if not self._dumpMode:
            for label_name, label_data in wrongs.items():
                print("Updating {}".format(label_name))
                working_label = next((x for x in self.dst_original_labels
                                     if x.name == label_name), None)
                working_label.edit(label_name, working_label.color, label_data['description'])

    def deleteBad(self):
        bads = self.getBad()
        self._labels.update(bads)
        if not self._dumpMode:
            for name, _ in bads.items():
                print("Deleting {}".format(name))
                working_label = next((x for x in self.dst_original_labels
                                     if x.name == name), None)
                working_label.delete()

    def fullCopy(self):
        self.createMissing()
        self.updateWrongColor()
        self.updateWrongDescription()
        self.deleteBad()
