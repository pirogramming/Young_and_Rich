from django.urls import path
from . import views
from .views import progressbar

app_name = 'comp'

urlpatterns = [
    path('comp/progressbar/<int:pk>/', progressbar, name='progressbar'),
]