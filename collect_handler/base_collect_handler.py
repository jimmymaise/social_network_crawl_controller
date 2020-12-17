from abc import ABCMeta, abstractmethod


class BaseCollectHandler(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        self.type = None
        pass
