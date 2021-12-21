import time
from itertools import chain
from operator import attrgetter

from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .detection import find_duplicates
from .forms import ImageUploadForm
from .helpers import open_images


def upload(request):
    """
    View with upload form for images.

    Initialize and display a an empty form for image upload to a user.
    """
    form = ImageUploadForm()
    return render(request, "duplicates/upload.html", {"form": form})


# TODO better name for this view?
def detect(request):
    """
    Process POST request with images and find duplicates.

    On GET or any other request, redirects user to image uploads page.
    """

    if request.method == "POST":
        start = time.thread_time()
        # in-built checks for multiple image files are useless,
        # so we skip form instantiation and validation

        # for more info about uploading multiple files, see
        # https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/#uploading-multiple-files
        uploaded_files = request.FILES.getlist("images")  # may be empty
        uploaded_files = sorted(uploaded_files, key=attrgetter("name"))
        # TODO what to do if uploaded list is empty?

        # TODO validate uploaded files manually
        # for discussion why validation on multiple files is not run automatically, see
        # https://stackoverflow.com/a/46409022 and https://github.com/django/django/pull/9011
        # TODO some potential image files might be corrupted / not images at all
        # TODO security
        # TODO make sure there is at least two images
        # TODO tell user about this stuff

        # safely open uploaded files as PIL Images
        gen = open_images(uploaded_files, maxsize=settings.IMAGE_UPLOAD_MAX_MEMORY_SIZE)

        # find duplicated images
        # TODO log time
        dups_dict = find_duplicates(gen, threshold=settings.THRESHOLD)
        filenames = sorted(
            set(filename for filename in chain.from_iterable(dups_dict.values()))
        )

        # TODO option to save results as .txt file
        # TODO option to save results as .zip archive

        return render(
            request,
            "duplicates/results.html",
            context={
                "result": "\n".join(filenames),
                "elapsed": round(time.thread_time() - start, 3),
            },
        )

    # if GET (or any other method) send user back to upload page
    else:
        return HttpResponseRedirect(reverse("duplicate-detection"))
