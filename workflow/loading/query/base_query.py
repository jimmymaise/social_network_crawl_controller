from dataclasses import dataclass


@dataclass
class Query:
    filter_: dict
    sort_: list
    limit_: int
    priority: int
    selected_fields_: list

    def query_function(self):
        return Query(filter_=self.filter_, sort_=self.sort_, selected_fields_=self.selected_fields_,
                     limit_=self.limit_, priority=1)

    @property
    def filter(self):
        return self.filter_

    @property
    def selected_fields(self):
        return self.selected_fields_

    @property
    def limit(self):
        return self.limit_

    @property
    def sort(self):
        return self.sort_
