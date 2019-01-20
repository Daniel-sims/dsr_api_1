from django.conf import settings
from django.contrib.auth.models import Permission, Group
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from groups.models import DsrGroup
from users.factories import UserFactory, DsrGroupFactory


class CreateUserNoCompanyTestCase(APITestCase):
    valid_add_user_request = {
        "username": "username",
        "email": "username@email.com",
        "password": "123",
        "dsr_group": "",
        "first_name": "firstname",
        "last_name": "lastname"
    }

    def setUp(self):
        self.dsr_admin = UserFactory.create(
            group=DsrGroupFactory.create(
                slug_field=settings.DSR_ADMIN_SLUG_FIELD,
                linked_group__name=settings.DSR_ADMIN_GROUP_NAME,
                custom_user_permissions=[
                    settings.CAN_ADD_DSR_EMPLOYEE_NAME
                ],
            )
        )

        self.dsr_employee = UserFactory.create(
            group=DsrGroupFactory.create(
                slug_field=settings.DSR_EMPLOYEE_SLUG_FIELD,
                linked_group__name=settings.DSR_EMPLOYEE_GROUP_NAME,
                custom_user_permissions=[
                    # Add User Permissions
                ],
            )
        )

        self.dsr_customer_super_admin = UserFactory.create(
            group=DsrGroupFactory.create(
                slug_field=settings.DSR_CUSTOMER_SUPER_ADMIN_SLUG_FIELD,
                linked_group__name=settings.DSR_CUSTOMER_SUPER_ADMIN_GROUP_NAME,
                custom_user_permissions=[
                    # Add User Permissions
                    settings.CAN_ADD_DSR_CUSTOMER_ADMIN_NAME,
                    settings.CAN_ADD_DSR_CUSTOMER_USER_NAME
                ],
            )
        )

        self.dsr_customer_admin = UserFactory.create(
            group=DsrGroupFactory.create(
                slug_field=settings.DSR_CUSTOMER_ADMIN_SLUG_FIELD,
                linked_group__name=settings.DSR_CUSTOMER_ADMIN_GROUP_NAME,
                custom_user_permissions=[
                    # Add User Permissions
                    settings.CAN_ADD_DSR_CUSTOMER_USER_NAME
                ],
            )
        )

        self.dsr_customer_user = UserFactory.create(
            group=DsrGroupFactory.create(
                slug_field=settings.DSR_CUSTOMER_USER_SLUG_FIELD,
                linked_group__name=settings.DSR_CUSTOMER_USER_GROUP_NAME,
                custom_user_permissions=[
                    # Add User Permissions
                ],
            )
        )

    def _test_create_user_no_company_view_permissions(self, user, data, expected_status_code, response_keys=None):
        self.client.force_authenticate(user=user)
        response = self.client.post(reverse('create-users-no-company'), data, format='json')

        self.assertEqual(response.status_code, expected_status_code, response.content)

        if response_keys:
            for key in response_keys:
                response_field = response.json()[key]
                self.assertIsNotNone(response_field)

    """
    DSR Admin User No Company creation tests
    """

    def test_dsr_admin_cant_create_dsr_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_admin_can_create_dsr_employee_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_EMPLOYEE_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_201_CREATED,
            response_keys=('id', 'email', 'username', 'first_name', 'last_name')
        )

    def test_dsr_admin_cant_create_dsr_customer_super_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_SUPER_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_admin_cant_create_dsr_customer_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_admin_cant_create_dsr_customer_user_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_USER_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    """
    DSR Employee User No Company creation tests
    """

    def test_dsr_employee_cant_create_dsr_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_employee,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_employee_cant_create_dsr_employee_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_EMPLOYEE_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_employee,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_employee_cant_create_dsr_customer_super_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_SUPER_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_employee,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_employee_cant_create_dsr_customer_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_employee,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_employee_cant_create_dsr_customer_user_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_USER_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_employee,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    """
    DSR Customer Super Admin User No Company creation tests
    """

    def test_dsr_customer_super_admin_cant_create_dsr_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_super_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_customer_super_admin_cant_create_dsr_employee_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_EMPLOYEE_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_super_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_customer_super_admin_cant_create_dsr_customer_super_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_SUPER_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_super_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_customer_super_admin_cant_create_dsr_customer_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_super_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_customer_super_admin_cant_create_dsr_customer_user_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_USER_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_super_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    """
    DSR Customer Admin User No Company creation tests
    """

    def test_dsr_customer_admin_cant_create_dsr_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_customer_admin_cant_create_dsr_employee_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_EMPLOYEE_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_customer_admin_cant_create_dsr_customer_super_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_SUPER_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_customer_admin_cant_create_dsr_customer_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_customer_admin_cant_create_dsr_customer_user_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_USER_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_admin,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    """
    DSR Customer User User No Company creation tests
    """

    def test_dsr_customer_user_cant_create_dsr_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_user,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_customer_user_cant_create_dsr_employee_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_EMPLOYEE_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_user,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_customer_user_cant_create_dsr_customer_super_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_SUPER_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_user,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_customer_user_cant_create_dsr_customer_admin_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_ADMIN_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_user,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

    def test_dsr_customer_user_cant_create_dsr_customer_user_no_company(self):
        self.valid_add_user_request['dsr_group'] = settings.DSR_CUSTOMER_USER_SLUG_FIELD
        self._test_create_user_no_company_view_permissions(
            user=self.dsr_customer_user,
            data=self.valid_add_user_request,
            expected_status_code=status.HTTP_403_FORBIDDEN,
            response_keys=('detail',)
        )

