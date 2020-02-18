from django.urls import path
from . import views
from .views import sign_in, profile, show_user_rank

app_name = 'core'

urlpatterns = [
    path('rank', show_user_rank, name='show_user_rank'),
]