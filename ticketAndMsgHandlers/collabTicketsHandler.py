from datetime import datetime
from ticketAndMsgHandlers.handleTicketMessages import postCollabTicketMsg, ticket_id_company_mapping
import logging

logger = logging.getLogger('Running ProcessTacCollabTicket')


def ProcessTacCollabTicket(ticket) -> None:

    """
    parses out the SR number and account org_name from the ticket subject.
    Note: Collab ticket doesn't come with organization_id, that we can use to fetch further data from ZD.
    :param ticket: data received from ZD.
    :return: calls postCollabTicketMsg(postCollabTicketMsg) with the dict containing SR number, org name and counter as a parameter.
    """
    logger.info(f"Processing TAC collab ticket -> {ticket['id']} -> STARTED")
    subject = ticket['subject']
    SR_number = subject.split(' ')[2].split('#')[1].strip(']')
    org_name = subject.split(' ')[4].strip('[]')

    timestamp = datetime.strptime(ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ")
    formatted_timestamp = timestamp.strftime("%H:%M:%S")

    collabTickData = {
        'SR_number': SR_number,
        'org_name': org_name,
        'id': ticket['id'],
        'formatted_timestamp': formatted_timestamp,
        'ticket_counter': ticket['ticket_counter'],
        'subject': ticket['subject']
    }
    ticket_handled_data = {
        'ticket_id': ticket['id'],
        'customer_name': org_name
    }
    # print(f"ticket_id_company_mapping so far -> {ticket_id_company_mapping}")
    if ticket_handled_data not in ticket_id_company_mapping:
        ticket_id_company_mapping.append(ticket_handled_data)
    logger.info(f"Processing TAC collab ticket -> {ticket['id']} -> COMPLETED, Sending to be posted to WxT.")

    return postCollabTicketMsg(collabTickData)


if __name__ == "__main__":
    test_data = {"subject": "[Premium Support] [SR#695901881] [S3] [Hitachi]",
                 "created_at": "2023-07-26T07:58:01Z",
                 "ticket_counter": 1,
                 "ticket_id": 123456}
    ProcessTacCollabTicket(test_data)
