"""
This module contains helper functionality for safely dealing with image
uploads.
"""

import warnings
from typing import Generator, Sequence

from django.core.files.uploadedfile import UploadedFile
from PIL import Image, UnidentifiedImageError

# see `open_images` comments for details
warnings.simplefilter("error", Image.DecompressionBombWarning)


def open_images(
    uploaded_files: Sequence[UploadedFile],
    max_size: int = 1024 * 1024 * 10,
) -> Generator[Image.Image, None, None]:
    """
    Return a generator that tries to open each file in a sequence as PIL Image.

    It skips files that PIL cannot open, as well as files that are too big.
    Each yielded image instance has `filename` atribute set to corresponding
    file's `name` attribute.

    Args:
        uploaded_files: a list of `UploadedFile` objects.
        max_size: maximum allowed size (in bytes) of a file.
            Defaults to 10Mb.
    """

    # TODO better name for this function?

    for file in uploaded_files:
        if file.size <= max_size:
            try:
                image = Image.open(file)
            except (
                UnidentifiedImageError,  # supplied file is not a valid image
                FileNotFoundError,  # should never happen
                Image.DecompressionBombWarning,  # someone is trying to bomb us
            ):
                pass
            else:
                image.filename = file.name
                yield image
