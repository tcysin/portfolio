from django import forms


class ImageUploadForm(forms.Form):
    images = forms.ImageField(
        label_suffix="",
        widget=forms.ClearableFileInput(
            attrs={"multiple": True},  # TODO limit accepted types?
        ),
    )
