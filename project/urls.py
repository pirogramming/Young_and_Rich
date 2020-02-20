from django import core
from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from core.views import profile, sign_in, profile_edit, profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('core/', include('core.urls')),
    path('comp/', include('comp.urls')),
    path('community/', include('community.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile', profile, name='profile'),
    path('accounts/profile/<str:username>', profile_view, name='profile_view'),
    path('accounts/login', sign_in, name='sign_in'),
    path('accounts/profile_edit', profile_edit, name='profile_edit'),
    path("", lambda req: redirect("main:main")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
