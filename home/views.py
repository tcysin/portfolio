from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import FormView

from .forms import ContactForm


class ContactView(FormView):
    template_name = "home/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # all the valid form data is in .cleaned_data attr
        # if form is valid, send a message
        # if FormView().form_valid(form):
        #   ...
        return HttpResponseRedirect(reverse("home"))
