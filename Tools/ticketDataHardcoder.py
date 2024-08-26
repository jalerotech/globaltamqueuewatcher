from bfgData.getBfgUrlFromList import createBfgUrls
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Ticket Data Hard-coder - Custom ticket information')


def ret_covea_data(ticket_id) -> dict:
    """
    returns covea hardcoded information needed for the ticket alert message.
    """
    logger.info(f"Running ret_covea_data")
    tam_info = {
        "ticket_id": ticket_id,
        "primary_tam": "Joshua Alero",
        "backup_tam": "Anthony Attwood",
        "customer_region": "EMEA",
        "bfg_org_id": createBfgUrls([7948441])[0]
    }
    logger.info(f"Running ret_covea_data - Completed.")
    return tam_info
