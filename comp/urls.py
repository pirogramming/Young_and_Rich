from django.urls import path
from . import views
from .views import progressbar

app_name = 'comp'

urlpatterns = [
    path('comp/progressbar/<int:pk>/', progressbar, name='progressbar'),
    path("", views.comp_list, name="comp_list"),
    path("<int:pk>/overview/", views.comp_detail_overview, name="comp_overview"),
    path("<int:pk>/data/", views.comp_detail_data, name="comp_data"),
    path("<int:pk>/community/", views.comp_detail_community_list, name="comp_community_list"),
]