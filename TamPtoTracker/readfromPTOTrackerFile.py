import json
import logging


def read_json_file_line_by_line():
    logger = logging.getLogger("read_json_file_line_by_line")
    logger.info("Reading ticket from reminder_data.json file - STARTED.")
    """
    Read a JSON file line by line and return a list of dictionaries.

    Args:
    - file_path (str): The path to the JSON file.

    Returns:
    - list: A list of dictionaries, where each dictionary corresponds to a line in the file.
    """
    file_name = 'Files/tamPTOStatus.json'
    data_list = []
    with open(file_name, 'r') as json_file:
        for line in json_file:
            try:
                data = json.loads(line)
                data_list.append(data)
            except json.JSONDecodeError as e:
                logger.info(f"Error decoding JSON on line: {line}")
                logger.info(f"Error details: {e}")
    logger.info("Reading ticket from reminder_data.json file - COMPLETED.")
    return data_list


# if __name__ == '__main__':
#     # file_path = 'reminder_data.json'
#     file_path = '/Users/jalero/PycharmProjects/UmbrellaTamQueueWatcher/reminder_data.json'
#     reminder_data_list = read_json_file_line_by_line(file_path)
#
#     # Print the result
#     print(reminder_data_list)
