from django.urls import path
from .views import dashboardView

app_name = "dashboard"

urlpatterns = [
    path("", dashboardView)
]