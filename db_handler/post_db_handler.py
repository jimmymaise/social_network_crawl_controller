from db_handler import general_db_handler


class PostDBHandler(general_db_handler):
    def __init__(self):
        super(PostDBHandler, self).__init__()
        self.collection = self.database['posts']

    def get_many_pair_by_post_id(self,
                                 _post_ids,
                                 _selected_fields=None):
        result = self.get_many_pairs_by_id(_ids=_post_ids,
                                           _selected_fields=_selected_fields)
        return result

    def get_one_by_post_id(self,
                           _post_id,
                           _selected_fields=None):
        result = self.get_one_by_id(_id=_post_id,
                                    _selected_fields=_selected_fields)
        return result

    def get_many_by_user_id_with_timerange(self,
                                           _user_id,
                                           _from,
                                           _to,
                                           _selected_fields=None):
        # ===== Execute =====
        result = self.get_many_by_filter(_filter={'user_id': _user_id,
                                                  'taken_at_timestamp': {'$gt': _from,
                                                                         '$lt': _to}},
                                         _selected_fields=_selected_fields)
        return result

    def get_many_by_page_id_with_timerange(self,
                                           _page_id,
                                           _from,
                                           _to,
                                           _selected_fields=None):
        # ===== Execute =====
        result = self.get_many_by_filter(_filter={'page_id': _page_id,
                                                  'taken_at_timestamp': {'$gt': _from,
                                                                         '$lt': _to}},
                                         _selected_fields=_selected_fields)
        return result

    def get_many_by_user_id(self, _filter, _sort, _selected_fields, _num_post=30):
        result = self.get_many_by_filter_and_sort(_filter=_filter,
                                                  _sort=_sort,
                                                  _selected_fields=_selected_fields) \
            .limit(_num_post)
        return result
