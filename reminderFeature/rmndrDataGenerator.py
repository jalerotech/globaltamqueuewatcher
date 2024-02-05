import json
import logging

data_list = []
logger = logging.getLogger('Reminder Data Writer')


def rmndrDataWriter(entry_data) -> None:
    """
    Writes the ticket information (dict) into the reminder_data.json file.
    Each entry (data) is a list item in the .json file.
    For example:
    [
      {'ticket_counter': 1, 'subject': 'Account Role change error', 'assignee': 399319664672, 'ticket_id': 1745461},
      {'ticket_counter': 2, 'subject': "macOS 14.3 - issue", 'assignee': 399319664672, 'ticket_id': 1746333}
    ]
    :param entry_data:dict in this format -> {'ticket_counter': 1, 'subject': 'Account Role change error', 'assignee': 399319664672, 'ticket_id': 1745461}
    :return: None
    """

    logger.info(f"Writing data {entry_data} to the reminder_data.json file")
    # Specify the JSON file name
    file_name = 'Files/reminder_data.json'

    # logger.info(f"Adding data -> {entry_data} to the data_list")
    # # Creates a list of all the entry_data.
    # data_list.append(entry_data)
    # with open(file_name, 'w') as json_file:  # Use 'w' mode to overwrite the file
    #     json.dump(data_list, json_file)

    #  Writes the entry_data one line at a time in the reminder_data.json file. No list needed here -> Evaluating the best performance in the reminder feature.
    with open(file_name, 'a') as json_file:
        json.dump(entry_data, json_file)
        json_file.write('\n')
