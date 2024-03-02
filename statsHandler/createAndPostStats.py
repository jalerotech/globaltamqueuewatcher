import logging
from datetime import datetime
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tQw
from ticketAndMsgHandlers.handleTicketMessages import reset_tickets_handled_today, reset_processed_tickets
from zendeskData.fetchProcessZendeskData import reset_sets_of_tickets_no_time_check
from ticketAndMsgHandlers.msgPoster import sendMessageToWxT
from statsHandler.ticketStatsWritingClass import TicketStats as DoStats
from collections import defaultdict
from Tools.jsonFileCleaner import cleanJsonFiles

logger = logging.getLogger('Creating and Posting Summary')
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M :%S')
currentDateAndTime = datetime.now()
today = currentDateAndTime.strftime('%A')


def _createStatsMsg(tickets_cust_handled_today, shift_data) -> str:
    """
    Creates the Summary message using the data received -> tickets_cust_handled_today
    :param tickets_cust_handled_today -> customer and ticket_id mappings.
    :param shift_data -> Theatre str (APAC, EMEA or US)
    :return: msg_to_send (str)
    """
    stats_str = ''
    counter = 0
    ticket_added_to_stats = []
    if len(tickets_cust_handled_today) == 1:
        logger.info(f"Generating {shift_data['theatre']} summary message. - STARTED")
        item = tickets_cust_handled_today[0]
        stats_str = f"1. **Ticket #**: {item['ticket_id']}, **Company Name**: {item['customer_name']} \n"
        ticket_added_to_stats.append(item['ticket_id'])
        msg_to_send = f"### **Statistics from {shift_data['theatre']} shift of today:** \n " \
                      f"Total number of tickets: **{len(tickets_cust_handled_today)}** \n " \
                      f"{stats_str}"
        logger.info(f"Generating {shift_data['theatre']} statistics message. - COMPLETED")
        logger.info(f"Produced stats message -> {msg_to_send}")
        return msg_to_send
    else:
        logger.info(f"Generating {shift_data['theatre']}  statistics message. - STARTED")
        for item in tickets_cust_handled_today:
            for i in range(1, (len(tickets_cust_handled_today))):
                if item['ticket_id'] not in ticket_added_to_stats:
                    counter += i
                    stats_str += f"{counter}. **Ticket #**: {item['ticket_id']}, **Company Name**: {item['customer_name']} \n"
                    ticket_added_to_stats.append(item['ticket_id'])
        msg_to_send = f"### **Statistics from {shift_data['theatre']}  shift of today:** \n " \
                      f"Total number of tickets: **{len(tickets_cust_handled_today)}** \n " \
                      f"{stats_str}"
        logger.info(f"Generating {shift_data['theatre']} statistics message. - COMPLETED")
        logger.info(f"Produced stats message -> {msg_to_send}")
        return msg_to_send


def _tallyTicketsPerCustomer(input_data) -> [dict, list]:
    """
    Tallies up the tickets per customer and creates a dict with a list of tickets per customer.
    Also creates a list of company/customer names.
    :param input_data: customer and ticket_id mapping.
    :return: ticketListPerOrg, org_list
    """
    ticketListPerOrg = defaultdict(list)
    org_list = []
    for cust_data in input_data:
        ticket_w_url = f"[{cust_data['ticket_id']}]({tQw().zend_agent_tickets_url}{cust_data['ticket_id']})"
        ticketListPerOrg[cust_data['customer_name']].append(ticket_w_url)
        org_list.append(cust_data['customer_name'])

    return ticketListPerOrg, org_list


