from core.workflows.loading.query.base_query import Aggregate


class PostAggregate:
    @staticmethod
    def get_post_statistics(user_id: str) -> Aggregate:
        agg = Aggregate()\
            .match({
                'user_id': user_id
            })\
            .group({
                '_id': "$user_id",
                'average_view': {
                    '$avg': "$num_view"
                },
                'average_like': {
                    '$avg': "$num_like"
                }
            })

        return agg
