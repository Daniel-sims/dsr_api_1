from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from company.models import CompanyModule
from company.serializers import CompanyModuleSerializer


class GetCompanyModulesAPIView(ListAPIView):
    """
    Gets all modules which can be added to a company.

    """

    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = CompanyModuleSerializer
    queryset = CompanyModule.objects.all()
