import logging
import json
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Weekly stats generator")


def readHandledTicketsDataFromFile() -> list:
    """
    Produces the list of ticket-to-company mappings from the weeklyStats file.
    """
    data_list = []
    with open("Files/weeklyStats.json", 'r') as json_file:
        for line in json_file:
            try:
                data = json.loads(line)
                logger.info("Reading ticket from weeklyStats.json file - COMPLETED.")
                data_list.append(data)
            except json.JSONDecodeError as e:
                logger.info(f"Error details: {e}")
    return data_list
