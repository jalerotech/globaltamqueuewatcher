import logging

from ticketAndMsgHandlers.msgPoster import sendMessageToWxT
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

handled_tickets = []


def createMsg(ticket_data):
    """
    Produces the message (str) to send to WebEx teams using the list of ticket data provided.
    :param ticket_data: list of ticket information -> id, creation time etc.
    :return:
    """
    for ticket in ticket_data:
        logger = logging.getLogger('createMsg: ')
        logger.info(f"Creating personalized message to send to WxT space for ticket -> {ticket['ticket_id']}")
        msg_to_send = f"### New High Severity Ticket has landed in the TAM Q !!! ({ticket['ticket_counter']}) \n " \
                      f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                      f"Subject: {ticket['subject']} \n " \
                      f"Company name: **{ticket['customer_name']}** \n " \
                      f"Creation time in UTC: {ticket['created_at']} \n" \
                      f"Primary TAM: {ticket['primary_tam']} \n" \
                      f"CSM: {ticket['csm']} \n" \
                      f"Backup TAM(s): {ticket['backup_tam']} \n" \
                      f"Customer region:  {ticket['customer_region']} \n " \
                      f"BFG Link(s): {ticket['bfg_org_id']} \n " \
                      f"**Severity**: **{ticket['severity']}** \n " \

        data = {
            "text": msg_to_send,
            "markdown": msg_to_send,
            "high_touch_service": True
        }
        if ticket['ticket_id'] not in handled_tickets:
            sendMessageToWxT(data)
            handled_tickets.append(ticket['ticket_id'])
