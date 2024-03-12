import requests
import logging
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw
from ticketAndMsgHandlers.collabTicketsHandler import ProcessTacCollabTicket

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Zendesk Data')

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
                                        "assignee": ticket['assignee_id']
                                    }
                                    # print(ticket['priority'])
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
                                        "assignee": ticket['assignee_id']
                                    }
                                    # print(ticket['priority'])
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
                                    "assignee": ticket['assignee_id']
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


