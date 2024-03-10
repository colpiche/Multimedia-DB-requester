from python_database.IndexDatabase import IndexDatabase as db
from python_database.QBE import QBE
import logging


# Define the paths and file names
DB_PATH: str = r'Base10000'


# Global variables for the query by example (QBE) system
DESCRIPTORS_PATH: str = r'Base10000_descriptors'
IMAGE_NAME: str = '123033.jpg'
DESCRIPTOR_FILE_NAME: str = 'Base10000.HistGREY_256'
NB_RESULTS: int = 30


# Set the logging level and format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )


# Instructions to index the database
index_db = db(DB_PATH)

# Uncomment this line to index the database
# index_db.index(nbins=16)


# Instructions to query the database
qbe = QBE(DB_PATH, DESCRIPTORS_PATH)
qbe.request(DESCRIPTOR_FILE_NAME, IMAGE_NAME, NB_RESULTS)
