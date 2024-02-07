import logging
from datetime import datetime, timedelta, timezone
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw
from ticketAndMsgHandlers.msgPoster import sendMessageToWxT
from reminderFeature.assigneeInfo import get_user_info

reminder_sent = []
current_time = datetime.utcnow()
is_assigned_msg_sent = []


def createRmndrMsg(list_of_ticket) -> None:
    logger = logging.getLogger('Reminder Services')
    """
    Creates the reminder message using the list_of_ticket received from processReminderData function
    which returns the data in dict format
    :param list_of_ticket:
    :return: None
    """
    if list_of_ticket:
        for ticket in list_of_ticket:
            # Initialize empty dict for the is_assigned information.
            is_assigned = {}
            # Ensures that the ticket is not completely processed in the case of when it's been assigned already
            if ticket['ticket_id'] not in is_assigned_msg_sent:
                is_assigned = get_user_info(ticket)
            if ticket['ticket_id'] not in reminder_sent:
                # time_in_queue = _IsTimeDifMoreThan30Mins(ticket)
                if _IsTimeDifMoreThan30Mins(ticket):
                    time_in_queue = f"{_IsTimeDifMoreThan30Mins(ticket)[0]['hours']} hour(s) and {_IsTimeDifMoreThan30Mins(ticket)[0]['minutes']} minute(s)."
                    # Checks if the reminder should be triggered and ticket is not yet assigned.
                    if reminder_trigger(ticket, is_assigned) and not is_assigned:
                        logger.info(f"Creating Reminder Message - STARTED")
                        RmndrMsg = f"### ⏰Reminder !!! ({ticket['ticket_counter']}) _(Beta)_ \n " \
                                   f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                                   f"Subject: {ticket['subject']} \n " \
                                   f"In Queue for: {time_in_queue} \n " ""
                        data = {
                            "text": RmndrMsg,
                            "markdown": RmndrMsg
                        }
                        logger.info(f"Creating Reminder Message - COMPLETED")
                        logger.info(f"Sending Reminder for {ticket['ticket_id']} -> STARTED")
                        sendMessageToWxT(data)
                        reminder_sent.append(ticket['ticket_id'])
                        logger.info(f"Sending Reminder for {ticket['ticket_id']} -> COMPLETED")
                # Checks if the ticket is already assigned and hasn't been completely processed.
            if is_assigned:
                if ticket['ticket_id'] not in is_assigned_msg_sent:
                    # time_in_queue = _IsTimeDifMoreThan30Mins(ticket)
                    logger.info(f"Triggering ticket Assignment alert for ticket -> {ticket['ticket_id']} - STARTED")
                    logger.info(f"Creating ticket Assignment Message for {ticket['ticket_id']} - STARTED")
                    ticket_assigned_msg = \
                        f"### ✅Ticket Assignment ({ticket['ticket_counter']}) _(Beta)_ \n " \
                        f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                        f"Subject: {ticket['subject']} \n " \
                        f"Assigned to: {is_assigned['Email']} \n "
                    data = {
                        "text": ticket_assigned_msg,
                        "markdown": ticket_assigned_msg
                    }
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
    :return:bool (True or False)
    """
    logger.info(f"Checking if reminder is needed for ticket {ticket['ticket_id']}")
    if _IsTimeDifMoreThan30Mins(ticket):
        time_in_queue = f"{_IsTimeDifMoreThan30Mins(ticket)[0]['hours']} hour(s) and {_IsTimeDifMoreThan30Mins(ticket)[0]['minutes']} minutes."
        to_trigger_reminder = _IsTimeDifMoreThan30Mins(ticket)[1]
        if to_trigger_reminder:
            if is_assigned:
                logger.info(f"No reminder needed for {ticket['ticket_id']} as it's already been assigned.")
                return False
            else:
                logger.info(f"Sending Reminder for {ticket['ticket_id']}")
                return True
        else:
            logger.info(f"No reminder needed for {ticket['ticket_id']} as it's {time_in_queue} in the Queue.")
            logger.info(f"Time difference on ticket with ID {ticket['ticket_id']} is {time_in_queue}")
            return False


def _IsTimeDifMoreThan30Mins(ticket) -> tuple:
    ticket_open_time = datetime.strptime(ticket['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    current_time_utc = datetime.now(timezone.utc)

    # Convert the datetime objects to Unix timestamps
    ticket_timestamp_unix = int(ticket_open_time.timestamp())
    current_time_unix = int(current_time_utc.timestamp())

    # Calculate the absolute difference in seconds
    time_difference_seconds = abs(current_time_unix - ticket_timestamp_unix)
    ticket_time_in_queue = _convert_seconds_to_hours_minutes(time_difference_seconds)
    if ticket_time_in_queue['minutes'] >= 30:
        return ticket_time_in_queue, True


def _convert_seconds_to_hours_minutes(seconds):
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
