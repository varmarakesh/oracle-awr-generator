__author__ = 'rakesh.varma'
from ConfigParser import SafeConfigParser

class ConfigFactory:

    def __init__(self):
        self.config = SafeConfigParser()
        self.config.read('config.ini')
        self.section = 'all'

    @property
    def username(self):
        return self.config.get(section = self.section, option = 'username')

    @property
    def password(self):
        return self.config.get(section = self.section, option = 'password')

    @property
    def database(self):
        return self.config.get(section = self.section, option = 'database')

    @property
    def directory(self):
        return self.config.get(section = self.section, option = 'directory')

    @property
    def poolsize(self):
        return self.config.get(section = self.section, option = 'poolsize')

    @property
    def kafkaconnection(self):
        return self.config.get(section = self.section, option = 'kafkaconnection')


    @property
    def kafkatopic(self):
        return self.config.get(section = self.section, option = 'kafkatopic')