import json
import logging

data_list = []
logger = logging.getLogger('Tam-to-customer-mapping Writer')


def tTcmWriter(mapping) -> None:
    """
    writes the tam-to-customer-mapping to tamToCustMappingMdy.json file.
    :param mapping: tam-to-customer-mapping from Monday.com
    :return: None
    """

    logger.info(f"tTcmWriter: Writing data {mapping} to the tamToCustMappingMdy.json file")
    file_name = 'Files/tamToCustMappingMdy.json'

    # Cleans up the file before writing to it.
    with open(file_name, 'w') as json_file:
        logger.info(f"{file_name} opened")
        logger.info(f'Cleaning up {file_name} file')
        json_file.close()
        logger.info(f'{file_name} file cleaned \n ')

    #  Writes the entry_data one line at a time in the reminder_data.json file. No list needed here -> Evaluating the best performance in the reminder feature.
    with open(file_name, 'a') as json_file:
        json.dump(mapping, json_file)
        json_file.write('\n')
