from django.contrib import admin

from .models import ExamInfoModel, PlaceModel

# Register your models here.

admin.site.register(ExamInfoModel)
admin.site.register(PlaceModel)