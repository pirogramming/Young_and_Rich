from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path("", views.main, name="main"),
    path("notice_list/", views.notice_list, name="notice_list"),
    path("notice_detail/<int:pk>/", views.notice_detail, name="notice_detail"),
]