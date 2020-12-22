from collection_loading.load.kol_load_handler import KOLLoadHandler
from collection_loading.load.report_load_handler import ReportLoadHandler


class FactoryLoadHandler:
    def create_load_handler(self, service_name):
        if service_name == 'KOLLoad':

            return KOLLoadHandler

        elif service_name == 'ReportLoad':

            return ReportLoadHandler
