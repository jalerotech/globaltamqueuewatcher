import json
import logging

data_list = []
logger = logging.getLogger('TAM PTO Message Data Writer')


def tamPTOMsgDataWriter(entry_data) -> None:
    """
    DOCSTRING HERE

    :param entry_data:dict in this format -> {'msg_id_#1': <ID_string_#1>}
    :return: None
    """

    logger.info(f"Writing data {entry_data} to the parentMsgIds.json file")
    # Specify the JSON file name
    file_name = 'Files/tamPTOStatus.json'

    #  Writes the entry_data one line at a time in the reminder_data.json file. No list needed here -> Evaluating the best performance in the reminder feature.
    with open(file_name, 'a') as json_file:
        json.dump(entry_data, json_file)
        json_file.write('\n')
