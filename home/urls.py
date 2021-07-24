from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="home/home.html"),
        name="home",
    ),
    path(
        "privacy-policy/",
        TemplateView.as_view(template_name="home/privacy-policy.html"),
        name="privacy-policy",
    ),
]
