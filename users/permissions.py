from django.conf import settings
from rest_framework.permissions import BasePermission


class UserPermissionsNoCompany(BasePermission):
    """
    The Users endpoint is one of the most complicated. With specifics on who and who can't access the endpoints.
    In Future I'd like to be able to specific which user groups a staff member can view but for now it is a simple
    Yes or No to being able to GET on this endpoint. A GET Request from a user will either list all None company users
    if the requesting user is not in a company, or all users for that company if the user is in a company.

    User Permissions by group for no company;
        DSR Admin
            CAN_ADD_DSR_EMPLOYEE_PERM

        DSR Employee

        DSR Customer Super Admin

        DSR Customer Admin

        DSR Customer User
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':

            new_user_dsr_group = request.data['dsr_group']

            if new_user_dsr_group is not None:
                # DSR Admin and DSR Employee are the only account types that can be created
                # without a company.
                if new_user_dsr_group == settings.DSR_ADMIN_SLUG_FIELD:
                    return request.user.has_perm(settings.CAN_ADD_DSR_ADMIN_PERM_NAME)

                elif new_user_dsr_group == settings.DSR_EMPLOYEE_SLUG_FIELD:
                    return request.user.has_perm(settings.CAN_ADD_DSR_EMPLOYEE_PERM_NAME)

                else:
                    # The group isn't on the list of accepted groups so deny permissions as it'll
                    # cause unexpected behaviour.
                    return False

        elif request.method == 'PATCH':
            return True
        elif request.method == 'DELETE':
            return True

        return False
