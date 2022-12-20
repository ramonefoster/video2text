from django.urls import path, include
from . import views

urlpatterns = [
    path("", view=views.IndexView.as_view(), name="index"),
    path("converted", view=views.IndexView.as_view(), name="converter_url"),
    path("converted/<slug:slug>", view=views.ViewSingle.as_view(), name="post_url"),

]
