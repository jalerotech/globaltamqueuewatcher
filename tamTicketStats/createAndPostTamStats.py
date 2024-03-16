from tamTicketStats.readFromTamStats import read_tam_stats_file
from tQwAlerter.shiftTimeDataClass import ShifttimeData as sd
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Running TAM stats script")


def createStatsMsg() -> dict:
    logger.info("Creating TAM stats message - STARTED")
    """
    Creates statistics per TAM and postes the message to WxT.
    """
    shift_data = sd().theatre_shift_time()
    if shift_data:
        # logger.info(f'Waiting for 20 seconds before continuing')
        if shift_data['status'] == "ended 🏁":
            raw_stats = read_tam_stats_file()
            stat_msg = ''
            for email in raw_stats:
                _return_ticket_list(raw_stats[email])
                stat_msg += f" <@personEmail:{email}>: {_return_ticket_list(raw_stats[email])} \n"
            msg_to_send = f"### **📊 Stats Per TAM from {shift_data['theatre']} shift**: \n " \
                          f"{stat_msg}"
            data = {
                "text": msg_to_send,
                "markdown": msg_to_send
            }
            logger.info("Creating TAM stats message - COMPLETED")
            return data


def _return_ticket_list(ticket_data):
    if len(ticket_data) == 1:
        ticket_with_url = f"[{ticket_data[0]}]({tqw().zend_agent_tickets_url}{ticket_data[0]})"
        return ticket_with_url
    else:
        joined_ticket_list = ', '.join(f"[{item}]({tqw().zend_agent_tickets_url}{item})"for item in ticket_data)
        return joined_ticket_list


if __name__ == '__main__':
    createStatsMsg()
#
# logger.info(f"Generating {shift_data['theatre']}  statistics message. - STARTED")
# for item in tickets_cust_handled_today:
#     for i in range(1, (len(tickets_cust_handled_today))):
#         if item['ticket_id'] not in ticket_added_to_stats:
#             counter += i
#             stats_str += f"{counter}. **Ticket #**: {item['ticket_id']}, **Company Name**: {item['customer_name']} \n"
#             ticket_added_to_stats.append(item['ticket_id'])
# msg_to_send = f"### **Statistics from {shift_data['theatre']}  shift of today:** \n " \
#               f"Total number of tickets: **{len(tickets_cust_handled_today)}** \n " \
#               f"{stats_str}"
# logger.info(f"Generating {shift_data['theatre']} statistics message. - COMPLETED")
# logger.info(f"Produced stats message -> {msg_to_send}")
# return msg_to_send
