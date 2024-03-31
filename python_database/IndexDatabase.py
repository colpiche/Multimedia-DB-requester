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
        _db_path (str): The path to folder containing the images constituting the database.
        _db_files (list[str]): The list of files in the database.
        _histograms_type (list[str]): The list of histogram types.
        _jp (JPicture): An instance of the JPicture class.

    Methods:
        __init__(self, db_path: str): Initializes the IndexDatabase object.
        _get_db_files(self): Retrieves the list of files in the database.
        _write_file(self, histograms: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]): Writes histograms to a file.
        index(self): Indexes the database.
    """

    _db_path: str
    _db_files: list[str]
    _histograms_type: list[str]
    _jp: JPicture

    def __init__(self, db_path: str):
        """
        Initializes the IndexDatabase object.

        Args:
            db_path (str): The path to the database.
        """

        self._db_path = db_path
        self._db_files = []
        self._histograms_type = [
            "HistGRAY_256",
            "HistRGB_2x2x2",
            "HistRGB_4x4x4",
            "HistRGB_6x6x6"
        ]
        self._jp = JPicture()
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
        DB_FILENAMES_FILE_PATH: str = os.path.join(self._db_path, DB_FILENAMES_FILE)

        # Open the file in read mode
        file = open(DB_FILENAMES_FILE_PATH, "r")

        # Iterate over each line in the file
        for line in file:
            # Add the file name to the list of database files, removing the newline character
            self._db_files.append(line.strip('\n'))

        # Close the file
        file.close()

    def _write_file(self, histograms: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]):
        """
        Writes histograms to a file.

        Args:
            histograms (tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]): The histograms to write.
        """

        # Debugging information
        logging.debug(f'{inspect.currentframe().f_code.co_name}()')

        # Create the folder to store the histograms if it doesn't exist
        folder: str = os.path.join(self._db_path, 'histograms')
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Iterate over each histogram in the tuple
        for index, histo in enumerate(histograms):
            file_path: str

            # Construct the file path for the histogram
            file_path = os.path.join(
                folder,
                f'{self._db_path}.{self._histograms_type[index]}.txt'
            )

            # Check if the file already exists, if not create it
            if not os.path.exists(file_path):
                open(file_path, 'w').close()

            # Open the file in append mode
            with open(file_path, 'a') as file:

                # Flatten the numpy array and write each value to the file
                for value in histo.flatten():
                    file.write(f'{value} ')

                # Write a newline character to separate each histogram
                file.write('\n')

            # Close the file
            file.close()

    def index(self):
        """
        Indexes the database.
        """

        # Debugging information
        logging.debug(f'{inspect.currentframe().f_code.co_name}()')

        # Logging information
        logging.info(f'Indexing database in {self._db_path}...')

        # Iterate over each filename in the database files
        for filename in self._db_files:
            # Construct the image path
            image_path = os.path.join(self._db_path, 'images', filename)

            # Open the image using PIL
            image: Image.Image = Image.open(image_path)

            # Compute the histograms using the jp.histograms method
            histograms: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] = self._jp.histograms(image)

            # Close the image
            image.close()

            # Write the file with the computed histograms
            self._write_file(histograms)
        
        # Logging information
        logging.info('Database indexed successfully!')
