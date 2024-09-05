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
        uldll, tc = _retUsableData(raw_list)
        for company in uldll:
            # stat_msg += f" - **{company}**, **_N° ticket(s)_**: {uldll[company]} \n "
            stat_msg += f" - ***{company}***: {uldll[company]} \n "
        msg_to_send = f"### **🗃️ Weekly Summary of Tickets Per Customer Globally:** \n " \
                      f" Total number of tickets: **{len(tc)}** \n " \
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
    ticket_count = []
    usable_list_dict_list_length = {}
    for item in raw_list:
        ticket = item['ticket_id']
        if item['customer_name'] in usable_list_dict:
            usable_list_dict[item['customer_name']].append(ticket)
        else:
            usable_list_dict.update({item['customer_name']: [item['ticket_id']]})
        if ticket not in ticket_count:
            ticket_count.append(ticket)
    for customer_name in usable_list_dict:
        usable_list_dict_list_length.update({customer_name: len(usable_list_dict[customer_name])})
    return usable_list_dict_list_length, ticket_count


if __name__ == '__main__':
    info = [{"ticket_id": 1802949, "customer_name": "HITACHI"},
            {"ticket_id": 1802952, "customer_name": "BRENNTAG SE"},
            {"ticket_id": 1803002, "customer_name": "Koninklijke Philips"},
            {"ticket_id": 1803014, "customer_name": "ITC Holdings"},
            {"ticket_id": 1803036, "customer_name": "BREWIN DOLPHIN"},
            {"ticket_id": 1803078, "customer_name": "Nielsen Company LLC (Nielsen Media)"},
            {"ticket_id": 1803128, "customer_name": "SAP"},
            {"ticket_id": 1803194, "customer_name": "WageWorks / HealthEquity"},
            {"ticket_id": 1803259, "customer_name": "Prosegur"},
            {"ticket_id": 1803361, "customer_name": "AMERICAN LEBANESE SYRIAN ASSOCIATED CHARITIES"},
            {"ticket_id": 1803505, "customer_name": "Toshiba Corporation"},
            {"ticket_id": 1803526, "customer_name": "BRENNTAG SE"},
            {"ticket_id": 1803527, "customer_name": "ZIMMER, INC."},
            {"ticket_id": 1803543, "customer_name": "Prosegur"},
            {"ticket_id": 1803558, "customer_name": "Avolta ( Dufry)"},
            {"ticket_id": 1803607, "customer_name": "Penguin Random House"},
            {"ticket_id": 1803686, "customer_name": "SANTANDER"},
            {"ticket_id": 1803789, "customer_name": "GLIC"},
            {"ticket_id": 1803903, "customer_name": "GLIC"},
            {"ticket_id": 1804011, "customer_name": "TMB Bank [SIG]"},
            {"ticket_id": 1804263, "customer_name": "STARLING BANK C O PROJECT VISION"},
            {"ticket_id": 1804281, "customer_name": "HSE"},
            {"ticket_id": 1804330, "customer_name": "HSE"},
            {"ticket_id": 1804396, "customer_name": "MTN NIGERIA COMMUNICATIONS PLC"},
            {"ticket_id": 1804425, "customer_name": "Nielsen Company LLC (Nielsen Media)"},
            {"ticket_id": 1804429, "customer_name": "GLIC"},
            {"ticket_id": 1804440, "customer_name": "SC DEPT OF ADMIN DIV OF TECHNOLOGY OPERATIONS"},
            {"ticket_id": 1804495, "customer_name": "GLIC"},
            {"ticket_id": 1804536, "customer_name": "Tennessee Valley Authority"},
            {"ticket_id": 1804671, "customer_name": "HSE"},
            {"ticket_id": 1804723, "customer_name": "COOLEY LLP"},
            {"ticket_id": 1804729, "customer_name": "Jetstar"},
            {"ticket_id": 1804730, "customer_name": "Toshiba Corporation"},
            {"ticket_id": 1804733, "customer_name": "TAC-Collab"},
            {"ticket_id": 1804754, "customer_name": "HITACHI"},
            {"ticket_id": 1804774, "customer_name": "Koninklijke Philips"}
            ]

    _retUsableData(info)
