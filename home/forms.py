from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(max_length=70, label_suffix="")
    subject = forms.CharField(required=False, max_length=100, label_suffix="")
    message = forms.CharField(
        max_length=3000,
        widget=forms.Textarea,
        label_suffix="",
    )
    # cc_myself = forms.BooleanField(required=False, label_suffix="?")
