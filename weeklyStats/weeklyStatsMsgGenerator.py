import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Running Weekly Stats Message generator")


def createWeeklyStatsMsg(raw_list) -> dict:
    logger.info("Generating Weekly Stats Message")
    """
    Generates the weekly stats message..
    """
    if raw_list:
        logger.info(f"Raw Data received to generate weekly Stats message -> {raw_list}.")
        stat_msg = ''
        uldll = _retUsableData(raw_list)
        for company in uldll:
            # stat_msg += f" - **{company}**, **_N° ticket(s)_**: {uldll[company]} \n "
            stat_msg += f" - **{company}**: {uldll[company]} \n "
        msg_to_send = f"### **📊 Weekly Summary of Tickets Per Customer Globally:** \n " \
                      f"{stat_msg}"
        data = {
            "text": msg_to_send,
            "markdown": msg_to_send
        }
        logger.info("Weekly Stats Message Created.")
        return data
    else:
        logger.info(f"No stats data received from the read_tam_stats_file function.")


def _retUsableData(raw_list):
    """
    Produces a json output of the total number of tickets per customer using the raw list as input.
    """
    usable_list_dict = {}
    usable_list_dict_list_length = {}
    for item in raw_list:
        ticket = item['ticket_id']
        if item['customer_name'] in usable_list_dict:
            usable_list_dict[item['customer_name']].append(ticket)
        else:
            usable_list_dict.update({item['customer_name']: [item['ticket_id']]})
    for customer_name in usable_list_dict:
        usable_list_dict_list_length.update({customer_name: len(usable_list_dict[customer_name])})
    return usable_list_dict_list_length


if __name__ == '__main__':
    info = [{
        "ticket_id": 1800808,
        "customer_name": "Iron Mountain"
    },
        {
            "ticket_id": 1801114,
            "customer_name": "PepsiCo"
        },
        {
            "ticket_id": 1801123,
            "customer_name": "SANTANDER"
        },
        {
            "ticket_id": 1801182,
            "customer_name": "Koninklijke Philips"
        },
        {
            "ticket_id": 1801253,
            "customer_name": "HCA Inc."
        },
        {
            "ticket_id": 1801283,
            "customer_name": "HONEYWELL INTERNATIONAL INC"
        },
        {
            "ticket_id": 1802229,
            "customer_name": "INFRABEL SA"
        },
        {
            "ticket_id": 1802235,
            "customer_name": "HITACHI"
        },
        {
            "ticket_id": 1802241,
            "customer_name": "Signode"
        },
        {
            "ticket_id": 1802374,
            "customer_name": "INFRABEL SA"
        },
        {
            "ticket_id": 1802401,
            "customer_name": "GLIC"
        },
        {
            "ticket_id": 1802464,
            "customer_name": "GLIC"
        }]
    _retUsableData(info)
