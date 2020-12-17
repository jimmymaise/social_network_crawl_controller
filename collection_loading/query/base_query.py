from dataclasses import dataclass


@dataclass
class Query:
    _filter: dict
    _sort: list
    _limit: int
    priority: int
    selected_fields: list
