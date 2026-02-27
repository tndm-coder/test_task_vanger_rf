from django.urls import path

from .views import slider_page

app_name = "slider"

urlpatterns = [
    path("", slider_page, name="page"),
]
