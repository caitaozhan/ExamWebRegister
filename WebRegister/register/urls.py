from django.conf.urls import url, include
from django.contrib.auth import urls

from . import views

# app_name = 'register'

urlpatterns = [
    url(r'$', views.index, name='index'),
    url(r'', include('django.contrib.auth.urls')),
    url(r'signup$', views.add_user, name='add_user'),
    url(r'profile$', views.profile, name='user_info'),
    url(r'add_exam$', views.add_exam, name='add_exam'),
]