from ..command import Command as _Command

class Command(_Command):
    version = None

    @classmethod
    def get_version(cls):
        return cls.version
