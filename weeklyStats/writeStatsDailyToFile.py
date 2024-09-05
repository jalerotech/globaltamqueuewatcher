import logging
import json
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Weekly stats generator")


def writeHandledTicketsToFile(ticket_id_company):
    """
    Writes the ticket-company-mappings to weeklyStats.json file when called by the handleTicketMessages script.
    """
    logger.info(f"Writing ticket_handled_with_company_mapping -> {ticket_id_company} to 'weeklyStats.json' file")
    file_name = 'Files/weeklyStats.json'
    with open(file_name, 'a') as json_file:
        json.dump(ticket_id_company, json_file)
        json_file.write('\n')
    return None

    # with open('Files/weeklyStats.json', 'w') as f:
    #     json.dump(ticket_id_company_mapping, f, indent=4)
    # f.close()
    # logger.info(f'Written {ticket_id_company_mapping} to "weeklyStats.json"')
    # return None





