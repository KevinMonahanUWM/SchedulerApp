import abc


class UserObj(abc.ABC):

    def __init__(self):
        self.database = None

    @abc.abstractmethod
    def login(self, email_address, password):
        pass

    @abc.abstractmethod
    def getUsername(self):
        pass

    @abc.abstractmethod
    def getPassword(self):
        pass

    @abc.abstractmethod
    def getName(self):
        pass

    @abc.abstractmethod
    def getRole(self):
        pass

    @abc.abstractmethod
    def editContactInfo(self):
        pass
