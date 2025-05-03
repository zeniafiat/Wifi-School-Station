from django.urls import path
from users.views import login, registrarion, logout

app_name = 'users'

urlpatterns = [
    path('login/', login, name = 'login'),
    path('registration/', registrarion, name = 'registration'),
    path('logout/', logout, name='logout')
]
