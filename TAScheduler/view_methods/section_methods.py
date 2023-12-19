import abc


class SectionObj(abc.ABC):

    def __init__(self):
        self.database = None

    @abc.abstractmethod
    def getID(self):
        pass

    @abc.abstractmethod
    def getParentCourse(self):
        pass
