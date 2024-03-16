import json
import logging

data_list = []
logger = logging.getLogger('TAM ticket stats Data Writer')


def TamStatsDataWriter(entry_data) -> None:
    """
    Writes the ticket assignment data into the tamTicketStats.json file.
    :param
    :return: None
    """

    logger.info(f"Writing data {entry_data} to the tamTicketStats.json file")
    # Specify the JSON file name
    file_name = 'Files/tamTicketStats.json'

    #  Writes the entry_data one line at a time in the reminder_data.json file. No list needed here -> Evaluating the best performance in the reminder feature.
    with open(file_name, 'w+') as json_file:
        json.dump(entry_data, json_file)
        json_file.write('\n')
