from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^signup$', views.sign_up, name='signup'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^logout$', views.log_out, name='logout'),
    url(r'^login$', views.log_in, name='login'),
]
