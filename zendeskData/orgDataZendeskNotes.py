import requests
import logging
import re
from bfgData.getBfgUrlFromList import createBfgUrls
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw
from ticketAndMsgHandlers.collabTicketsHandler import ProcessTacCollabTicket
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher
bfg_base_url = TamQueueWatcher().bfg_base_url

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Org Data via Zendesk Notes')


def retZDOrgData(tick_org_notes) -> dict:
    """
    Parses out the TAM, Backup_TAM(s), CMS, Customer_region, BFG_org from the Zendesk org notes.
    Produces a dict containing the parsed information.
    """
    logger.info(f"Zendesk Notes found for ticket {tick_org_notes['ticket_id']}, parsing out TAM, REGION and BFG info.")
    # Define regular expressions to capture CSM, TAM, BFG_org, CUSTOMER_REGION
    # print(tick_org_notes)
    csm_pattern = r'CSM:\s*([^\n]+)'
    tam_pattern = r'PRIMARY_TAM:\s*([^\n]+)'
    backup_tams_pattern = r'BACKUP_TAM:\s*([^\n]+)'
    cust_region_pattern = r'CUSTOMER_REGION:\s*([^\n]+)'
    bfg_org_pattern = r'BFG_ORG:\s*([^\n]+)'

    # Search for the patterns in the input string
    csm_match = re.search(csm_pattern, tick_org_notes['notes'])
    tam_match = re.search(tam_pattern, tick_org_notes['notes'])
    backup_tams_match = re.search(backup_tams_pattern, tick_org_notes['notes'])
    cust_region_match = re.search(cust_region_pattern, tick_org_notes['notes'])
    bfg_org_match = re.search(bfg_org_pattern, tick_org_notes['notes'])

    # Extract the matches, if found
    csm = csm_match.group(1).strip() if csm_match else None
    tam = tam_match.group(1).strip() if tam_match else None
    backup_tams = backup_tams_match.group(1).strip() if backup_tams_match else None
    cust_region = cust_region_match.group(1).strip() if cust_region_match else None
    bfg_org = bfg_org_match.group(1).strip() if bfg_org_match else None

    updated_tick_data = {
        "ticket_id": tick_org_notes['ticket_id'],
        "primary_tam": tam,
        "backup_tam": backup_tams,
        "customer_region": cust_region,
        "bfg_org_id": createBfgUrls([bfg_org])[0]
    }
    logger.info(f"Returning updated ticket data for ticket {tick_org_notes['ticket_id']}.")
    return updated_tick_data

