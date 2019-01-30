from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from company.models import CompanyModule, Company
from users.models import User


class CompanyModuleSerializer(serializers.ModelSerializer):
    """
    CompanyModule Serializer
    """

    class Meta:
        model = CompanyModule
        fields = ['id', 'name', 'slug_field', ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(write_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'user', 'modules']
        read_only_fields = ('id',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        context = kwargs.get('context', None)
        if context:
            request = kwargs['context']['request']

            if request.method == 'POST':
                self.fields['modules'] = PrimaryKeyRelatedField(many=True, queryset=CompanyModule.objects.all())
            elif request.method == 'GET':
                self.fields['modules'] = CompanyModuleSerializer(many=True)

    def create(self, validated_data):
        modules = validated_data.pop('modules')
        company = Company.objects.create_company(**validated_data)

        if modules:
            for module in modules:
                company.modules.add(module)

        self.fields['modules'] = CompanyModuleSerializer(many=True)

        return company
