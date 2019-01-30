import uuid

import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager,
    Group)
from django.db import models, transaction


class UserQuerySet(models.QuerySet):
    def active_and_not_deleted(self):
        return self.filter(is_deleted=False, is_active=True)


class UserManager(BaseUserManager):

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db).active_and_not_deleted()

    def create_user_no_company(self, username, email, password, first_name=None, last_name=None, dsr_group=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        with transaction.atomic():
            user.set_password(password)
            user.save()

            if dsr_group:
                user.groups.add(dsr_group)

            user.save()

        return user

    def create_user_with_company(self, username, email, password, dsr_group, first_name, last_name, company):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            company=company
        )

        with transaction.atomic():
            user.set_password(password)
            user.save()

            if dsr_group:
                user.groups.add(dsr_group)

            user.save()

        return user


class User(AbstractUser):
    # Date the User was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Date the User info was last updated
    updated_at = models.DateTimeField(auto_now=True)

    # Date the User last logged into the app
    last_active = models.DateTimeField(auto_now=True)

    # Indicates whether this users has been deleted or not
    is_deleted = models.BooleanField(default=False)

    first_name = models.CharField(max_length=64, blank=True, null=True)

    last_name = models.CharField(max_length=64, blank=True, null=True)

    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    class Meta:
        # Extra permissions user actions based on groups
        permissions = (
            # DSR Admin
            (settings.CAN_ADD_DSR_ADMIN_PERM, settings.CAN_ADD_DSR_ADMIN_NAME),
            (settings.CAN_DELETE_DSR_ADMIN_PERM, settings.CAN_DELETE_DSR_ADMIN_NAME),
            (settings.CAN_UPDATE_DSR_ADMIN_PERM, settings.CAN_UPDATE_DSR_ADMIN_NAME),
            # DSR Employee
            (settings.CAN_ADD_DSR_EMPLOYEE_PERM, settings.CAN_ADD_DSR_EMPLOYEE_NAME),
            (settings.CAN_DELETE_DSR_EMPLOYEE_PERM, settings.CAN_DELETE_DSR_EMPLOYEE_NAME),
            (settings.CAN_UPDATE_DSR_EMPLOYEE_PERM, settings.CAN_UPDATE_DSR_EMPLOYEE_NAME),
            # DSR Customer Super User
            (settings.CAN_ADD_DSR_CUSTOMER_SUPER_ADMIN_PERM, settings.CAN_ADD_DSR_CUSTOMER_SUPER_ADMIN_NAME),
            (settings.CAN_DELETE_DSR_CUSTOMER_SUPER_ADMIN_PERM, settings.CAN_DELETE_DSR_CUSTOMER_SUPER_ADMIN_NAME),
            (settings.CAN_UPDATE_DSR_CUSTOMER_SUPER_ADMIN_PERM, settings.CAN_UPDATE_DSR_CUSTOMER_SUPER_ADMIN_NAME),
            # DSR Customer Admin
            (settings.CAN_ADD_DSR_CUSTOMER_ADMIN_PERM, settings.CAN_ADD_DSR_CUSTOMER_ADMIN_NAME),
            (settings.CAN_DELETE_DSR_CUSTOMER_ADMIN_PERM, settings.CAN_DELETE_DSR_CUSTOMER_ADMIN_NAME),
            (settings.CAN_UPDATE_DSR_CUSTOMER_ADMIN_PERM, settings.CAN_UPDATE_DSR_CUSTOMER_ADMIN_NAME),
            # DSR Customer User
            (settings.CAN_ADD_DSR_CUSTOMER_USER_PERM, settings.CAN_ADD_DSR_CUSTOMER_USER_NAME),
            (settings.CAN_DELETE_DSR_CUSTOMER_USER_PERM, settings.CAN_DELETE_DSR_CUSTOMER_USER_NAME),
            (settings.CAN_UPDATE_DSR_CUSTOMER_USER_PERM, settings.CAN_UPDATE_DSR_CUSTOMER_USER_NAME),
        )
