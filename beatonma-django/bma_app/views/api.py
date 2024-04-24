import logging

from bma_app.auth import has_api_permission
from bma_app.views.pagination import ApiPagination
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import GenericViewSet, ModelViewSet

log = logging.getLogger(__name__)


class ApiTokenPermission(BasePermission):
    def has_permission(self, request, view):
        return has_api_permission(request)

    def has_object_permission(self, request, view, obj):
        return has_api_permission(request)


class ApiViewSet(GenericViewSet):
    permission_classes = (ApiTokenPermission,)
    pagination_class = ApiPagination


class ApiModelViewSet(ApiViewSet, ModelViewSet):
    pass
