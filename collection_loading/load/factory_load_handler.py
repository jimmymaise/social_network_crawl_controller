from collection_loading.load.kol_load_handler import KOLLoadHandler
from collection_loading.load.report_load_handler import ReportLoadHandler
from collection_loading.load.collection_load_enum import CollectionLoadEnum


class FactoryLoadHandler:
    @staticmethod
    def create_load_handler(service_name):
        if service_name == CollectionLoadEnum.KOLLoad:

            return KOLLoadHandler

        elif service_name == CollectionLoadEnum.ReportLoad:

            return ReportLoadHandler
