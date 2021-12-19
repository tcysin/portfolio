from django.urls import path

from . import views

urlpatterns = [
    path("", views.upload, name="duplicate-detection"),
    path("results/", views.detect, name="results"),
]
