import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Running Weekly Stats Per Region Message generator")


def createWeeklyStatsPerRegionMsg(raw_list) -> dict:
    logger.info("Generating Weekly  Stats Per Region Message")
    """
    Generates the weekly Stats Per Region message..
    """
    if raw_list:
        logger.info(f"Raw Data received to generate weekly Stats Per Region message-> {raw_list}.")
        stat_msg = ''
        uldll, tc = _retUsableData(raw_list)
        for region in uldll:
            stat_msg += f" - ***{region}***: {uldll[region]} \n "
        msg_to_send = f"### **🗃️ Weekly Summary of Tickets Per Region:** \n " \
                      f"{stat_msg}"
        data = {
            "text": msg_to_send,
            "markdown": msg_to_send
        }
        logger.info("Weekly Stats Per Region Message Created.")
        return data
    else:
        logger.info(f"No stats data received from the read_tam_stats_file function.")


def _retUsableData(raw_list):
    """
    Produces a json output of the total number of tickets per customer using the raw list as input.
    """
    usable_list_dict = {}
    ticket_count = []
    usable_list_dict_list_length = {}
    for item in raw_list:
        ticket = item['ticket_id']
        try:
            if item['region'] in usable_list_dict:
                usable_list_dict[item['region']].append(ticket)
            else:
                usable_list_dict.update({item['region']: [item['ticket_id']]})
            if ticket not in ticket_count:
                ticket_count.append(ticket)
        except KeyError as e:
            logger.info(f"Ticket data is missing region in the written entry -> error raised is {e.args}")
    for region in usable_list_dict:
        usable_list_dict_list_length.update({region: len(usable_list_dict[region])})
    return usable_list_dict_list_length, ticket_count


if __name__ == '__main__':
    info = [{"ticket_id": 1802949, "customer_name": "HITACHI", "region": "EMEA"},
            {"ticket_id": 1802952, "customer_name": "BRENNTAG SE", "region": "EMEA"},
            {"ticket_id": 1803002, "customer_name": "Koninklijke Philips", "region": "EMEA"},
            {"ticket_id": 1803014, "customer_name": "ITC Holdings", "region": "APAC"},
            {"ticket_id": 1803036, "customer_name": "BREWIN DOLPHIN", "region": "APAC"},
            {"ticket_id": 1803078, "customer_name": "Nielsen Company LLC (Nielsen Media)", "region": "APAC"},
            {"ticket_id": 1803128, "customer_name": "SAP", "region": "US"},
            {"ticket_id": 1803194, "customer_name": "WageWorks / HealthEquity", "region": "US"},
            {"ticket_id": 1803259, "customer_name": "Prosegur", "region": "EMEA"},
            {"ticket_id": 1803361, "customer_name": "AMERICAN LEBANESE SYRIAN ASSOCIATED CHARITIES", "region": "APAC"},
            {"ticket_id": 1803505, "customer_name": "Toshiba Corporation", "region": "EMEA"},
            {"ticket_id": 1803526, "customer_name": "BRENNTAG SE", "region": "APAC"},
            {"ticket_id": 1803527, "customer_name": "ZIMMER, INC.", "region": "US"},
            {"ticket_id": 1803543, "customer_name": "Prosegur", "region": "US"},
            {"ticket_id": 1803558, "customer_name": "Avolta ( Dufry)", "region": "EMEA"},
            {"ticket_id": 1803607, "customer_name": "Penguin Random House", "region": "APAC"},
            {"ticket_id": 1803686, "customer_name": "SANTANDER", "region": "EMEA"},
            {"ticket_id": 1803789, "customer_name": "GLIC", "region": "US"},
            {"ticket_id": 1803903, "customer_name": "GLIC", "region": "US"},
            {"ticket_id": 1804011, "customer_name": "TMB Bank [SIG]", "region": "EMEA"}
            ]

    _retUsableData(info)
    createWeeklyStatsPerRegionMsg(info)
