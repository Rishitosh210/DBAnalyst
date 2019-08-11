"""audtech_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from audtech_app import views
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    # path('api/user/', views.UserCRUD),
    path('api/user/list/', views.UserList.as_view()),
    path('api/user/detail/<int:pk>/', views.UserDetail.as_view()),
    path('api/user/update/<int:pk>/', views.UserUpdate.as_view()),
    path('api/user/delete/<int:pk>/', views.UserDelete.as_view()),
    # path('upload-data/', views.process_file, name="upload-data"),
]
