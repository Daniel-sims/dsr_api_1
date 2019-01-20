from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AemGroupQuerySet(models.QuerySet):
    def for_company(self):
        return self.filter()


class AemGroupManager(models.Manager):

    def get_queryset(self):
        return AemGroupQuerySet(self.model, using=self._db).for_company()


class DsrGroup(models.Model):
    linked_group = models.ForeignKey(Group, related_name='dsrgroup', on_delete=models.CASCADE)
    slug_field = models.SlugField(unique=True)

    objects = AemGroupManager()

    def __str__(self):
        return self.slug_field
