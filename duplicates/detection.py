"""
This module contains functionality for finding duplicated and near-duplicated
images.

TODO better description
TODO which methods do we use here?
"""

from collections import defaultdict
from typing import Dict, Iterable, List

import numpy as np
from PIL import Image
from scipy import spatial


def dHash(image: Image.Image):
    """
    Return dHash array for given PIL Image.

    We compute standard 64-bit difference hash using `Image.BOX` interpolation.

    For detailed discussion of dHash algorithm see
    http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html.

    This implementation is heavily inspired by `ImageHash` library at
    https://pypi.org/project/ImageHash/.

    Returns:
        boolean 1-D ndarray of size 64.
    """

    # convert the image to grayscale and resize the grayscale image,
    # adding a single column (width) so we can compute the horizontal
    # gradient
    gray = image.convert("L")
    resized = gray.resize((9, 8), resample=Image.BOX)
    pixels = np.asarray(resized)

    # compute the (relative) horizontal gradient between adjacent
    # column pixels
    diff = pixels[:, :-1] < pixels[:, 1:]

    return np.ravel(diff)


def distance_matrix(X, metric="euclidean"):
    """
    Return square distance matrix between rows of X.

    Args:
        X (array-like): M by N array of M original observations in an
            N-dimensional space.
        metric (str): the distance metric to use.
            See docs for `scipy.spatial.distance.pdist`.

    Returns:
        Y (ndarray): square distance matrix of shape (M, M).
    """

    condensed = spatial.distance.pdist(X, metric=metric)
    return spatial.distance.squareform(condensed)


def duplicate_matrix(X: np.ndarray, threshold: float):
    """
    Return matrix of duplicates from distance matrix X.

    We mark both vectors as duplicates when the distance between them is
    smaller than the threshold.

    Args:
        X: distance matrix of shape (M, M).
        threshold (float): cutoff threshold for duplicated vectors.

    Returns:
        Y (ndarray): boolean matrix of shape (M, M).
    """

    return X < threshold


def duplicates_dict(X: np.ndarray) -> Dict[int, List[int]]:
    """
    Return duplicates dictionary from a matrix of duplicates.

    Each key is an index of original vector, while value is a list of
    vector indices we consider duplicates.

    Args:
        X (ndarray): boolean duplicate matrix of shape (M, M).
    """

    # TODO is logic ok? is it what we want?

    dict_dups = defaultdict(list)
    dups = set()  # keep track of duplicates
    n = len(X)

    for row in range(n - 1):  # skip last row

        if row in dups:
            continue

        for col in range(row + 1, n):  # start one past diagonal

            if X[row, col] == True:  # noqa E712
                dict_dups[row].append(col)
                dups.add(col)  # mark j as a duplicate

    return dict(dict_dups)  # freeze final dict


def find_duplicates(
    images: Iterable[Image.Image], threshold: float = 0.16
) -> Dict[str, List[str]]:
    """
    Find duplicated or near-duplicated images.

    Resulting dictionary may be empty if there are no duplicated images
    or initial iterable is empty.

    We utilize dHash method to get 64-bit perceptive hashes of given images
    and compare them using Hamming distance metric.

    Args:
        images: iterable of PIL Images with non-empty `filename` attribute.
        threshold: cutoff threshold for duplicated hashes.
            A fraction of bits that differs between two hashes (scaled
            Hamming distance). Must be between 0 and 1.

    Returns:
        dict: dictionary with filenames for original and duplicated images.
            Each key is a filename of original image, while value is a list
            of filenames marked as duplicates.
    """

    filenames = []
    hashes = []

    for image in images:
        filenames.append(image.filename)
        hashes.append(dHash(image))

    # TODO is this a good design?
    if len(hashes) == 0:
        return {}

    hashes = np.vstack(hashes)  # convert to (M,64) bool ndarray
    M = distance_matrix(hashes, metric="hamming")  # (M,M) float in [0.0, 1.0]
    D = duplicate_matrix(M, threshold)
    dups_dict = duplicates_dict(D)
    result = {
        filenames[orig]: [filenames[i] for i in dups]
        for orig, dups in dups_dict.items()
    }

    return result
