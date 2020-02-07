from django.urls import path
from . import views

app_name = 'comp'

urlpatterns = [
    path("", views.comp_list, name="comp_list"),
    path("<int:pk>/overview/", views.comp_detail_overview, name="comp_overview"),
    path("<int:pk>/overview/description", views.comp_detail_overview_description, name="comp_description"),
    path("<int:pk>/overview/evaluation", views.comp_detail_overview_evaluation, name="comp_evaluation"),
    path("<int:pk>/overview/timeline", views.comp_detail_overview_timeline, name="comp_timeline"),
    path("<int:pk>/overview/prizes", views.comp_detail_overview_prizes, name="comp_prizes"),
    path("<int:pk>/data/", views.comp_detail_data, name="comp_data"),
    path("<int:pk>/community/", views.comp_detail_community_list, name="comp_community_list"),
    path("<int:pk>/community/<int:pk2>/", views.comp_detail_community_detail, name="comp_community_detail"),
    path("<int:pk>/ranking/", views.comp_ranking, name="comp_ranking"),
    path("<int:pk>/submit/", views.submit_answer, name="comp_submit_answer"),
    path("<int:pk>/answerlist/", views.answer, name="comp_answerlist")
]
