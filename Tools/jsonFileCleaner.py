import json
import logging


def cleanJsonFiles():
    logger = logging.getLogger("Cleaning Json Files")
    logger.info("Reading ticket from reminder_data.json file - STARTED.")
    """
    DOCSTRING HERE
    """
    file_name_list = ['parentMsgIds', 'reminder_data', 'tamPTOStatus']
    for file_name in file_name_list:
        file_name = f'Files/{file_name}.json'
        with open(file_name, 'w') as json_file:
            json.dump({}, json_file)
            logger.info(f'Cleaned up {file_name}.json file - COMPLETED')
