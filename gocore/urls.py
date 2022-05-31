from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from gocore.settings import DEBUG

urlpatterns = [
    path('admin', admin.site.urls),
    path('dashboard', include("dashboard.urls", namespace="dashboard")),
    path('', include("goshop.urls", namespace="goshop"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)