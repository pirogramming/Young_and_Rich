from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('comp/', include('comp.urls')),
    path('community/', include('community.urls')),
    path('accounts/', include('allauth.urls')),
]
