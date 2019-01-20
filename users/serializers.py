from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth import authenticate

from dsr_api.settings import DSR_ADMIN_SLUG_FIELD, DSR_EMPLOYEE_SLUG_FIELD, DSR_CUSTOMER_ADMIN_SLUG_FIELD, \
    DSR_CUSTOMER_USER_SLUG_FIELD
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Creates a new User account without a company
    """
    dsr_group = serializers.SlugRelatedField(
        queryset=Group.objects.none(),
        slug_field='dsrgroup__slug_field',
        write_only=True,
        error_messages={
            'does_not_exist': "DSR Group does not exist."
        }
    )

    DSR_GROUPS = [DSR_ADMIN_SLUG_FIELD, DSR_EMPLOYEE_SLUG_FIELD]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        q_objects = Q()
        for g in self.DSR_GROUPS:
            q_objects.add(Q(dsrgroup__slug_field=g), Q.OR)
        self.fields['dsr_group'].queryset = Group.objects.filter(q_objects)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'dsr_group']
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user_no_company(**validated_data)


class CompanyUserSerializer(UserSerializer):
    """
    Creates a new user with a company
    """
    DSR_GROUPS = [DSR_CUSTOMER_ADMIN_SLUG_FIELD, DSR_CUSTOMER_USER_SLUG_FIELD]

    company = serializers.CharField()

    class Meta:
        fields = UserSerializer.Meta.fields + ['company', ]

    def create(self, validated_data):
        return User.objects.create_user_with_company(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    first_name = serializers.CharField(max_length=128, read_only=True)
    last_name = serializers.CharField(max_length=128, read_only=True)
    token = serializers.CharField(max_length=128, read_only=True)

    def validate(self, data):
        user = authenticate(username=data.get('username', None), password=data.get('password', None))

        if user is None:
            raise serializers.ValidationError(
                'A users with this email and password was not found.'
            )

        return {
            'token': user.token,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
