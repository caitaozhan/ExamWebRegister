from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^examinations$', views.examinations, name='examinations'),
    url(r'^begin_registration$', views.begin_registration, name='begin_registration'),
    url(r'^select_for_examination', views.select_for_examination, name='select_for_examination'),
    url(r'^select_for_place$', views.select_for_place, name='select_for_place'),
    url(r'^fill_registration_form$', views.fill_registration_form, name='fill_registration_form'),
    url(r'^save_registration_form$', views.save_registration_form, name='save_registration_form'),
]
