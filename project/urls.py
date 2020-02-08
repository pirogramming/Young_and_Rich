from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core.views import profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('comp/', include('comp.urls')),
    path('community/', include('community.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile', profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
