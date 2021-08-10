from django import forms
from django.conf import settings
from django.core.mail import send_mail


class ContactForm(forms.Form):
    email = forms.EmailField(max_length=70, label_suffix="")
    subject = forms.CharField(required=False, max_length=100, label_suffix="")
    message = forms.CharField(
        max_length=3000,
        widget=forms.Textarea,
        label_suffix="",
    )

    def send_email(self):
        """Send email to my personal address using form data."""

        sender = self.cleaned_data.get("email")
        # TODO clean subject field?
        subject = self.cleaned_data.get("subject", "Email from personal website")
        # TODO clean message?
        message = self.cleaned_data.get("message")
        me = settings.MY_PERSONAL_EMAIL

        send_mail(subject, message, sender, [me])
