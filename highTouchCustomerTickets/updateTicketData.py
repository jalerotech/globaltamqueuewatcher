import logging
from datetime import datetime

from highTouchCustomerTickets.checkZdOrgNotes import checkZDOrgNotesData
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tQw
import requests

from zendeskData.noteValidator import isNoteViable
from zendeskData.orgDataZendeskNotes import retZDOrgData

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


treated_tickets = []


def updateTicketData(list_of_new_tickets):
    """
    Fetches the org names from Zendesk using the cust_zendesk_org_id from the tickets.
    Using the org names to get the TAM, Backup_TAMs, Customer region and BFG_org where applicable.
    :param list_of_new_tickets: List of new high touch tickets from Zendesk.
    :return: updated_tickets -> containing the org name and other parameter -> "updated_tickets"
    """

    logger = logging.getLogger('updateTicketData: ')
    logger.info("Validating new tickets.")

    # Validated tickets would be those with cust_zendesk_org_id, org_name, ticket_id and creation_time
    updated_tickets = []
    lont_w_orgName = []

    for tick in list_of_new_tickets:
        try:
            if tick['ticket_id'] not in treated_tickets:
                if tick['cust_zendesk_org_id']:
                    zendesk_org_url = f"{tQw().zendesk_org_url}{tick['cust_zendesk_org_id']}.json"
                    zendesk_response_org = requests.get(zendesk_org_url, headers=tQw().zendesk_headers)
                    if zendesk_response_org.status_code == 200:
                        # If the API call was successful, extract the organization name from the response JSON
                        organization_name = zendesk_response_org.json()['organization']['name']
                        organization_notes = zendesk_response_org.json()['organization']['notes']
                        tick.update({
                            'org_name': organization_name
                        })
                        lont_w_orgName.append(tick)
                        if organization_notes:
                            timestamp = datetime.strptime(tick['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                            formatted_timestamp = timestamp.strftime("%H:%M:%S")
                            if isNoteViable(organization_notes):
                                logger.info(f"Zendesk Note is viable for ticket {tick['ticket_id']}.")
                                tick_org_notes = {
                                    "ticket_counter": tick['ticket_counter'],
                                    "ticket_id": tick['ticket_id'],
                                    "notes": organization_notes,
                                    "priority": tick['priority'],
                                    "org_name": tick['org_name'],
                                    "subject": tick['subject'],
                                    "created_at": formatted_timestamp,
                                    "linked_incidents": None
                                }
                                updated_tickets.append(checkZDOrgNotesData(tick_org_notes))
            # return updated_tickets
        except KeyError as e:
            logger.debug(f'The ticket {tick} has no organization_id  or cust_zendesk_org_id key {e.args}.')
    if updated_tickets:
        return updated_tickets

