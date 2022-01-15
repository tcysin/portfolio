from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path("", cache_page(60 * 60 * 4)(views.upload), name="duplicate-detection"),
    path("results/", views.detect, name="results"),
]
