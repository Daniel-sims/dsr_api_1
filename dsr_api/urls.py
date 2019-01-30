from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from users import views as user_views
from company import views as company_views

urlpatterns = [

    path('admin/', admin.site.urls),

    # Users
    path(
        'users/login/',
        user_views.LoginAPIView.as_view(),
        name="login"
    ),

    path(
        'users/',
        user_views.ListCreateUserNoCompanyAPIView.as_view(),
        name="list-create-users-no-company"
    ),

    # Company Modules
    path(
        'modules/',
        company_views.ListCompanyModulesAPIView.as_view(),
        name="list-company-modules"
    ),

    # Company
    path(
        'company/',
        company_views.ListCreateCompanyAPIView.as_view(),
        name="create-company"
    ),

    path(
        'company/<int:pk>/',
        company_views.RetrieveUpdateDestroyCompanyAPIView.as_view(),
        name="retrieve-update-destroy-company"
    ),

    path(
        'company/<int:pk>/users/',
        user_views.ListCreateUserWithCompanyAPIView.as_view(),
        name="list-create-users-with-company"
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
