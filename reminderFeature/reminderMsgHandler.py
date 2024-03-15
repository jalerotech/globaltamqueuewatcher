import logging
from datetime import datetime, timedelta, timezone
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw
from reminderFeature.assigneeInfo import get_user_info
from msgReply.readfromReplyDatarFile import read_json_file_line_by_line
from msgReply.replyMsgs import reply_to_message
from tamTicketStats.tamStatsGenerator import TamStatsDataWriter

first_reminder_sent = []
second_reminder_sent = []
third_reminder_sent = []
current_time = datetime.utcnow()
is_assigned_msg_sent = []
tam_assigned_tickets_stats = {}

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Reminder Message Handler')


def returnReplyMsgId(ticket_id):
    """
    Returns the message id of the parent message sent initially. This ID is to be used to reply to the initial message
    using the initial message id as the reply message's parentId.
    :param ticket_id:
    :return: None
    """
    for msg_info in read_json_file_line_by_line():
        if msg_info['ticket_id'] == ticket_id:
            return msg_info['msg_id']


def createRmndrMsg(list_of_ticket):
    # logger = logging.getLogger('Reminder Services')
    """
    Creates the reminder message using the list_of_ticket received from processReminderData function
    which returns the data in dict format
    :param list_of_ticket:
    :return: None
    """
    if list_of_ticket:
        for ticket in list_of_ticket:
            is_assigned = {}
            # Ensures that the ticket is not completely processed in the case of when it's been assigned already
            if ticket['ticket_id'] not in is_assigned_msg_sent:
                is_assigned = get_user_info(ticket)
                if _IsTimeDifMoreThan30Mins(ticket):
                    time_in_queue = f"{_IsTimeDifMoreThan30Mins(ticket)[0]['hours']} hour(s) and {_IsTimeDifMoreThan30Mins(ticket)[0]['minutes']} minute(s)."
                    to_trigger_reminder = _IsTimeDifMoreThan30Mins(ticket)[1]
                    # Checks if the reminder should be triggered and ticket is not yet assigned.
                    if reminder_trigger(ticket, is_assigned) and not is_assigned:
                        if ticket['ticket_id'] not in first_reminder_sent:
                            if to_trigger_reminder == "HALF_HOUR":
                                logger.info(f"Creating First Reminder Message - STARTED")
                                # RmndrMsg = f"### ⏰First Reminder !!! ({ticket['ticket_counter']}) \n " \
                                #            f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                                #            f"In Queue for: {time_in_queue} \n " ""
                                RmndrMsg = f"### ⏰First Reminder !!! ({ticket['ticket_counter']}) \n " \
                                           f"In Queue for: {time_in_queue} \n " ""
                                data = {
                                    "text": RmndrMsg,
                                    "markdown": RmndrMsg
                                }
                                logger.info(f"Creating First Reminder Message - COMPLETED")
                                logger.info(f"Sending First Reminder for {ticket['ticket_id']} -> STARTED")
                                reply_to_message(returnReplyMsgId(ticket['ticket_id']), data)
                                first_reminder_sent.append(ticket['ticket_id'])
                                logger.info(f"Sending First Reminder for {ticket['ticket_id']} -> COMPLETED")
                            else:
                                logger.info(f"Ticket {ticket['ticket_id']} not yet ready for First reminder.")

                        if ticket['ticket_id'] not in second_reminder_sent:
                            if to_trigger_reminder == "QUARTER_HOUR":
                                logger.info(f"Creating Second Reminder Message - STARTED")
                                # RmndrMsg = f"### ⏰Reminder !!! ({ticket['ticket_counter']}) (#2) _(Beta)_ \n " \
                                #            f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                                #            f"In Queue for: {time_in_queue} \n " ""
                                # RmndrMsg = f"### ⏰Second Reminder !!! ({ticket['ticket_counter']}) \n " \
                                #            f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                                #            f"In Queue for: {time_in_queue} \n " ""
                                RmndrMsg = f"### ⏰Second Reminder !!! ({ticket['ticket_counter']}) \n " \
                                           f"In Queue for: {time_in_queue} \n " ""
                                data = {
                                    "text": RmndrMsg,
                                    "markdown": RmndrMsg
                                }
                                logger.info(f"Creating Second Reminder Message - COMPLETED")
                                logger.info(f"Sending Second Reminder for {ticket['ticket_id']} -> STARTED")
                                reply_to_message(returnReplyMsgId(ticket['ticket_id']), data)
                                second_reminder_sent.append(ticket['ticket_id'])
                                logger.info(f"Sending Second Reminder for {ticket['ticket_id']} -> COMPLETED")
                            else:
                                logger.info(f"Ticket {ticket['ticket_id']} not yet ready for second reminder.")

                        if ticket['ticket_id'] not in third_reminder_sent:
                            if to_trigger_reminder == "HOUR":
                                logger.info(f"Creating Final Reminder Message - STARTED")
                                # RmndrMsg = f"### ⏰Final Reminder !!! ({ticket['ticket_counter']}) \n " \
                                #            f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                                #            f"In Queue for: {time_in_queue} \n " ""
                                RmndrMsg = f"### ⏰Final Reminder !!! ({ticket['ticket_counter']}) \n " \
                                           f"In Queue for: {time_in_queue} \n " ""
                                data = {
                                    "text": RmndrMsg,
                                    "markdown": RmndrMsg
                                }
                                logger.info(f"Creating Final Reminder Message - COMPLETED")
                                logger.info(f"Sending Final Reminder for {ticket['ticket_id']} -> STARTED")
                                reply_to_message(returnReplyMsgId(ticket['ticket_id']), data)
                                third_reminder_sent.append(ticket['ticket_id'])
                                logger.info(f"Sending Final for {ticket['ticket_id']} -> COMPLETED")
                            else:
                                logger.info(f"Ticket {ticket['ticket_id']} not yet ready for final reminder.")
            # Checks if the ticket is already assigned and hasn't been completely processed.
            if is_assigned:
                if is_assigned['Email'] not in tam_assigned_tickets_stats:
                    tam_assigned_tickets_stats.update({is_assigned['Email']: []})
                if ticket['ticket_id'] not in is_assigned_msg_sent:
                    email = is_assigned['Email']
                    tam_assigned_tickets_stats[email].append(ticket['ticket_id'])
                    logger.info(f"Triggering ticket Assignment alert for ticket -> {ticket['ticket_id']} - STARTED")
                    logger.info(f"Creating ticket Assignment Message for {ticket['ticket_id']} - STARTED")
                    # ticket_assigned_msg = \
                    #     f"### ✅Ticket Assignment ({ticket['ticket_counter']}) \n " \
                    #     f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                    #     f"Assigned to: <@personEmail:{is_assigned['Email']}> \n "
                    ticket_assigned_msg = \
                        f"### ✅Ticket Assignment ({ticket['ticket_counter']}) \n " \
                        f"Assigned to: <@personEmail:{is_assigned['Email']}> \n "
                    data = {
                        "text": ticket_assigned_msg,
                        "markdown": ticket_assigned_msg
                    }
                    logger.info(f"Creating ticket Assignment Message for {ticket['ticket_id']} - COMPLETED")
                    logger.info(f"Sending Ticket Assignment message for {ticket['ticket_id']} -> STARTED")
                    reply_to_message(returnReplyMsgId(ticket['ticket_id']), data)
                    is_assigned_msg_sent.append(ticket['ticket_id'])
                    logger.info(f"Sending Ticket Assignment message for {ticket['ticket_id']} -> COMPLETED")
                    logger.info(f"Triggering ticket Assignment alert for ticket -> {ticket['ticket_id']} - COMPLETED")
                else:
                    logger.info(f"Ticket {ticket['ticket_id']} is not yet assigned.")
        TamStatsDataWriter(tam_assigned_tickets_stats)
        logger.info(f"Processed tickets -> {is_assigned_msg_sent}")


