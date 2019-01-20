from rest_framework import serializers

from company.models import CompanyModule


class CompanyModuleSerializer(serializers.ModelSerializer):
    """
    CompanyModule Serializer
    """

    class Meta:
        model = CompanyModule
        fields = ['id', 'name', 'slug_field', ]
