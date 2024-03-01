import json
import logging


def cleanJsonFiles(file_name_input):
    logger = logging.getLogger("Cleaning Json Files")
    logger.info("Reading ticket from reminder_data.json file - STARTED.")
    """
    DOCSTRING HERE
    """
    if file_name_input:
        with open(file_name_input, 'w') as json_file:
            json.dump('', json_file)
            logger.info(f'Cleaned up {file_name_input}.json file - COMPLETED')
    else:
        file_name_list = ['parentMsgIds', 'reminder_data', 'tamPTOStatus']
        for file_name in file_name_list:
            file_name = f'Files/{file_name}.json'
            with open(file_name, 'w') as json_file:
                json.dump({}, json_file)
                logger.info(f'Cleaned up {file_name}.json file - COMPLETED')
