from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import ContactForm


class ContactView(FormView):
    template_name = "home/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        """If the form is valid, send email and redirect to success url."""
        form.send_email()
        return FormView.form_valid(self, form)
