from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import UserPermissionsNoCompany
from users.serializers import LoginSerializer, UserSerializer, CompanyUserSerializer


class ListCreateUserNoCompanyAPIView(ListCreateAPIView):
    """
    Creates a new User Account.

    Accepted account types;
        - DSR Admin
        - DSR Employee

    POST - Creates a new user with no company
           Required permission;
            - Can add DSR Customer Admin
            OR
            - Can add DSR Customer User

    GET - Lists users associated with company that the user is.
          Required permission;
            - Can view DSR Customer Admin
            OR/AND
            - Can view DSR Customer User
    """

    permission_classes = (
        IsAuthenticated,
        UserPermissionsNoCompany
    )
    serializer_class = UserSerializer


class ListCreateUserWithCompanyAPIView(ListCreateAPIView):
    """
    Creates a new User Account for a company.

    Accepted account types;
        - DSR Customer Admin
        - DSR Customer User

    POST - Creates a new user with no company
            Required permission;
            - Can add DSR Customer Admin
            OR
            - Can add DSR Customer User
    GET - Lists users with no company
    """
    serializer_class = CompanyUserSerializer


class LoginAPIView(APIView):
    """
    View for authenticating all Users.
    """
    permission_classes = (
        AllowAny,
    )
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
