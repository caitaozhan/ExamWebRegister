from django.conf.urls import url, include

from . import views

urlpatterns = [
	url(r'^', include('django.contrib.auth.urls')),
	url(r'^signup$', views.add_user, name='add_user'),
    url(r'^profile$', views.profile, name='user_profile'),
]