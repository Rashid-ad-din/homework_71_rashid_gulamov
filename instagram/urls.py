from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from instagram.views import IndexView

urlpatterns = \
    [
        path('admin/', admin.site.urls),
        path("auth/", include('accounts.urls')),
        path("", IndexView.as_view(), name='index'),
        path('api/', include('api.urls')),
        path('rest/', include('rest_framework.urls', namespace='rest_framework'))
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
