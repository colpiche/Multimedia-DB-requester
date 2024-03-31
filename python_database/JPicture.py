import inspect
import logging
import numpy as np
import os
from PIL import Image


class JPicture:
    """
    JPicture class represents an image processing utility.

    Attributes:
        None

    Methods:
        _compute_histrograms: Computes the histograms of an image.
        _normalize_image: Normalizes the pixel values of an image.
        _rgb_to_luma: Converts an RGB image to grayscale using the luma formula.
        histrograms: Computes the histograms of an image and its grayscale version.
    """

    def __init__(self):
        pass

    def _compute_histograms(self, pixels: np.ndarray, nbins: int) -> np.ndarray:
        """
        Computes the histograms of an image.

        Args:
            pixels (np.ndarray): The pixel values of the image.
            nbins (int): The number of bins for the histograms.

        Returns:
            np.ndarray: The computed histograms with normalized values.
        """

        # Debugging information
        logging.debug(f'{inspect.currentframe().f_code.co_name}()')

        # Initialize bins array
        bins: np.ndarray

        # Check if the image is RGB or grayscale
        if pixels.shape.__len__() == 3:
            # If array is 3D (RGB image)
            bins = self._compute_RGB_histogram(pixels, nbins)
        else:
            # If not (grayscale image)
            bins = self._compute_gray_level_histogram(pixels, nbins)

        # Normalize the histogram by dividing by the total number of pixels
        bins = bins / (pixels.shape[0] * pixels.shape[1])

        # Return the computed histograms
        return bins

def _compute_RGB_histogram(self, pixels: np.ndarray, nbins: int) -> np.ndarray:
    """
    Computes the RGB histogram of an image.

    Args:
        pixels (np.ndarray): The pixel values of the image.
        nbins (int): The number of bins for the histogram.

    Returns:
        np.ndarray: The computed RGB histogram.
    """

    # Debugging information
    logging.debug(f'{inspect.currentframe().f_code.co_name}()')

    # Calculate the dimensions of the bins array
    bins_dimension: tuple = tuple(nbins for _ in range(pixels.shape[2]))

    # Initialize the bins array
    bins: np.ndarray = np.zeros(bins_dimension, dtype=int)

    # Calculate the step size for each bin
    step: float = 1 / nbins

    # Iterate over each pixel in the image
    for line in pixels:
        for pixel in line:
            # Calculate the bin index for each color channel
            red_index: int = int(pixel[0] // step)
            green_index: int = int(pixel[1] // step)
            blue_index: int = int(pixel[2] // step)

            # If the pixel value is the maximum possible value, put it in the last bin
            if red_index == nbins:
                red_index -= 1

            if green_index == nbins:
                green_index -= 1

            if blue_index == nbins:
                blue_index -= 1

            # Increment the corresponding bin
            bins[red_index, green_index, blue_index] += 1

    return bins

    def _compute_gray_level_histogram(self, pixels: np.ndarray, nbins: int) -> np.ndarray:
        """
        Computes the gray level histogram of an image.

        Args:
            pixels (np.ndarray): The pixel values of the image.
            nbins (int): The number of bins for the histogram.

        Returns:
            np.ndarray: The computed gray level histogram.
        """

        # Debugging information
        logging.debug(f'{inspect.currentframe().f_code.co_name}()')

        # Initialize the bins array
        bins: np.ndarray = np.zeros(nbins, dtype=int)

        # Calculate the step size for each bin
        step: float = 1 / nbins

        # Iterate over each pixel in the image
        for line in pixels:
            for pixel in line:
                # Calculate the bin index
                bin_index: int = int(pixel // step)

                # If the pixel value is the maximum possible value, put it in the last bin
                if bin_index == nbins:
                    bin_index -= 1

                # Increment the corresponding bin
                bins[bin_index] += 1

        return bins

    def _normalize_image(self, image: Image.Image) -> np.ndarray:
        """
        Normalizes the pixel values of an image.

        Args:
            image (Image.Image): The input image.

        Returns:
            np.ndarray: The normalized pixel values.
        """

        # Debugging information
        logging.debug(f'{inspect.currentframe().f_code.co_name}()')

        # Convert the image to a numpy array
        pixels: np.ndarray = np.asarray(image)

        # Normalize the pixel values by dividing them by the maximum possible value
        normalized_pixels = pixels / (pow(2, image.bits) - 1)

        return normalized_pixels

    def _rgb_to_luma(self, image: np.ndarray) -> np.ndarray:
        """
        Converts an RGB image to grayscale using the luma formula.

        Args:
            image (np.ndarray): The input RGB image.

        Returns:
            np.ndarray: The grayscale image.
        """

        # Debugging information
        logging.debug(f'{inspect.currentframe().f_code.co_name}()')

        # Convert the RGB image to grayscale using the luma formula
        image_luma: np.ndarray = np.array(
            0.299 * image[:, :, 0] +
            0.587 * image[:, :, 1] +
            0.114 * image[:, :, 2]
            )

        return image_luma

    def histograms(self, image: Image.Image) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Public method that computes the histograms of an image (luma and RGB).

        Args:
            image (Image.Image): The input image.

        Returns:
            tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
                The corresponding histograms: luma256, RGB 2x2x2, RGB 4x4x4, RGB 6x6x6.
        """
            # nbins (int): The number of bins for the histograms.

        # Debugging information
        logging.debug(f'{inspect.currentframe().f_code.co_name}()')

        # Logging information
        logging.info(f'Computing the histograms for {os.path.basename(image.filename)}...')

        # Normalize the pixel values of the image
        pixels: np.ndarray = self._normalize_image(image)

        # Compute the RGB histograms
        rgb_histo_2x2x2: np.ndarray = self._compute_histograms(pixels, 2)
        rgb_histo_4x4x4: np.ndarray = self._compute_histograms(pixels, 4)
        rgb_histo_6x6x6: np.ndarray = self._compute_histograms(pixels, 6)

        # Convert the image to grayscale
        grayscale_pixels: np.ndarray = self._rgb_to_luma(pixels)

        # Compute the luma histogram
        gray_histo: np.ndarray = self._compute_histograms(grayscale_pixels, 256)

        # Return the histograms
        return (gray_histo, rgb_histo_2x2x2, rgb_histo_4x4x4, rgb_histo_6x6x6)
