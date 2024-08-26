import json
import logging


def readFromTamToCustMappingMdy():
    logger = logging.getLogger("Read from TamToCustomerMapping file.")
    logger.info("Reading ticket from tamToCustMappingMdy.json file - STARTED.")
    """
    Reads the tamToCustMappingMdy.json file and produces it's content.
    """
    file_name = 'Files/tamToCustMappingMdy.json'
    with open(file_name, 'r') as json_file:
        try:
            data = json.load(json_file)
            logger.info("Reading ticket from tamToCustMappingMdy.json' file - COMPLETED.")
            return data
        except json.JSONDecodeError as e:
            logger.info(f"Error details: {e}")
