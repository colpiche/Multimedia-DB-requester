import inspect
from .JPicture import JPicture
import logging
import numpy as np
import os
from PIL import Image


class IndexDatabase:
    """
    A class representing a database indexing utility.

    Attributes:
        db_path (str): The path to the database.
        db_files (list[str]): The list of files in the database.
        jp (JPicture): An instance of the JPicture class.

    Methods:
        __init__(self, db_path: str): Initializes the IndexDatabase object.
        _get_db_files(self): Retrieves the list of files in the database.
        _write_file(self, filename: str, histograms: tuple[np.ndarray, np.ndarray]): Writes histograms to a file.
        index(self, nbins: int = 64): Indexes the database.
    """

    db_path: str
    db_files: list[str]
    jp: JPicture

    def __init__(self, db_path: str):
        """
        Initializes the IndexDatabase object.

        Args:
            db_path (str): The path to the database.
        """

        self.db_path = db_path
        self.db_files = []
        self.jp = JPicture()
        self._get_db_files()

    def _get_db_files(self):
        """
        Retrieves the list of files in the database.
        """

        # Debugging information
        logging.debug(f'{inspect.currentframe().f_code.co_name}()')

        # Define the name of the file containing the list of database files
        DB_FILENAMES_FILE: str = 'Base10000_files.txt'

        # Construct the full path to the file containing the list of database files
        DB_FILENAMES_FILE_PATH: str = os.path.join(self.db_path, DB_FILENAMES_FILE)

        # Open the file in read mode
        file = open(DB_FILENAMES_FILE_PATH, "r")

        # Iterate over each line in the file
        for line in file:
            # Add the file name to the list of database files, removing the newline character
            self.db_files.append(line.strip('\n'))

        # Close the file
        file.close()

    def _write_file(self, filename: str, histograms: tuple[np.ndarray, np.ndarray]):
        """
        Writes histograms to a file.

        Args:
            filename (str): The name of the file.
            histograms (tuple[np.ndarray, np.ndarray]): The histograms to write.
        """

        # Debugging information
        logging.debug(f'{inspect.currentframe().f_code.co_name}()')

        # Create the folder to store the histograms if it doesn't exist
        folder: str = os.path.join(self.db_path, 'histograms')
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Iterate over each histogram in the tuple
        for histo in histograms:
            file_path: str
            nbins: int = histo.shape[0]

            # Check if the histogram is grayscale or RGB
            if histo.ndim == 1:
                # Grayscale histogram
                file_path = os.path.join(
                    folder,
                    f'{os.path.splitext(filename)[0]}_HistGRAY_{nbins}.txt'
                )

                # Write the grayscale histogram values to the file
                with open(file_path, 'w') as file:
                    for value in histo:
                        file.write(f'{value} ')

            elif histo.ndim == 3:
                # RGB histogram
                file_path = os.path.join(
                    folder,
                    f'{os.path.splitext(filename)[0]}_HistRGB_{nbins}x{nbins}x{nbins}.txt'
                )

                # Write the RGB histogram values to the file
                with open(file_path, 'w') as file:
                    for slice in histo:
                        for column in slice:
                            for value in column:
                                file.write(f'{value} ')
                        file.write('\n')

            # Close the file
            file.close()

    def index(self, nbins: int = 64):
        """
        Indexes the database.

        Args:
            nbins (int, optional): The number of bins for the histograms. Defaults to 64.
        """

        # Debugging information
        logging.debug(f'{inspect.currentframe().f_code.co_name}()')

        # Logging information
        logging.info(f'Indexing database in {self.db_path}...')

        # Iterate over each filename in the database files
        for filename in self.db_files:
            # Construct the image path
            image_path = os.path.join(self.db_path, 'images', filename)

            # Open the image using PIL
            image: Image.Image = Image.open(image_path)

            # Compute the histograms using the jp.histograms method
            histograms: tuple[np.ndarray, np.ndarray] = self.jp.histograms(image, nbins)

            # Close the image
            image.close()

            # Write the file with the computed histograms
            self._write_file(filename, histograms)

        # Logging information
        logging.info('Database indexed successfully!')