def reminder_trigger(ticket, is_assigned) -> tuple:
    logger = logging.getLogger('Reminder Trigger')
    """
    Returns True if the ticket has been created more than 30 minutes ago and has not been assigned.
    :param ticket:
    :return:Tuple Bool & trigger_data
    """
    logger.info(f"Checking if reminder is needed for ticket {ticket['ticket_id']}")
    if _IsTimeDifMoreThan30Mins(ticket):
        time_in_queue = f"{_IsTimeDifMoreThan30Mins(ticket)[0]['hours']} hour(s) and {_IsTimeDifMoreThan30Mins(ticket)[0]['minutes']} minutes."
        to_trigger_reminder = _IsTimeDifMoreThan30Mins(ticket)[1]
        if to_trigger_reminder:
            if is_assigned:
                logger.info(f"No reminder needed for {ticket['ticket_id']} as it's already been assigned.")
                return to_trigger_reminder, False
            else:
                logger.info(f"Sending Reminder for {ticket['ticket_id']}")
                return to_trigger_reminder, True
        else:
            logger.info(f"No reminder needed for {ticket['ticket_id']} as it's {time_in_queue} in the Queue.")
            logger.info(f"Time difference on ticket with ID {ticket['ticket_id']} is {time_in_queue}")
            return to_trigger_reminder, False


