import json
import logging


def read_tam_stats_file():
    logger = logging.getLogger("read_tam_stats_file")
    logger.info("Reading ticket from tamTicketStats.json file - STARTED.")
    """
    Reads the tamTicketStats.json file and produces it's content.
    """
    file_name = 'Files/tamTicketStats.json'
    with open(file_name, 'r') as json_file:
        try:
            data = json.load(json_file)
            logger.info("Reading ticket from tamTicketStats.json file - COMPLETED.")
            return data
        except json.JSONDecodeError as e:
            logger.info(f"Error details: {e}")
    # logger.info("Reading ticket from tamTicketStats.json file - COMPLETED.")


if __name__ == '__main__':
    print(read_tam_stats_file())