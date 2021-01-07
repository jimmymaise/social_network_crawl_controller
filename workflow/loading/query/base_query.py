from dataclasses import dataclass


@dataclass
class Query:
    filter_: dict
    sort_: list
    limit_: int
    priority: int
    selected_fields: list

    def query_function(self):
        return Query(filter_=self.filter_, sort_=self.sort_, selected_fields=self.selected_fields,
                     limit_=self.limit_, priority=1)

    def filter(self):
        return self.filter_

    def selected_fields(self):
        return self.selected_fields

    def limit(self):
        return self.limit_

    def sort(self):
        return self.sort_
