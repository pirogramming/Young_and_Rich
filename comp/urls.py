from django.urls import path
from . import views

app_name = 'comp'

urlpatterns = [
    path("", views.comp_list, name="comp_list"),
    path("<int:pk>/overview/", views.comp_detail_overview, name="comp_overview"),
    path("<int:pk>/data/", views.comp_detail_data, name="comp_data"),
    path("<int:pk>/community/", views.comp_detail_community_list, name="comp_community_list"),
    path("<int:pk>/community/<int:pk2>/", views.comp_detail_community_detail, name="comp_community_detail"),
    path("<int:pk>/ranking/", views.comp_ranking, name="comp_ranking"),
]