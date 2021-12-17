from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import ImageUploadForm
from .helpers import open_images


class ImageUploadView(FormView):
    form_class = ImageUploadForm
    success_url = reverse_lazy("duplicate-detection")
    template_name = "duplicates/duplicates.html"

    # TODO on valid form, redirect a user to a page with an image
    def form_valid(self, form):
        # for more info about uploading multiple files, see
        # https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/#uploading-multiple-files
        uploaded_files = self.request.FILES.getlist("images")

        # try to open files as PIL images
        gen = open_images(uploaded_files, maxsize=settings.IMAGE_UPLOAD_MAX_MEMORY_SIZE)

        for im in gen:
            print(im.filename, im.size, im.mode)

        # TODO validate uploaded files manually
        # for discussion why validation on multiple files is not run automatically, see
        # https://stackoverflow.com/a/46409022 and https://github.com/django/django/pull/9011
        # TODO some potential image files might be corrupted / not images at all
        # TODO security
        # TODO make sure there is at least two images

        return super().form_valid(form)
