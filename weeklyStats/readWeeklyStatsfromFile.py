import logging
import json
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Weekly stats generator")

processed_data = []


def readHandledTicketsDataFromFile() -> list:
    """
    Produces the list of ticket-to-company mappings from the weeklyStats file.
    """
    data_list = []
    with open("Files/weeklyStats.json", 'r') as json_file:
        for line in json_file:
            try:
                data = json.loads(line)
                if data['ticket_id'] not in processed_data:
                    data_list.append(data)
                    processed_data.append(data['ticket_id'])
                else:
                    logger.info(f"Ticket {data['ticket_id']} already read from the weeklyStats.json file.")
            except json.JSONDecodeError as e:
                logger.info(f"Error decoding JSON on line: {line}")
                logger.info(f"Error details: {e}")
    logger.info("Reading ticket from weeklyStats.json file - COMPLETED.")
    return data_list


if __name__ == '__main__':
    readHandledTicketsDataFromFile()