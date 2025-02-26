from typing import Tuple, List, Union, Dict, Any, Optional
import requests
import logging
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw
from ticketAndMsgHandlers.collabTicketsHandler import ProcessTacCollabTicket
from zendeskData.noteValidator import isNoteViable
from zendeskData.orgDataZendeskNotes import retZDOrgData
from mondayData.readFromTickToCustMApping import readFromTamToCustMappingMdy
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Zendesk Data Processor')

sets_of_tickets = set()
ticket_msg_sent = []


def getAllTickets() -> list[dict]:
    logger.info("Fetching tickets from Zendesk.")
    """
    Produces a json file (list[dict]) of all the tickets with "New" as status.
    :return:list[dict])
    """
    ticket_msg_number = len(sets_of_tickets)
    zendesk_response = requests.get(tqw().zendesk_api_url, headers=tqw().zendesk_headers)
    if zendesk_response.status_code == 200:
        logger.info("Fetching tickets successful.")

        # Parses out the response into a json format and extract the ticket information.
        tickets = zendesk_response.json()['tickets']
        list_of_new_tickets = []
        logger.info("Checking for new tickets in the Zendesk response.")
        for ticket in tickets:
            try:
                # Check if the ticket has a status
                # Checks that ticket is not a non-reply requests.
                if (ticket['status'] == tqw().ticket_status) and (ticket['recipient'] != tqw().no_reply_recipient):
                    if ticket['id'] not in ticket_msg_sent:
                        ticket_msg_sent.append(ticket['id'])
                        ticket_msg_number += 1
                        if ticket['recipient'] != tqw().tac_collab:
                            if ticket['organization_id']:
                                if ticket['priority']:
                                    ticket_data = {
                                        "ticket_counter": ticket_msg_number,
                                        "ticket_id": ticket['id'],
                                        "subject": ticket['subject'],
                                        "cust_zendesk_org_id": ticket['organization_id'],
                                        "created_at": ticket['created_at'],
                                        "priority": ticket['priority'],
                                        "assignee": ticket['assignee_id'],
                                        "SR_number": None
                                    }
                                    list_of_new_tickets.append(ticket_data)
                                    sets_of_tickets.add(ticket['id'])
                                else:
                                    ticket_data = {
                                        "ticket_counter": ticket_msg_number,
                                        "ticket_id": ticket['id'],
                                        "subject": ticket['subject'],
                                        "cust_zendesk_org_id": ticket['organization_id'],
                                        "created_at": ticket['created_at'],
                                        "priority": None,
                                        "assignee": ticket['assignee_id'],
                                        "SR_number": None
                                    }
                                    list_of_new_tickets.append(ticket_data)
                                    sets_of_tickets.add(ticket['id'])
                            else:
                                ticket_data = {
                                    "ticket_counter": ticket_msg_number,
                                    "ticket_id": ticket['id'],
                                    "subject": ticket['subject'],
                                    "cust_zendesk_org_id": None,
                                    "created_at": ticket['created_at'],
                                    "priority": None,
                                    "assignee": ticket['assignee_id'],
                                    "SR_number": None
                                }
                                list_of_new_tickets.append(ticket_data)
                                sets_of_tickets.add(ticket['id'])
                        else:
                            logger.info(f"Ticket {ticket['id']} is a TAC to Umbrella Collab case, pass it to ProcessTacCollabTicket function.")
                            ticket.update({"ticket_counter": ticket_msg_number})
                            sets_of_tickets.add(ticket['id'])
                            ProcessTacCollabTicket(ticket)

                else:
                    logger.info(
                        f"Ticket ID {ticket['id']} has status of {ticket['status']} which is not {tqw().ticket_status}, so skipping it.")
            except KeyError as e:
                logger.info(f'Ticket {ticket} has no "id" key.')
                logger.info(f'Failed to find key {e.args}')
        if len(list_of_new_tickets) == 0:
            logger.info("No new tickets, life is great!.")
        logger.info("Finished fetching and processing tickets from the queue. Taking a small break and will repeat the process again in 60s.")
        print(f"ticket_msg_sent {ticket_msg_sent}")
        return list_of_new_tickets

    else:
        logger.info("Fetching tickets failed.")


