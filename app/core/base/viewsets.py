

from core.base.pagination import ConditionalPaginationMixin, HeadersPaginationMixin
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet


class ModelListViewSet(
        HeadersPaginationMixin,
        ConditionalPaginationMixin,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
    pass


class ModelListCreateViewSet(
        HeadersPaginationMixin,
        ConditionalPaginationMixin,
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
    pass


class ModelCrudViewSet(HeadersPaginationMixin,
                       ConditionalPaginationMixin,
                       ModelViewSet):
    pass

