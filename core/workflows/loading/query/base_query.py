from dataclasses import dataclass


@dataclass
class Query:
    filter_: dict
    sort_: list
    limit: int
    selected_fields: list
    priority: int
