from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from core.views import profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('core/', include('core.urls')),
    path('comp/', include('comp.urls')),
    path('community/', include('community.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile', profile, name='profile'),

    path("", lambda req: redirect("main:main")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
