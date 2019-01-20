from django.db import models


class CompanyModuleQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class CompanyModuleManager(models.Manager):

    def get_queryset(self):
        return CompanyModuleQuerySet(self.model, using=self._db).active()


class CompanyModule(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    slug_field = models.SlugField(max_length=100, blank=False, null=False)
    image_url = models.CharField(max_length=256, blank=False, null=False)

    is_active = models.BooleanField(default=True)

    objects = CompanyModuleManager()

    def __str__(self):
        return self.name
