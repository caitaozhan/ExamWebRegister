from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
   # url(r'^add_exam$', views.add_exam, name='add_exam'),
]