def _createStatsMsg_v2(tickets_cust_handled_today, shift_data) -> str:
    """
    Creates the summary message using the data received -> tickets_cust_handled_today
    :param tickets_cust_handled_today -> customer and ticket_id mappings.
    :param shift_data -> Theatre str (APAC, EMEA or US)
    :return: msg_to_send (str)
    """
    ticketListPerOrg, org_list = _tallyTicketsPerCustomer(tickets_cust_handled_today)
    stats_str = ''
    counter = 0
    ticket_added_to_stats = []
    if len(org_list) == 1:
        logger.info(f"Generating {shift_data['theatre']} Summary message. - STARTED")
        org_name = org_list[0]
        joined_ticket_list = ', '.join(ticketListPerOrg[org_name])
        stats_str = f"1. **Company name**: _{org_name}_ \n **Ticket(s)**: {joined_ticket_list} \n "
        ticket_added_to_stats.append(ticketListPerOrg['ticket_id'])
        msg_to_send = f"### **📊 Summary of today's {shift_data['theatre']} shift:** \n " \
                      f"Total number of tickets: **{len(org_list)}** \n " \
                      f"{stats_str}"
        logger.info(f"Generating {shift_data['theatre']} Summary message. - COMPLETED")
        return msg_to_send
    else:
        logger.info(f"Generating {shift_data['theatre']} Summary message. - STARTED")
        for org in org_list:
            for i in range(1, (len(org_list))):
                if ticketListPerOrg[org] not in ticket_added_to_stats:
                    counter += i
                    joined_ticket_list = ', '.join(ticketListPerOrg[org])
                    stats_str += f"{counter}. **Company name**: _{org}_ \n **Ticket(s)**: {joined_ticket_list} \n "
                    ticket_added_to_stats.append(ticketListPerOrg[org])
        msg_to_send = f"### **📊 Summary of today's {shift_data['theatre']} shift:** \n " \
                      f"Total number of tickets: **{len(org_list)}** \n " \
                      f"{stats_str}"
        logger.info(f"Generating {shift_data['theatre']} summary message. - COMPLETED")
        logger.info(f"Produced stats message -> {msg_to_send}")
        return msg_to_send


def postDailyStatistics_V2(ticket_id_company_mapping, shift_data) -> None:

    """
    Posts daily ticket summary to WxT at the specified times.
    :param ticket_id_company_mapping -> ticket_id and company mapping.
    :param shift_data
    :return: None
    """
    # Only start preparing summary when shift status received is = ended.
    if shift_data:
        if shift_data['status'] == "ended 🏁":
            logger.info(f"Got shift data {shift_data} and theatre is {shift_data['theatre']}, attempting to produce the summary.")
            if ticket_id_company_mapping:
                logger.info(f"Current Stats raw data contains -> {ticket_id_company_mapping}.")
                logger.info(f"Stats generator for {shift_data['theatre']} theatre - STARTED.")
                # Sends the raw data to create the formatted stats string.
                msg_to_send = _createStatsMsg(ticket_id_company_mapping, shift_data)
                if msg_to_send:
                    logger.info(f"Yes! got stats message -> {msg_to_send}, now posting it.")
                    try:
                        # Set the Webex API request payload
                        data = {
                            "text": msg_to_send,
                            "markdown": msg_to_send
                        }
                        sendMessageToWxT(data)
                        logger.info(f"Stats generator for {shift_data['theatre']} theatre - COMPLETED.")
                    except Exception as e:
                        logger.info(f"Posting {shift_data['theatre']} to WxT space failed with error -> {e}.")
            # writes the stats as soon as the shift ended message is sent.
            DoStats().writeTicketsToStats_list(ticket_id_company_mapping, shift_data['theatre'])
            # reset counters after shift is ended.
            reset_processed_tickets()
            reset_tickets_handled_today()
            reset_sets_of_tickets_no_time_check()
        return None


