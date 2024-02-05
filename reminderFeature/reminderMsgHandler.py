import logging
import requests
from datetime import datetime, timedelta
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw
from ticketAndMsgHandlers.msgPoster import sendMessageToWxT
from reminderFeature.assigneeInfo import get_user_info

reminder_sent = []
reminder_1_sent = []
reminder_2_sent = []
reminder_3_sent = []
rmndr_interval = 10  # 15 minutes or 900 seconds reminder interval
current_time = datetime.utcnow()
is_assigned_msg_sent = []


def createRmndrMsg(list_of_ticket) -> None:
    logger = logging.getLogger('Reminder Services')
    """
    Creates the reminder message using the list_of_ticket received from processReminderData function
    which returns the data in dict format
    :param list_of_ticket:
    :return: string
    """
    # print(list_of_ticket)
    if list_of_ticket:
        for ticket in list_of_ticket:
            is_assigned = get_user_info(ticket)
            if ticket['ticket_id'] not in reminder_sent:
                ticket_open_time = datetime.strptime(ticket['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                time_difference = abs(current_time - ticket_open_time)
                if reminder_trigger(ticket, is_assigned) and not is_assigned:
                    logger.info(f"Creating Reminder Message - STARTED")
                    RmndrMsg = f"### ⏰Reminder !!! ({ticket['ticket_counter']}) \n " \
                               f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                               f"Subject: {ticket['subject']} \n " \
                               f"In Queue for: {time_difference} \n " ""
                    data = {
                        "text": RmndrMsg,
                        "markdown": RmndrMsg
                    }
                    logger.info(f"Creating Reminder Message - COMPLETED")
                    logger.info(f"Sending Reminder for {ticket['ticket_id']} -> STARTED")
                    sendMessageToWxT(data)
                    reminder_sent.append(ticket['ticket_id'])
                    logger.info(f"Sending Reminder for {ticket['ticket_id']} -> COMPLETED")
            if is_assigned:
                # if (ticket['ticket_id'] not in is_assigned_msg_sent) and (ticket['ticket_id'] not in reminder_sent):
                if ticket['ticket_id'] not in is_assigned_msg_sent:
                    logger.info(f"Triggering ticket Assignment alert for ticket -> {ticket['ticket_id']} - STARTED")
                    logger.info(f"Creating ticket Assignment Message for {ticket['ticket_id']} - STARTED")
                    ticket_assigned_msg = \
                        f"### ✅Ticket Assignment ({ticket['ticket_counter']}) \n " \
                        f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                        f"Subject: {ticket['subject']} \n " \
                        f"Assigned to: {is_assigned['Email']} \n "
                    data = {
                        "text": ticket_assigned_msg,
                        "markdown": ticket_assigned_msg
                    }
                    # ‹@personEmail:jane@example.com>
                    logger.info(f"Creating ticket Assignment Message for {ticket['ticket_id']} - COMPLETED")
                    logger.info(f"Sending Ticket Assignment message for {ticket['ticket_id']} -> STARTED")
                    sendMessageToWxT(data)
                    is_assigned_msg_sent.append(ticket['ticket_id'])
                    reminder_sent.append(ticket['ticket_id'])
                    logger.info(f"Sending Ticket Assignment message for {ticket['ticket_id']} -> COMPLETED")
                    logger.info(f"Triggering ticket Assignment alert for ticket -> {ticket['ticket_id']} - COMPLETED")
            else:
                logger.info(f"Ticket {ticket['ticket_id']} is already processed.")


def reminder_trigger(ticket, is_assigned) -> bool:
    logger = logging.getLogger('Reminder Trigger')
    """
    Returns True if the ticket has been created more than 30 minutes ago and has not been assigned.
    :param ticket:
    :return:
    """
    logger.info(f"Checking if reminder is needed for ticket {ticket['ticket_id']}")
    ticket_open_time = datetime.strptime(ticket['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    time_difference = abs(current_time - ticket_open_time)
    # print(current_time)
    # print(ticket_open_time)
    # print(time_difference)
    if time_difference >= timedelta(minutes=30):
        if is_assigned:
            logger.info(f"No reminder needed for {ticket['ticket_id']} as it's already been assigned.")
            return False
        else:
            logger.info(f"Sending Reminder for {ticket['ticket_id']}")
            return True
    else:
        time_difference_test = abs(current_time - datetime.strptime(ticket['created_at'], '%Y-%m-%dT%H:%M:%SZ'))
        logger.info(f"No reminder needed for {ticket['ticket_id']} as it's not older than 30 minutes in the Queue.")
        logger.info(f"Time difference on ticket with ID {ticket['ticket_id']} is {time_difference_test}")
        return False
