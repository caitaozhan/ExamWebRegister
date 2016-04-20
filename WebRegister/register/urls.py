from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^examinations$', views.examinations, name='examinations'),
]
