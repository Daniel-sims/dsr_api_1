from django.conf import settings
from rest_framework.permissions import BasePermission


class CanListCreateCompanyPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.has_perm(settings.CAN_VIEW_COMPANY_PERM_NAME)

        elif request.method == 'POST':
            return request.user.has_perm(settings.CAN_ADD_COMPANY_PERM_NAME)

        return False


class CanRetrieveUpdateDestroyCompanyPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.has_perm(settings.CAN_VIEW_COMPANY_PERM_NAME)

        elif request.method == 'PATCH':
            return request.user.has_perm(settings.CAN_CHANGE_COMPANY_PERM_NAME)

        elif request.method == 'DELETE':
            return request.user.has_perm(settings.CAN_DELETE_COMPANY_PERM_NAME)

        return False
