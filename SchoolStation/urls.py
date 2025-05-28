"""
URL configuration for SchoolStation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path

from main.views import index,docs,info

from api.views import ( DATTAPIVIEVSET, CheckUserExists, RegisterUser,
                        UpdateTelegramIDView, UpdateAddrView, GetUserProfile,
                        GetSensorData, GetPastSensorData)

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'sensors', DATTAPIVIEVSET)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('docs/', docs, name='docs'),
    path('info/', info, name='info'),
    path('users/', include('users.urls', namespace='users')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/check-user/', CheckUserExists.as_view(), name='check_user_exists'),
    path('api/v1/register/', RegisterUser.as_view(), name='register_user'),
    path('api/v1/update-telegram-id/', UpdateTelegramIDView.as_view(), name='update_telegram_id'),
    path('api/v1/update-addr/', UpdateAddrView.as_view(), name='update_addr'),
    path('api/v1/profile/', GetUserProfile.as_view(), name='get_profile'),
    path('api/v1/sensor/latest/', GetSensorData.as_view(), name='get_latest_sensor_data'),
    path('api/v1/sensor/history/', GetPastSensorData.as_view(), name='get_sensor_history'),
]
