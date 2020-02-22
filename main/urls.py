from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path("", views.main, name="main"),
    path("explanation/page", views.explanation_page, name="explanation_page"),
    path("explanation/competition", views.explanation_competition, name="explanation_competition"),
    path("explanation/faq", views.explanation_faq, name="explanation_faq"),
]
