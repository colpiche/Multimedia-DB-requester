import inspect
import logging
import numpy as np
import os
from scipy.spatial.distance import chebyshev
from typing import TypedDict


class Distance(TypedDict):
    """
    Represents a distance between two objects in a database.

    Attributes:
        file (str): The file name of the object measured.
        distance (float): The distance between the objects.
    """

    file: str
    distance: float


class QBE:
    """
    QBE class represents a Query By Example system.
    """

    db_path: str
    descriptors_path: str
    db_files: list[str]

    def __init__(self, db_path: str, descriptors_path: str):
        """
        Initializes a QBE object.

        Args:
            db_path (str): Path to the database.
            descriptors_path (str): Path to the descriptors.
        """

        self.db_path = db_path
        self.descriptors_path = descriptors_path
        self.db_files = []
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
        DB_FILENAMES_FILE_PATH: str = os.path.join(self.descriptors_path, DB_FILENAMES_FILE)

        # Open the file in read mode
        file = open(DB_FILENAMES_FILE_PATH, "r")

        # Iterate over each line in the file
        for line in file:
            # Add the file name to the list of database files, removing the newline character
            self.db_files.append(line.strip('\n'))

        # Close the file
        file.close()

    def _init_descriptors(self, descriptor_file_name: str) -> np.ndarray:
        """
        Initializes the descriptors from a file.

        Args:
            descriptor_file_name (str): Name of the descriptor file.

        Returns:
            np.ndarray: Array of descriptors.
        """

        # Debugging information
        logging.debug(f'{inspect.currentframe().f_code.co_name}()')

        # Create an empty list to store the descriptors
        descriptors: list[list[float]] = []

        # Open the descriptor file
        descriptor_file = open(os.path.join(self.descriptors_path, descriptor_file_name), "r")

        # Iterate over each line in the descriptor file
        for line in descriptor_file:
            # Remove newline character and split the line by space
            values: list[float] = [float(value) for value in list(filter(None, line.strip('\n').split(' ')))]

            # Append the values to the descriptors list
            descriptors.append(values)

        # Convert the descriptors list to a numpy array and return it
        return np.asarray(descriptors)

    def _compute_descriptors_distance(
            self,
            descriptor1: np.ndarray,
            descriptor2: np.ndarray
            ) -> float:
        """
        Computes the distance between two descriptors.

        Args:
            descriptor1 (np.ndarray): First descriptor.
            descriptor2 (np.ndarray): Second descriptor.

        Returns:
            float: Distance between the descriptors.
        """

        # Debugging information
        logging.debug(f'{inspect.currentframe().f_code.co_name}()')

        # Compute the distance between the descriptors using the chebyshev function from scipy
        return chebyshev(descriptor1, descriptor2)

    def _generate_html_file(
            self,
            descriptor_file_path: str,
            image_name: str,
            distances: list[Distance],
            nb_results: int
            ):
        """
        Generates an HTML file with the query results.

        Args:
            descriptor_file_path (str): Path to the descriptor file.
            image_name (str): Name of the base image.
            distances (list[Distance]): List of distances.
            nb_results (int): Number of results to display.
        """

        # Debugging information
        logging.debug(f'{inspect.currentframe().f_code.co_name}()')

        # Define the folder path for the generated HTML file
        folder: str = os.path.join(self.db_path, 'requests')

        # Create the folder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Define the file path for the generated HTML file
        file_path = os.path.join(
                folder,
                f'{"".join(image_name.split(".")[:-1])}_{descriptor_file_path.split(".")[-1]}_{nb_results}.html'
            )

        # Define the height of the images in the HTML file
        image_height: int = 100

        # Open the file in write mode
        with open(file_path, 'w') as file:
            # Write the HTML file header
            file.write('<!DOCTYPE html>\n')
            file.write('<html>\n')
            file.write('<head></head>\n')
            file.write('<body>\n')

            # Write the query information in the HTML file
            file.write(f'<h1>Query for image {image_name} using {os.path.basename(descriptor_file_path)} limited to {nb_results} results</h1>\n')
            file.write(f'<img src="../images/{image_name}" height="{image_height}" />\n')
            file.write('<h2>Results</h2>\n')

            # Write the image results in the HTML file
            for i in range(nb_results):
                file.write(f'<img src="../images/{distances[i]["file"]}" height="{image_height}" />\n')

            # Write the HTML file footer
            file.write('</body>\n')
            file.write('</html>\n')

            # Close the file
            file.close()

    def request(self, descriptor_file_name: str, base_image_name: str, nresults: int):
        """
        Performs a query using a descriptor file and a base image.

        Args:
            descriptor_file_name (str): Name of the descriptor file.
            base_image_name (str): Name of the base image.
            nresults (int): Number of results to retrieve.
        """

        # Debugging information
        logging.debug(f'{inspect.currentframe().f_code.co_name}()')

        # Logging information
        logging.info(f'Similarity requested for image {base_image_name} using {descriptor_file_name} limited to {nresults} results. Processing...')

        # Initialize descriptors from the descriptor file
        descriptors: np.ndarray = self._init_descriptors(descriptor_file_name)

        # Get the index of the base image in the list of database files
        base_image_index: int = self.db_files.index(base_image_name)

        # Get the descriptor of the base image
        base_image_descriptor: np.ndarray = descriptors[base_image_index]

        # Create an empty list to store the distances
        distances: list[Distance] = []

        # Iterate over each image in the database
        for current_image_name in self.db_files:

            # Skip the base image
            if current_image_name != base_image_name:

                # Get the index of the current image in the list of database files
                current_image_index: int = self.db_files.index(current_image_name)

                # Get the descriptor of the current image
                current_image_descriptor: np.ndarray = descriptors[current_image_index]

                # Compute the distance between the current image and the base image
                distance: float = self._compute_descriptors_distance(current_image_descriptor, base_image_descriptor)

                # Add the distance to the list of distances
                distances.append({'file': current_image_name, 'distance': distance})

        # Sort the distances in ascending order
        distances.sort(key=lambda x: x['distance'])

        # Generate an HTML file with the query results
        self._generate_html_file(descriptor_file_name, base_image_name, distances, nresults)

        # Logging information
        logging.info(f'Query for image {base_image_name} done.')