def postDailyShiftTicketSummary(ticket_id_company_mapping, shift_data) -> None:

    """
    Posts daily ticket summary to WxT at the specified times.
    :param ticket_id_company_mapping -> ticket_id and company mapping.
    :param shift_data
    :return: None
    """
    # Only start preparing summary when shift status received is = ended.
    if shift_data:
        if shift_data['status'] == "ended 🏁":
            logger.info(f"Got shift data {shift_data} and theatre is {shift_data['theatre']}, attempting to produce the summary.")
            if ticket_id_company_mapping:
                logger.info(f"Current Stats raw data contains -> {ticket_id_company_mapping}.")
                logger.info(f"Stats generator for {shift_data['theatre']} theatre - STARTED.")
                # Sends the raw data to create the formatted stats string.
                msg_to_send = _createStatsMsg_v2(ticket_id_company_mapping, shift_data)
                if msg_to_send:
                    logger.info(f"Yes! got stats message -> {msg_to_send}, now posting it.")
                    try:
                        # Set the Webex API request payload
                        data = {
                            "text": msg_to_send,
                            "markdown": msg_to_send
                        }
                        sendMessageToWxT(data)
                        logger.info(f"Stats generator for {shift_data['theatre']} theatre - COMPLETED.")
                    except Exception as e:
                        logger.info(f"Posting {shift_data['theatre']} to WxT space failed with error -> {e}.")
            # writes the stats as soon as the shift ended message is sent.
            DoStats().writeTicketsToStats_list(ticket_id_company_mapping, shift_data['theatre'])
            # reset counters after shift is ended.
            reset_processed_tickets()
            reset_tickets_handled_today()
            reset_sets_of_tickets_no_time_check()
            # Clean up
            cleanJsonFiles(None)
        return None


if __name__ == "__main__":  # Local testing.
    # tickets_cust_handled_today = [{'ticket_id': 1615151, 'customer_name': 'SAP'}, {'ticket_id': 1615305, 'customer_name': 'PepsiCo'}, {'ticket_id': 1615312, 'customer_name': 'Cae'}, {'ticket_id': 1615313, 'customer_name': 'Rent-A-Center'}, {'ticket_id': 1615442, 'customer_name': 'PepsiCo'}, {'ticket_id': 1615458, 'customer_name': 'Sutter Health'}, {'ticket_id': 1615469, 'customer_name': 'PepsiCo'}, {'ticket_id': 1615516, 'customer_name': 'NBN COMPANY LTD'}]
    # tickets_cust_handled_today = [{'ticket_id': 1616869, 'customer_name': 'Koninklijke Philips'}, {'ticket_id': 1617148, 'customer_name': 'PepsiCo'}, {'ticket_id': 1617222, 'customer_name': 'PepsiCo'}, {'ticket_id': 1617262, 'customer_name': 'PepsiCo'}, {'ticket_id': 1617280, 'customer_name': 'Ineos NV'}]
    # tickets_cust_handled_today = [{'ticket_id': 1617354, 'customer_name': 'Toshiba Corporation'}, {'ticket_id': 1616869, 'customer_name': 'Koninklijke Philips'}]
    tickets_cust_handled_today = [
        {'ticket_id': 1617354, 'customer_name': 'Toshiba Corporation'},
        {'ticket_id': 1777354, 'customer_name': 'Toshiba Corporation'},
        {'ticket_id': 1888354, 'customer_name': 'Toshiba Corporation'},
        {'ticket_id': 1616869, 'customer_name': 'Koninklijke Philips'},
        {'ticket_id': 1996869, 'customer_name': 'DEUTSCHE BANK AG'},
        {'ticket_id': 2222231, 'customer_name': 'DEUTSCHE BANK AG'}
    ]
    # tickets_cust_handled_today = [
    #     {'ticket_id': 1617354, 'customer_name': 'Toshiba Corporation'}
    # ]
    # test_data = [{'ticket_id': 1619584, 'customer_name': 'THE CLEVELAND CLINIC FOUNDATION'}, {'ticket_id': 1619603, 'customer_name': 'AMERICAN LEBANESE SYRIAN ASSOCIATED CHARITIES'}]
    shift_data = {'theatre': 'CYBERTRON', 'shift_time': '17:15 CEST', 'status': 'ended 🏁'}
    postDailyShiftTicketSummary(tickets_cust_handled_today, shift_data)