def _IsTimeDifMoreThan30Mins(ticket):
    """
    Checks if the time difference is at least 30 minutes before enabling the trigger.
    :param ticket: ticket data -> ticket_id, ticket_open_time etc.
    :return: time_in_queue in minutes and trigger labels
    """
    ticket_open_time = datetime.strptime(ticket['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    current_time_utc = datetime.now(timezone.utc)

    # Convert the datetime objects to Unix timestamps
    ticket_timestamp_unix = int(ticket_open_time.timestamp())
    current_time_unix = int(current_time_utc.timestamp())

    # Calculate the absolute difference in seconds
    time_difference_seconds = abs(current_time_unix - ticket_timestamp_unix)
    ticket_time_in_queue = _convert_seconds_to_hours_minutes(time_difference_seconds)
    if (30 <= ticket_time_in_queue['minutes'] < 31) and ticket_time_in_queue['hours'] == 0:
        return ticket_time_in_queue, tqw().half_hour_trigger
    if (45 <= ticket_time_in_queue['minutes'] < 47) and ticket_time_in_queue['hours'] == 0:
        return ticket_time_in_queue, tqw().quarter_hour_trigger
    if ticket_time_in_queue['hours'] == 1 and ticket_time_in_queue['minutes'] < 2:
        return ticket_time_in_queue, tqw().hour_trigger
    else:
        return None


def _convert_seconds_to_hours_minutes(seconds) -> dict:
    """
    converts the absolute time to seconds.
    :param seconds:
    :return: dict - time in queue in dict format.
    """
    # Calculate hours and minutes
    hours = seconds // 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds // 60
    # EMEA time is currently UTC+1 so need to deduct this from the ticket time (in UTC).
    if hours >= 1:
        utc_minus_one = hours - 1
        # time_in_queue = f"{utc_minus_one} Hour(s) and {minutes} Minutes"
        time_in_queue = {
            "hours": utc_minus_one,
            "minutes": minutes
        }
        return time_in_queue
    else:
        # time_in_queue = f"{hours} Hour(s) and {minutes} Minutes"
        time_in_queue = {
            "hours": hours,
            "minutes": minutes
        }
        return time_in_queue


def ret_tam_assigned_tickets_stats():
    print(f'tam_assigned_tickets_stats -> {tam_assigned_tickets_stats}')
    return tam_assigned_tickets_stats


def reset_tam_assigned_tickets_stats():
    logger.info(f'Current tam_assigned_tickets_stats -> {tam_assigned_tickets_stats}')
    logger.info(f'Resetting tam_assigned_tickets_stats - STARTED')
    tam_assigned_tickets_stats.clear()
    logger.info(f'Resetting tam_assigned_tickets_stats - COMPLETED')
