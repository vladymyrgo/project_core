from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import permissions

from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

from account.models import User
from account.serializers import UserListSerializer, UserDetailSerializer

from core.reusable_core.core_bridges import LogicViewMixin
from account.reusable_core.views_api_logic import AccountSearchListViewLogic


class AccountListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,
                          permissions.IsAdminUser)
    queryset = User.objects.actual_list()
    serializer_class = UserListSerializer


class AccountSearchListView(generics.ListAPIView, LogicViewMixin):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserListSerializer
    logic_class = AccountSearchListViewLogic

    def get_queryset(self):
        search = self.logic.get_search_query()

        # Django-Haystack
        search_queryset = (SearchQuerySet().filter(content__contains=AutoQuery(search))
                                           .models(User))

        return self.logic.get_users_queryset_by_search_queryset(search_queryset)


class AccountDetailView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.actual_list()
    serializer_class = UserDetailSerializer


class AccountEditView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDetailSerializer

    def get_object(self, queryset=None):
        obj = get_object_or_404(User, id=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        User.objects.filter(id=obj.id).update(is_active=False)
        return Response(status=status.HTTP_204_NO_CONTENT)
