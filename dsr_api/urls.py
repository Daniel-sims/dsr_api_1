from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from users import views as user_views
from company import views as company_views

urlpatterns = [

    path('admin/', admin.site.urls),

    # Users
    path('users/login/', user_views.LoginAPIView.as_view(), name="login"),

    path('users/', user_views.CreateUserNoCompanyAPIView.as_view(), name="create-users-no-company"),
    path('company/<int:pk>/users/', user_views.CreateUserWithCompanyAPIView.as_view(), name="create-users-with-company"),

    # Company Modules
    path('modules/', company_views.GetCompanyModulesAPIView.as_view(), name="company-modules"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
