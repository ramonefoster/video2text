from django.urls import path, include
from . import views

urlpatterns = [
    path("", view=views.IndexView.as_view(), name="index"),
    path("converter", view=views.IndexView.as_view(), name="converter_url")
]
