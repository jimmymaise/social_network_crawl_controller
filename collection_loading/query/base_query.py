from dataclasses import dataclass


@dataclass
class Query:
    _filter: dict
    _sort: list
    _limit: int
    priority: int
    selected_fields: list

    def query_function(self):
        return Query(_filter=self._filter, _sort=self._sort, selected_fields=self.selected_fields,
                     _limit=self._limit, priority=1)