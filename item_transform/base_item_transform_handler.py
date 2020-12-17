from abc import ABCMeta, abstractmethod


class BaseItemTransformHandler(object, ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def process_item(self, load_items, crawl_items):
        pass
