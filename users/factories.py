from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
import factory
from factory import lazy_attribute
from faker import Faker

from groups.models import DsrGroup
from users.models import User

FAKER = Faker(locale='en_US')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = lazy_attribute(lambda x: FAKER.name())
    password = 'Password01'
    email = lazy_attribute(lambda a: '{0}@example.com'.format(a.username).lower())

    @factory.post_generation
    def group(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.groups.add(extracted.linked_group)


class GroupsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group
        django_get_or_create = ('name',)

    name = ""


class DsrGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DsrGroup
        django_get_or_create = ('slug_field',)

    linked_group = factory.SubFactory(GroupsFactory)
    slug_field = ""

    @factory.post_generation
    def custom_user_permissions(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for name in extracted:
                self.linked_group.permissions.add(
                    Permission.objects.get(
                        name=name
                    )
                )
