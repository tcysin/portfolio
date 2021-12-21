"""
This module contains helper functionality for safely dealing with image
uploads.
"""

import warnings
from typing import Generator, Sequence, Union

from django.core.files.uploadedfile import UploadedFile
from PIL import Image, UnidentifiedImageError

# see `open_images` comments for details
warnings.simplefilter("error", Image.DecompressionBombWarning)


def open_image(file: UploadedFile) -> Union[Image.Image, None]:
    """
    Try to open a file as a PIL Image and return it; return None if it fails.
    """

    # TODO should i move this to `open_images` instead?

    try:
        image = Image.open(file)
    except UnidentifiedImageError:
        # TODO the image cannot be opened and identified; happens if
        #  supplied file is not a valid image
        return None
    except FileNotFoundError:
        # TODO something happened with the UploadedFile; this should NEVER happen
        return None
    except Image.DecompressionBombWarning:
        # TODO someone is trying to bomb us; handle it (log / issue message, etc)
        # for more info on related warning and error at
        # https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.open
        return None
    else:
        return image


def open_images(
    uploaded_files: Sequence[UploadedFile],
    maxsize: int = 1024 * 1024 * 10,
) -> Generator[Image.Image, None, None]:
    """
    Return a generator that tries to open each file in a sequence as PIL Image.

    It skips files that PIL cannot open, as well as files that are too big.
    Each yielded image instance has `filename` atribute set to corresponding
    file's `name` attribute.

    Args:
        uploaded_files: a list of `UploadedFile` objects.
        maxsize: maximum allowed size (in bytes) of a file.
            Defaults to 10Mb.
    """

    # TODO better name for this function?
    # TODO preconditions? checks

    for file in uploaded_files:
        if file.size <= maxsize:
            image = open_image(file)

            if image is not None:
                image.filename = file.name
                yield image
