import json
import logging


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Cleaning Json Files")


def cleanJsonFiles(file_name_input):
    logger.info("Reading ticket from *.json file - STARTED.")
    """
    DOCSTRING HERE
    """
    if file_name_input:
        with open(file_name_input, 'w') as json_file:
            json_file.close()
            logger.info(f'Cleaned up {file_name_input}.json file - COMPLETED')
    else:
        # file_name_list = ['parentMsgIds', 'reminder_data']
        file_name_list = ['stats.json']
        for file_name in file_name_list:
            file_name = f'Files/{file_name}.json'
            with open(file_name, 'w') as json_file:
                json_file.close()
                logger.info(f'Cleaned up {file_name}.json file - COMPLETED')


if __name__ == '__main__':
    file = None
    cleanJsonFiles(file)

