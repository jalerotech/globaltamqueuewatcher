import logging
from datetime import datetime
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw
from ticketAndMsgHandlers.msgPoster import sendMessageToWxT
from reminderFeature.rmndrDataGenerator import rmndrDataWriter
from msgReply.replyMsgDataGenerator import rplyMsgDataWriter
import json

logger = logging.getLogger('Msg_handler')
processed_tickets = set()
ticket_id_company_mapping = []
msg_id_dict = {}
msg_id_list = []

currentDateAndTime = datetime.now()
current_time = currentDateAndTime.time()
today = currentDateAndTime.strftime('%A')
reminder_added = set()


def _callReminderFun(ticket):
    if ticket['assignee']:
        point_data = {
            "ticket_counter": ticket['ticket_counter'],
            "subject": ticket['subject'],
            "assignee": ticket['assignee'],
            "ticket_id": ticket['ticket_id'],
            "created_at": ticket['created_at']
        }
    else:
        point_data = {
            "ticket_counter": ticket['ticket_counter'],
            "subject": ticket['subject'],
            "ticket_id": ticket['ticket_id'],
            "created_at": ticket['created_at'],
            "assignee": None
        }
    return point_data


def postMsgTicketInfo(lont_w_OrgNames, TAMs_data):
    logger.info("Creating and posting messages to WebEx teams")
    """
    Send messages to WxT space after checking the TAM assigned to the customer on Monday.com.

    :param TAMs_data: List TAM to customer mappings.
    :param lont_w_OrgNames: List of new tickets with org names populated.
    :return: List -> list of handled tickets as soon as message is posted to WxT.
    """
    try:
        for ticket in lont_w_OrgNames:
            for tam_data in TAMs_data:
                try:
                    if ticket['ticket_id'] == tam_data['ticket_id']:
                        if ticket['ticket_id'] not in processed_tickets:
                            # Add the ticket to the processed tickets set before continuing
                            logger.info(f"Adding ticket {ticket['ticket_id']} to processed tickets.")
                            processed_tickets.add(ticket['ticket_id'])

                            timestamp = datetime.strptime(ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                            formatted_timestamp = timestamp.strftime("%H:%M:%S")

                            # Construct the message to send to the Webex Teams room
                            pickMsgToSend(tam_data, ticket, formatted_timestamp)
                            logger.info(f'Posting message to WebEx Teams space.')
                        else:
                            logger.info(f"Ticket {ticket['ticket_id']} has already been processed, Moving on.")
                except json.decoder.JSONDecodeError as a:
                    logger.info(f"Something failed in the 'postMsgTicketInfo' function with {a}")
            if not TAMs_data:
                tam_data = []
                if ticket['ticket_id'] not in processed_tickets:
                    # Add the ticket to the processed tickets set before continuing
                    logger.info(f"Adding ticket {ticket['ticket_id']} to processed tickets.")
                    processed_tickets.add(ticket['ticket_id'])

                    timestamp = datetime.strptime(ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                    formatted_timestamp = timestamp.strftime("%H:%M:%S")

                    # Construct the message to send to the Webex Teams room
                    pickMsgToSend(tam_data, ticket, formatted_timestamp)
                    logger.info(f'Posting message to WebEx Teams space.')
                else:
                    logger.info(f"Ticket {ticket['ticket_id']} has already been processed, Moving on.")
    except TypeError as e:
        logger.info(str(e))


def pickMsgToSend(tam_data, ticket, formatted_timestamp):
    """
    Produces the message (str) to send to WebEx teams given the data fetched from Monday.com and Zendesk.
    :param tam_data: list of ticket_ids, primary and backup TAMS and customer region.
    :param ticket: ticket information -> id, creation time etc.
    :param formatted_timestamp: Time of the ticket creation on Zendesk
    :return: msg_to_send [str]
    """
    logger.info('Creating personalized message to send to WxT space.')
    handled_tickets = []
    if tam_data:
        # This checks if the customer has region and both primary & backup TAMs on Monday.com
        try:
            # Extra check to make sure the ticket_ids from both data collected matches for accurate results.
            if tam_data['ticket_id'] == ticket['ticket_id']:
                if tam_data['primary_tam']:
                    if tam_data['backup_tam']:
                        if (tam_data['customer_region']) and (tam_data['bfg_org_id']):
                            if ticket['priority']:
                                msg_to_send = f"### New ticket has landed in the TAM Q !!! ({ticket['ticket_counter']}) \n " \
                                              f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                                              f"Subject: {ticket['subject']} \n " \
                                              f"Company name: **{ticket['org_name']}** \n " \
                                              f"Creation time in UTC: {formatted_timestamp} \n" \
                                              f"Primary TAM: {tam_data['primary_tam']} \n" \
                                              f"Backup TAM(s): {tam_data['backup_tam']} \n" \
                                              f"Customer region:  {tam_data['customer_region']} \n " \
                                              f"BFG Link(s): {tam_data['bfg_org_id']} \n " \
                                              f"**Priority**: **{ticket['priority']}** \n " \

                                data = {
                                    "text": msg_to_send,
                                    "markdown": msg_to_send
                                }
                                msg_id = sendMessageToWxT(data)
                                if msg_id:
                                    if msg_id not in msg_id_list:
                                        msg_id_dict.update({'msg_id': msg_id,
                                                            'ticket_id': ticket['ticket_id']})
                                        msg_id_list.append(ticket['ticket_id'])
                                if ticket['ticket_id'] not in reminder_added:
                                    rmndrDataWriter(_callReminderFun(ticket))
                                    reminder_added.add(ticket['ticket_id'])
                                    msg_dict_data = {'msg_id': msg_id,
                                                     'ticket_id': ticket['ticket_id']}
                                    rplyMsgDataWriter(msg_dict_data)
                                # _callReminderFun(ticket)

                                if ticket['ticket_id'] not in handled_tickets:
                                    handled_tickets.append(ticket['ticket_id'])
                                ticket_handled_data = {
                                    'ticket_id': ticket['ticket_id'],
                                    'customer_name': ticket['org_name']
                                }
                                if ticket_handled_data not in ticket_id_company_mapping:
                                    ticket_id_company_mapping.append(ticket_handled_data)
                            else:
                                msg_to_send = f"### New ticket has landed in the TAM Q !!! ({ticket['ticket_counter']}) \n " \
                                              f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                                              f"Subject: {ticket['subject']} \n " \
                                              f"Company name: **{ticket['org_name']}** \n " \
                                              f"Creation time in UTC: {formatted_timestamp} \n" \
                                              f"Primary TAM: {tam_data['primary_tam']} \n" \
                                              f"Backup TAM(s): {tam_data['backup_tam']} \n" \
                                              f"Customer region:  {tam_data['customer_region']} \n " \
                                              f"BFG Link(s): {tam_data['bfg_org_id']} \n "

                                data = {
                                    "text": msg_to_send,
                                    "markdown": msg_to_send
                                }
                                # sendMessageToWxT(data)
                                msg_id = sendMessageToWxT(data)
                                if msg_id:
                                    if msg_id not in msg_id_list:
                                        msg_id_dict.update({'msg_id': msg_id,
                                                            'ticket_id': ticket['ticket_id']})
                                        msg_id_list.append(ticket['ticket_id'])
                                if ticket['ticket_id'] not in reminder_added:
                                    rmndrDataWriter(_callReminderFun(ticket))
                                    reminder_added.add(ticket['ticket_id'])
                                    msg_dict_data = {'msg_id': msg_id,
                                                     'ticket_id': ticket['ticket_id']}
                                    rplyMsgDataWriter(msg_dict_data)

                                if ticket['ticket_id'] not in handled_tickets:
                                    handled_tickets.append(ticket['ticket_id'])
                                ticket_handled_data = {
                                    'ticket_id': ticket['ticket_id'],
                                    'customer_name': ticket['org_name']
                                }
                                if ticket_handled_data not in ticket_id_company_mapping:
                                    ticket_id_company_mapping.append(ticket_handled_data)
                # This checks if the customer has region set and has primary and NO backup TAMs on Monday.com
                if not tam_data['backup_tam']:
                    if tam_data['primary_tam']:
                        if tam_data['customer_region'] and tam_data['bfg_org_id']:
                            msg_to_send = f"### New ticket has landed in the TAM Q !!! ({ticket['ticket_counter']}) \n " \
                                          f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                                          f"Subject: {ticket['subject']} \n " \
                                          f"Company name: **{ticket['org_name']}** \n " \
                                          f"Creation time in UTC: {formatted_timestamp} \n" \
                                          f"Primary TAM: {tam_data['primary_tam']} \n" \
                                          f"Backup TAM(s): {tqw().unassigned_label} \n" \
                                          f"Customer region: {tam_data['customer_region']} \n " \
                                          f"BFG Link(s): {tam_data['bfg_org_id']} \n "

                            data = {
                                "text": msg_to_send,
                                "markdown": msg_to_send
                            }
                            # sendMessageToWxT(data)
                            msg_id = sendMessageToWxT(data)
                            if msg_id:
                                if msg_id not in msg_id_list:
                                    msg_id_dict.update({'msg_id': msg_id,
                                                        'ticket_id': ticket['ticket_id']})
                                    msg_id_list.append(ticket['ticket_id'])
                            if ticket['ticket_id'] not in reminder_added:
                                rmndrDataWriter(_callReminderFun(ticket))
                                reminder_added.add(ticket['ticket_id'])
                                msg_dict_data = {'msg_id': msg_id,
                                                 'ticket_id': ticket['ticket_id']}
                                rplyMsgDataWriter(msg_dict_data)

                            if ticket['ticket_id'] not in handled_tickets:
                                handled_tickets.append(ticket['ticket_id'])
                            ticket_handled_data = {
                                'ticket_id': ticket['ticket_id'],
                                'customer_name': ticket['org_name']
                            }
                            if ticket_handled_data not in ticket_id_company_mapping:
                                ticket_id_company_mapping.append(ticket_handled_data)

                # This checks if the customer has no region assigned and has both primary and backup TAMs on Monday.com
                if (tam_data['primary_tam']) and (tam_data['backup_tam']) and (not tam_data['customer_region']) and tam_data['bfg_org_id']:
                    msg_to_send = f"### New ticket has landed in the TAM Q !!! ({ticket['ticket_counter']}) \n " \
                                  f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                                  f"Subject: {ticket['subject']} \n " \
                                  f"Company name: **{ticket['org_name']}** \n " \
                                  f"Creation time in UTC: {formatted_timestamp} \n" \
                                  f"Primary TAM: {tam_data['primary_tam']} \n"\
                                  f"Backup TAM(s): {tam_data['backup_tam']} \n" \
                                  f"Customer region:  {tqw().not_set} \n " \
                                  f"BFG Link(s): {tam_data['bfg_org_id']} \n "
                    data = {
                        "text": msg_to_send,
                        "markdown": msg_to_send
                    }
                    # sendMessageToWxT(data)
                    msg_id = sendMessageToWxT(data)
                    if msg_id:
                        if msg_id not in msg_id_list:
                            msg_id_dict.update({'msg_id': msg_id,
                                                'ticket_id': ticket['ticket_id']})
                            msg_id_list.append(ticket['ticket_id'])
                    if ticket['ticket_id'] not in reminder_added:
                        rmndrDataWriter(_callReminderFun(ticket))
                        reminder_added.add(ticket['ticket_id'])
                        msg_dict_data = {'msg_id': msg_id,
                                         'ticket_id': ticket['ticket_id']}
                        rplyMsgDataWriter(msg_dict_data)

                    if ticket['ticket_id'] not in handled_tickets:
                        handled_tickets.append(ticket['ticket_id'])
                    ticket_handled_data = {
                        'ticket_id': ticket['ticket_id'],
                        'customer_name': ticket['org_name']
                    }
                    if ticket_handled_data not in ticket_id_company_mapping:
                        ticket_id_company_mapping.append(ticket_handled_data)

                # This checks if the customer has no region assigned and has primary TAM assigned but NO backup TAMs on Monday.com
                if (tam_data['primary_tam']) and (not tam_data['backup_tam']) and (not tam_data['customer_region']) and tam_data['bfg_org_id']:
                    # print(f"{ticket} matched case 4")
                    msg_to_send = f"### New ticket has landed in the TAM Q !!! ({ticket['ticket_counter']}) \n " \
                                  f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                                  f"Subject: {ticket['subject']} \n " \
                                  f"Company name: **{ticket['org_name']}** \n " \
                                  f"Creation time in UTC: {formatted_timestamp} \n" \
                                  f"Primary TAM: {tam_data['primary_tam']} \n" \
                                  f"Backup TAM(s): {tqw().unassigned_label} \n" \
                                  f"Customer region:  {tqw().not_set} \n " \
                                  f"BFG Link(s): {tam_data['bfg_org_id']} \n "
                    data = {
                        "text": msg_to_send,
                        "markdown": msg_to_send
                    }
                    # sendMessageToWxT(data)
                    msg_id = sendMessageToWxT(data)
                    if msg_id:
                        if msg_id not in msg_id_list:
                            msg_id_dict.update({'msg_id': msg_id,
                                                'ticket_id': ticket['ticket_id']})
                            msg_id_list.append(ticket['ticket_id'])
                    if ticket['ticket_id'] not in reminder_added:
                        rmndrDataWriter(_callReminderFun(ticket))
                        reminder_added.add(ticket['ticket_id'])
                        msg_dict_data = {'msg_id': msg_id,
                                         'ticket_id': ticket['ticket_id']}
                        rplyMsgDataWriter(msg_dict_data)

                    if ticket['ticket_id'] not in handled_tickets:
                        handled_tickets.append(ticket['ticket_id'])
                    ticket_handled_data = {
                        'ticket_id': ticket['ticket_id'],
                        'customer_name': ticket['org_name']
                    }
                    if ticket_handled_data not in ticket_id_company_mapping:
                        ticket_id_company_mapping.append(ticket_handled_data)

                # This checks if the customer has no region assigned and has primary TAM assigned but NO backup TAMs on Monday.com
                if (tam_data['primary_tam']) and (not tam_data['backup_tam']) and (not tam_data['customer_region']) and (not tam_data['bfg_org_id']):
                    msg_to_send = f"### New ticket has landed in the TAM Q !!! ({ticket['ticket_counter']}) \n " \
                                  f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                                  f"Subject: {ticket['subject']} \n " \
                                  f"Company name: **{ticket['org_name']}** \n " \
                                  f"Creation time in UTC: {formatted_timestamp} \n" \
                                  f"Primary TAM: {tam_data['primary_tam']} \n" \
                                  f"Backup TAM(s): {tqw().unassigned_label} \n" \
                                  f"Customer region:  {tqw().not_set} \n " \
                                  f"BFG Link(s): Unknown \n "
                    data = {
                        "text": msg_to_send,
                        "markdown": msg_to_send
                    }
                    # sendMessageToWxT(data)
                    msg_id = sendMessageToWxT(data)
                    if msg_id:
                        if msg_id not in msg_id_list:
                            msg_id_dict.update({'msg_id': msg_id,
                                                'ticket_id': ticket['ticket_id']})
                            msg_id_list.append(ticket['ticket_id'])
                    if ticket['ticket_id'] not in reminder_added:
                        rmndrDataWriter(_callReminderFun(ticket))
                        reminder_added.add(ticket['ticket_id'])
                        msg_dict_data = {'msg_id': msg_id,
                                         'ticket_id': ticket['ticket_id']}
                        rplyMsgDataWriter(msg_dict_data)

                    if ticket['ticket_id'] not in handled_tickets:
                        handled_tickets.append(ticket['ticket_id'])
                    ticket_handled_data = {
                        'ticket_id': ticket['ticket_id'],
                        'customer_name': ticket['org_name']
                    }
                    if ticket_handled_data not in ticket_id_company_mapping:
                        ticket_id_company_mapping.append(ticket_handled_data)

                else:
                    if ticket['ticket_id'] not in handled_tickets:
                        msg_to_send = f"### New ticket has landed in the TAM Q !!! ({ticket['ticket_counter']}) \n " \
                                      f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                                      f"Subject: {ticket['subject']} \n " \
                                      f"Company name: **{ticket['org_name']}** \n " \
                                      f"Creation time in UTC: {formatted_timestamp} \n" \
                                      f"Primary TAM: Unknown \n" \
                                      f"Backup TAM(s): Unknown \n" \
                                      f"Customer region: Unknown \n " \
                                      f"BFG Link(s): Unknown \n "
                        data = {
                            "text": msg_to_send,
                            "markdown": msg_to_send
                        }
                        # sendMessageToWxT(data)
                        msg_id = sendMessageToWxT(data)
                        if msg_id:
                            if msg_id not in msg_id_list:
                                msg_id_dict.update({'msg_id': msg_id,
                                                    'ticket_id': ticket['ticket_id']})
                                msg_id_list.append(ticket['ticket_id'])
                        if ticket['ticket_id'] not in reminder_added:
                            rmndrDataWriter(_callReminderFun(ticket))
                            reminder_added.add(ticket['ticket_id'])
                            msg_dict_data = {'msg_id': msg_id,
                                             'ticket_id': ticket['ticket_id']}
                            rplyMsgDataWriter(msg_dict_data)

                        if ticket['ticket_id'] not in handled_tickets:
                            handled_tickets.append(ticket['ticket_id'])
                        ticket_handled_data = {
                            'ticket_id': ticket['ticket_id'],
                            'customer_name': ticket['org_name']
                        }
                        if ticket_handled_data not in ticket_id_company_mapping:
                            ticket_id_company_mapping.append(ticket_handled_data)
            else:
                if ticket['ticket_id'] not in handled_tickets:
                    msg_to_send = f"### New ticket has landed in the TAM Q !!! ({ticket['ticket_counter']}) \n " \
                                  f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                                  f"Subject: {ticket['subject']} \n " \
                                  f"Company name: **{ticket['org_name']}** \n " \
                                  f"Creation time in UTC: {formatted_timestamp} \n" \
                                  f"Primary TAM: Unknown \n" \
                                  f"Backup TAM(s): Unknown \n" \
                                  f"Customer region: Unknown \n " \
                                  f"BFG Link(s): Unknown \n "
                    data = {
                        "text": msg_to_send,
                        "markdown": msg_to_send
                    }
                    # sendMessageToWxT(data)
                    msg_id = sendMessageToWxT(data)
                    if msg_id:
                        if msg_id not in msg_id_list:
                            msg_id_dict.update({'msg_id': msg_id,
                                                'ticket_id': ticket['ticket_id']})
                            msg_id_list.append(ticket['ticket_id'])
                    if ticket['ticket_id'] not in reminder_added:
                        rmndrDataWriter(_callReminderFun(ticket))
                        reminder_added.add(ticket['ticket_id'])
                        msg_dict_data = {'msg_id': msg_id,
                                         'ticket_id': ticket['ticket_id']}
                        rplyMsgDataWriter(msg_dict_data)

                    if ticket['ticket_id'] not in handled_tickets:
                        handled_tickets.append(ticket['ticket_id'])
                    ticket_handled_data = {
                        'ticket_id': ticket['ticket_id'],
                        'customer_name': ticket['org_name']
                    }
                    if ticket_handled_data not in ticket_id_company_mapping:
                        ticket_id_company_mapping.append(ticket_handled_data)

        except KeyError as e:
            logger.info(f'{tam_data} is Missing information {e.args}')

    else:
        if ticket['ticket_id'] not in handled_tickets:
            msg_to_send = f"### New ticket has landed in the TAM Q !!! ({ticket['ticket_counter']}) \n " \
                          f"Ticket number: #[{ticket['ticket_id']}]({tqw().zend_agent_tickets_url}{ticket['ticket_id']}) \n " \
                          f"Subject: {ticket['subject']} \n " \
                          f"Company name: **{ticket['org_name']}** \n " \
                          f"Creation time in UTC: {formatted_timestamp} \n" \
                          f"Primary TAM: Unknown \n" \
                          f"Backup TAM(s): Unknown \n" \
                          f"Customer region: Unknown \n " \
                          f"BFG Link(s): unknown \n "
            data = {
                "text": msg_to_send,
                "markdown": msg_to_send
            }
            # sendMessageToWxT(data)
            msg_id = sendMessageToWxT(data)
            if msg_id:
                if msg_id not in msg_id_list:
                    msg_id_dict.update({'msg_id': msg_id,
                                        'ticket_id': ticket['ticket_id']})
                    msg_id_list.append(ticket['ticket_id'])
            if ticket['ticket_id'] not in reminder_added:
                rmndrDataWriter(_callReminderFun(ticket))
                reminder_added.add(ticket['ticket_id'])
                msg_dict_data = {'msg_id': msg_id,
                                 'ticket_id': ticket['ticket_id']}
                rplyMsgDataWriter(msg_dict_data)

            if ticket['ticket_id'] not in handled_tickets:
                handled_tickets.append(ticket['ticket_id'])
            ticket_handled_data = {
                'ticket_id': ticket['ticket_id'],
                'customer_name': ticket['org_name']
            }
            if ticket_handled_data not in ticket_id_company_mapping:
                ticket_id_company_mapping.append(ticket_handled_data)


def postCollabTicketMsg(data) -> None:
    """
    Adds the collab ticket to processed ticket set before calling the sendMessageToWxT function.
    :param data: dict
    :return: None
    """
    handled_collab_tickets = []
    if (data['id'] not in processed_tickets) and (data['id'] not in handled_collab_tickets):
        # Add the ticket to the processed tickets set before continuing
        logger.info(f"Adding ticket {data['id']} to processed tickets. - STARTED")
        processed_tickets.add(data['id'])
        logger.info(f"Adding ticket {data['id']} to processed tickets. - COMPLETED")

        msg_to_send = f"### New TAC Collab ticket has landed in the TAM Q !!! ({data['ticket_counter']}) \n " \
                      f"Ticket number: #[{data['id']}]({tqw().zend_agent_tickets_url}{data['id']}) \n " \
                      f"Subject: {data['subject']} \n " \
                      f"Company name: **{data['org_name']}** \n " \
                      f"Creation time in UTC: {data['formatted_timestamp']} \n" \
                      f"TAC SR: [{data['SR_number']}]({tqw().csone_short_base_url}{data['SR_number']}) \n "
        msg_data = {
            "text": msg_to_send,
            "markdown": msg_to_send
        }
        # sendMessageToWxT(msg_data)
        msg_id = sendMessageToWxT(data)
        if msg_id:
            if msg_id not in msg_id_list:
                msg_id_dict.update({'msg_id': msg_id,
                                    'ticket_id': data['ticket_id']})
                msg_id_list.append(data['ticket_id'])
        if data['ticket_id'] not in reminder_added:
            rmndrDataWriter(_callReminderFun(data))
            reminder_added.add(data['ticket_id'])
            msg_dict_data = {'msg_id': msg_id,
                             'ticket_id': data['ticket_id']}
            rplyMsgDataWriter(msg_dict_data)

        ticket_handled_data = {
            'ticket_id': data['id'],
            'customer_name': data['org_name']
        }
        if data['id'] not in handled_collab_tickets:
            handled_collab_tickets.append(data['id'])
        if ticket_handled_data not in ticket_id_company_mapping:
            ticket_id_company_mapping.append(ticket_handled_data)
    else:
        logger.info(f"Ticket {data['id']} has already been processed, Moving on.")
    return None


# def ticketDataForStats() -> list[dict]:
#     """
#     Produces the number of tickets handled today mapping with company/customer's name
#     This happens a minute before the end of each shift (theatre)
#     :return:
#     """
#     # APAC
#     if datetime.now().hour == 9 and (0 <= datetime.now().minute < 3):
#         return ticket_id_company_mapping
#     # EMEA
#     if datetime.now().hour == 16 and (0 <= datetime.now().minute < 3):
#         return ticket_id_company_mapping
#     # US
#     if datetime.now().hour == 2 and (0 <= datetime.now().minute < 3):
#         return ticket_id_company_mapping


def returnCurrentDataForStats() -> list[dict]:
    return ticket_id_company_mapping


def retMsgList_MsgDict():
    return msg_id_dict, msg_id_list


def writeMsgList_MsgDict_to_file():
    return msg_id_dict, msg_id_list


def reset_processed_tickets() -> None:
    logger.info(f"length of 'processed_ticket_set' is {len(processed_tickets)}.")
    logger.info("Resetting the 'processed_ticket set to be a length of 0'")
    """
    resets the processed ticket set to a length of 0 to save memory usage.
    :return: 
    """
    processed_tickets.clear()
    logger.info(f"length of 'processed_ticket_set' is now {len(processed_tickets)}.")
    logger.info("Resetting the 'processed_ticket set to be a length of 0'...=> COMPLETED")


def reset_tickets_handled_today() -> None:
    logger.info(f"length of 'tickets_handled_today' is {len(ticket_id_company_mapping)}.")
    logger.info("Resetting the 'tickets_handled_today set to be a length of 0'")
    """
    resets the tickets_handled_today list to a length of 0 to save memory usage.
    :return: None
    """
    ticket_id_company_mapping.clear()
    logger.info(f"length of 'tickets_handled_today' is now {len(ticket_id_company_mapping)}.")
    logger.info("Resetting the 'tickets_handled_today to be a length of 0'...=> COMPLETED")
