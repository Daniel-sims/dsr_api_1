from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, \
    CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from company.models import CompanyModule, Company
from company.permissions import CanRetrieveUpdateDestroyCompanyPermission, CanListCreateCompanyPermission
from company.serializers import CompanyModuleSerializer, CompanySerializer


class ListCompanyModulesAPIView(ListAPIView):
    """
    Gets all modules which can be added to a company.

    """

    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = CompanyModuleSerializer
    queryset = CompanyModule.objects.all()


class ListCreateCompanyAPIView(CreateAPIView):
    """
    Lists or creates companies.

    """

    permission_classes = (IsAuthenticated, CanListCreateCompanyPermission)
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class RetrieveUpdateDestroyCompanyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, CanRetrieveUpdateDestroyCompanyPermission)
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
