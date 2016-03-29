from core.reusable_core.core_bridges import BaseLogic

from account.models import User


class AccountSearchListViewLogic(BaseLogic):

    def get_search_query(self):
        query = self.request.query_params
        return query.get('search', None)

    def get_users_queryset_by_search_queryset(self, search_queryset):
        if search_queryset:
            ids = [o.pk for o in search_queryset]
            return User.get_actual_list_by_ids(ids)
        else:
            return User.get_empty_queryset()