def getOrgName(list_of_new_tickets) -> list[dict]:
    logger.info("Fetching organization name from tickets.")
    """
    Produces a new json file after adding organization name to the ticket information in json format.
    :param list_of_new_tickets: Ticket from Zendesk
    :return: list_of_validated_tickets -> containing the org name and other parameter.
    """

    # Validated tickets would be those with cust_zendesk_org_id, org_name, ticket_id and creation_time
    lont_w_OrgNames = []

    for tick in list_of_new_tickets:
        try:
            if tick['cust_zendesk_org_id']:
                zendesk_org_url = f"{tqw().zendesk_org_url}{tick['cust_zendesk_org_id']}.json"
                zendesk_response_org = requests.get(zendesk_org_url, headers=tqw().zendesk_headers)
                if zendesk_response_org.status_code == 200:
                    # If the API call was successful, extract the organization name from the response JSON
                    organization_name = zendesk_response_org.json()['organization']['name']

                    # Display the name of the organization
                    logger.info(f"Ticket number {tick['ticket_id']} as organization name => {organization_name}")
                    # Update the new ticket list with the org name and adds the new data to the validated list of new tickets
                    tick.update({
                        'org_name': organization_name
                    })
                    lont_w_OrgNames.append(tick)
                else:
                    # If the API call was not successful, display the status code and reason
                    logger.info(
                        f"Error in the API call to Zendesk to fetch the cust_zendesk_org_id {zendesk_response_org.status_code}: "
                        f"{zendesk_response_org.reason}")
            else:
                logger.info(f'The ticket {tick["ticket_id"]} is missing cust_zendesk_org_id from Zendesk.')
                tick.update({
                    'org_name': None
                })
                lont_w_OrgNames.append(tick)
        except KeyError as e:
            logger.debug(f'The ticket {tick} has no organization_id  or cust_zendesk_org_id key {e.args}.')
    return lont_w_OrgNames


validated_tickets = []


def validateTickets(list_of_new_tickets) -> tuple[
    list[Union[dict, dict[str, Any], dict[str, Optional[Any]], dict[str, Any], dict[str, Optional[Any]]]], list[Any]]:
    logger.info("Validating new tickets.")
    """
    Fetches the org names from Zendesk using the cust_zendesk_org_id from the tickets.
    Using the org names to get the TAM, Backup_TAMs, Customer region and BFG_org where applicable.
    - If the org on zendesk have viable notes, this is used to get the TAM, Backup_TAMs, Customer region and BFG_org.
    - Otherwise uses the locally cached tam-to-customer-mapping -> "tamToCustMappingMdy.json".
    :param list_of_new_tickets: List of new ticket from Zendesk.
    :return: validated Ticket list -> containing the org name and other parameter -> "validatedTickets"
    :return: lont_w_orgName list -> containing the ticket counter, org_name, etc.
    """

    # Validated tickets would be those with cust_zendesk_org_id, org_name, ticket_id and creation_time
    validatedTickets = []
    lont_w_orgName = []

    for tick in list_of_new_tickets:
        try:
            if tick['ticket_id'] not in validated_tickets:
                if tick['cust_zendesk_org_id']:
                    zendesk_org_url = f"{tqw().zendesk_org_url}{tick['cust_zendesk_org_id']}.json"
                    zendesk_response_org = requests.get(zendesk_org_url, headers=tqw().zendesk_headers)
                    if zendesk_response_org.status_code == 200:
                        # If the API call was successful, extract the organization name from the response JSON
                        organization_name = zendesk_response_org.json()['organization']['name']
                        organization_notes = zendesk_response_org.json()['organization']['notes']
                        tick.update({
                            'org_name': organization_name
                        })
                        lont_w_orgName.append(tick)
                        # Update org name for Sfr and replace to COVEA GROUPE, as there's no data for Sfr on Monday.com nor on the Zendesk org.
                        if organization_name == "Sfr":
                            tick.update({
                                'org_name': "COVEA GROUPE"
                            })
                        if organization_notes:
                            if isNoteViable(organization_notes):
                                logger.info(f"Zendesk Note is viable for ticket {tick['ticket_id']}.")
                                tick_org_notes = {
                                    "ticket_id": tick['ticket_id'],
                                    "notes": organization_notes
                                }
                                validatedTickets.append(retZDOrgData(tick_org_notes))
                            else:
                                logger.info(f"Note is not viable on ticket {tick['ticket_id']}, Using Monday.com locally cached data method to get TAM Info.")
                                tick.update({
                                    'org_name': organization_name
                                })
                                # Since notes are not viable, check the locally cached file 'tamToCustMappingMdy.json' for needed data
                                usable_data = retTickDataLocalFile(tick)
                                if usable_data:
                                    # Adds the updated ticket to the validated ticket list
                                    validatedTickets.append(usable_data)
                                else:
                                    # Otherwise, create entry fot the ticket using the blank fields -> None below instead. And updates the validated tickets file.
                                    tick = {
                                        'ticket_id': tick['ticket_id'],
                                        'primary_tam': None,
                                        'backup_tam': None,
                                        'customer_region': None,
                                        'bfg_org_id': None
                                    }
                                    validatedTickets.append(tick)
                        else:
                            logger.info(f"Ticket {tick['ticket_id']} has no notes. Reverting to local methods.")
                            usable_data = retTickDataLocalFile(tick)
                            if usable_data:
                                # Adds the updated ticket to the validated ticket list
                                validatedTickets.append(usable_data)
                            else:
                                logger.info(f"Ticket {tick['ticket_id']} has no Zendesk notes and no Monday.com entry.")
                                tick.update({
                                    'ticket_id': tick['ticket_id'],
                                    'primary_tam': None,
                                    'backup_tam': None,
                                    'customer_region': None,
                                    'bfg_org_id': None
                                })
                                validatedTickets.append(tick)
                    else:
                        # If the API call was not successful, display the status code and reason
                        logger.info(
                            f"Error in the API call to Zendesk to fetch the cust_zendesk_org_id {zendesk_response_org.status_code}: "
                            f"{zendesk_response_org.reason}")
                else:
                    logger.info(f'The ticket {tick["ticket_id"]} is missing cust_zendesk_org_id from Zendesk.')
                    new_tick_data = {
                        'ticket_id': tick['ticket_id'],
                        'primary_tam': None,
                        'backup_tam': None,
                        'customer_region': None,
                        'bfg_org_id': None
                    }
                    tick.update({
                        'org_name': None
                    })
                    lont_w_orgName.append(tick)
                    validatedTickets.append(new_tick_data)
                    validated_tickets.append(tick['ticket_id'])
        except KeyError as e:
            logger.debug(f'The ticket {tick} has no organization_id  or cust_zendesk_org_id key {e.args}.')
    return validatedTickets, lont_w_orgName


