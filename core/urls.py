from django.urls import path
from . import views
from .views import sign_in, profile

app_name = 'core'

urlpatterns = [
    path('accounts/login', sign_in, name='sign_in'),
]