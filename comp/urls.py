from django.urls import path
from . import views

app_name = 'comp'

urlpatterns = [
    path("", views.comp_list, name="comp_list"),
]