from dataclasses import dataclass


@dataclass
class Query:
    filter_: dict
    sort_: list
    limit: int
    selected_fields: list
    priority: int


@dataclass
class Aggregate:
    pipelines: list

    def __init__(self):
        self.pipelines = []

    def match(self, match_):
        self.pipelines.append({
            '$match': match_
        })
        return self

    def group(self, group_):
        self.pipelines.append({
            '$group': group_
        })
        return self

    def sort(self, sort_):
        self.pipelines.append({
            '$sort': sort_
        })
        return self

    def build(self):
        return self.pipelines