local_ticket_data_returned = []


def retTickDataLocalFile(tick):
    for mapping in readFromTamToCustMappingMdy():
        if tick['ticket_id'] not in local_ticket_data_returned:
            if mapping['company_name'].lower() == tick['org_name'].lower():
                ret_tick_data = {
                    "ticket_id": tick['ticket_id'],
                    "primary_tam": mapping['primary_tam'],
                    "backup_tam": mapping['backup_tam'],
                    "customer_region": mapping['customer_region'],
                    "bfg_org_id": mapping['bfg_org_id']
                }
                local_ticket_data_returned.append(tick['ticket_id'])
                return ret_tick_data


def reset_sets_of_tickets_no_time_check():
    """
    resets the processed ticket set to a length of 0 (used as message/ticket counter) to save memory usage.
    :return:
    """
    logger.info("Running 'def reset_sets_of_tickets_no_time_check()'")
    logger.info(f"length of 'sets_of_tickets' is {len(sets_of_tickets)}.")
    logger.info("Resetting the 'sets_of_tickets set to be a length of 0'")
    sets_of_tickets.clear()
    logger.info(f"length of 'sets_of_tickets' is now {len(sets_of_tickets)}.")
    logger.info("Resetting the 'sets_of_tickets set to be a length of 0'...=> COMPLETED")


def reset_ticket_msg_sent():
    """
    resets the ticket_msg_sent list to a length of 0 (used as message/ticket counter) to save memory usage.
    This should be called every weekend.
    :return:
    """
    logger.info("Running 'def reset_ticket_msg_sent()'")
    logger.info(f"length of 'ticket_msg_sent' is {len(ticket_msg_sent)}.")
    logger.info("Resetting the 'ticket_msg_sent set to be a length of 0'")
    ticket_msg_sent.clear()
    logger.info(f"length of 'ticket_msg_sent' is now {len(ticket_msg_sent)}.")
    logger.info("Resetting the 'ticket_msg_sent set to be a length of 0'...=> COMPLETED")


