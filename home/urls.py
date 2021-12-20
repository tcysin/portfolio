from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from .views import ContactView

urlpatterns = [
    path(
        "",
        cache_page(60 * 60 * 4)(TemplateView.as_view(template_name="home/home.html")),
        name="home",
    ),
    path(
        "privacy-policy/",
        cache_page(60 * 60 * 4)(
            TemplateView.as_view(template_name="home/privacy-policy.html")
        ),
        name="privacy-policy",
    ),
    path(
        "contact/",
        ContactView.as_view(),
        name="contact",
    ),
    path(
        "success/",
        cache_page(60 * 60 * 4)(
            TemplateView.as_view(template_name="home/success.html")
        ),
        name="success",
    ),
]
