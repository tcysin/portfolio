from django.urls import reverse_lazy
from django.views.generic import FormView
from PIL import Image

from .forms import ImageUploadForm


class ImageUploadView(FormView):
    form_class = ImageUploadForm
    success_url = reverse_lazy("success")
    template_name = "duplicates/duplicates.html"

    # TODO on valid form, redirect a user to a page with an image
    def form_valid(self, form):
        # ImageField normalizes its inputs to UploadedFile with .image attr
        # see https://docs.djangoproject.com/en/3.2/ref/forms/fields/#imagefield
        uploaded_file = form.cleaned_data["image"]
        print(uploaded_file.name)
        print(type(uploaded_file))

        # convert to PIL image
        im = Image.open(uploaded_file)
        print(type(im), im.size)

        # TODO use your routine to find duplicates
        # TODO render template with results in the same response, without redirect?

        return super().form_valid(form)
