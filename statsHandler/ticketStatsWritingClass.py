import logging
import json
from datetime import datetime


class TicketStats:
    """
    Statistics generator.
    """

    def __init__(self):
        """
        Writes ticket data (id and customer name) to stats.json file at the end of each theatre shift.
        Creates message string (msg_to_send) that's sent to WxT.
        """

        self.logger = logging.getLogger('TicketStats')
        self.currentDateAndTime = datetime.now()

    def readAndConvertToList(self) -> list:
        """
        Opens the file named "stats.json" and turns it into a list and returns a list
        And if the json file is empty it returns a None
        :param : List of tickets [{Keys => ticket_id, customer_name}]
        :return: list
        """
        self.logger.info('Reading stats.json file and checking if empty or contains data. - STARTED')
        with open('Files/stats.json', 'r') as f:
            try:
                json_file = json.loads(f.read())
                self.logger.info('Stats.json not empty returning existing list.')
            except json.decoder.JSONDecodeError:
                self.logger.info('Stats.json is empty returning existing empty list.')
                json_file = []
        f.close()
        self.logger.info('Reading stats.json file and checking if empty or contains data. - COMPLETED')
        return json_file

    def writeTicketsToStats_list(self, ticket_id_company_mapping, theatre) -> None:
        """
        Opens the file named "stats.json" and writes the data collected and processed from Zendesk and Monday.

        :return: None

        """
        # All stats:
        date_today = datetime.today().strftime('%Y-%m-%d')
        stat_list = self.readAndConvertToList()
        if not any(date_today == stat["date"] and stat['theatre'] == theatre for stat in stat_list):
            stat_list.append(
                {
                    'theatre': theatre,
                    'date': date_today,
                    'data': ticket_id_company_mapping
                })
            self.logger.info(f"Stats for {theatre} being written to stats.json file -> {ticket_id_company_mapping}")
            self.logger.info(f'Writing {theatre} ticket data to file for statistics. - STARTED')
            with open('Files/stats.json', 'w') as f:
                json.dump(stat_list, f, indent=4)
            f.close()
            self.logger.info(f'Writing {theatre} ticket data to file for statistics. - COMPLETED')
            return None

        # # EMEA Stats
        # if datetime.now().hour == 16 and (0 <= datetime.now().minute < 3):
        #     date_today = datetime.today().strftime('%Y-%m-%d')
        #     stat_list = self.readAndConvertToList()
        #     if not any(date_today == stat["date"] for stat in stat_list):
        #         stat_list.append(
        #             {
        #                 'theatre': "EMEA",
        #                 'date': date_today,
        #                 'data': ticket_id_company_mapping
        #             })
        #         self.logger.info(f"Stats being written to stats.json file -> {ticket_id_company_mapping}")
        #         self.logger.info('Writing ticket data to file for statistics. - STARTED')
        #         with open('stats.json', 'w') as f:
        #             json.dump(stat_list, f, indent=4)
        #         f.close()
        #         self.logger.info('Writing ticket data to file for statistics. - COMPLETED')
        #         return None
        #
        # # APAC Stats
        # if datetime.now().hour == 9 and (0 <= datetime.now().minute < 3):
        #     date_today = datetime.today().strftime('%Y-%m-%d')
        #     stat_list = self.readAndConvertToList()
        #     if not any(date_today == stat["date"] for stat in stat_list):
        #         stat_list.append(
        #             {
        #                 'theatre': "APAC",
        #                 'date': date_today,
        #                 'data': ticket_id_company_mapping
        #             })
        #         self.logger.info(f"Stats being written to stats.json file -> {ticket_id_company_mapping}")
        #         self.logger.info('Writing ticket data to file for statistics. - STARTED')
        #         with open('stats.json', 'w') as f:
        #             json.dump(stat_list, f, indent=4)
        #         f.close()
        #         self.logger.info('Writing ticket data to file for statistics. - COMPLETED')
        #         return None
        #
        # # US stats
        # if datetime.now().hour == 2 and (0 <= datetime.now().minute < 3):
        #     date_today = datetime.today().strftime('%Y-%m-%d')
        #     stat_list = self.readAndConvertToList()
        #     if not any(date_today == stat["date"] for stat in stat_list):
        #         stat_list.append(
        #             {
        #                 'theatre': "US",
        #                 'date': date_today,
        #                 'data': ticket_id_company_mapping
        #             })
        #         self.logger.info(f"Stats being written to stats.json file -> {ticket_id_company_mapping}")
        #         self.logger.info('Writing ticket data to file for statistics. - STARTED')
        #         with open('stats.json', 'w') as f:
        #             json.dump(stat_list, f, indent=4)
        #         f.close()
        #         self.logger.info('Writing ticket data to file for statistics. - COMPLETED')
        #         return None

    # def writeTicketsToStats(self, tickets_handled_today) -> None:
    #     """
    #     Opens the file named "stats.json" and writes the data collected and processed from Zendesk and Monday.
    #     :param tickets_handled_today: List of tickets [{Keys => ticket_id, customer_name}]
    #     :return: None
    #     """
    #     self.logger.info('Writing ticket data to file for statistics. - STARTED')
    #     with open('stats.json', 'w') as f:
    #         json.dump(tickets_handled_today, f, indent=4)
    #     f.close()
    #     self.logger.info('Writing ticket data to file for statistics. - COMPLETED')
    #     return None

    # def readTicketsFromStats(self) -> list:
    #     """
    #     Opens the stats.json file and reads from it.
    #     :return: ticket_handled_data (original data writen to stats.json file by writeTicketsToStats function.)
    #     """
    #     self.logger.info('Reading ticket data from statistics file (stats.json). - STARTED')
    #
    #     try:
    #         with open('stats.json', 'r') as f:
    #             ticket_handled_data = json.load(f)
    #         f.close()
    #         self.logger.info('Reading ticket data from statistics file (stats.json). - COMPLETED')
    #         self.logger.info(f'Current stats.json file content -> {ticket_handled_data}.')
    #     except Exception as e:
    #         self.logger.info(f"Stats.json file is empty so error is seen as '{e.args}'")
    #     return ticket_handled_data

    # def statsMsg(self) -> str:
    #     """
    #     Creates the statistics message after looping through data read from the stats.json file by function readTicketsFromStats
    #     :return: msg_to_send (str)
    #     """
    #     self.logger.info("Generating statistics message...")
    #     tickets_handled_today = TicketStats().readTicketsFromStats()
    #     stats_str = ''
    #     counter = 0
    #     ticket_added_to_stats = []
    #     if len(tickets_handled_today) == 1:
    #         item = tickets_handled_today[0]
    #         stats_str = f"1. **Ticket #**: {item['ticket_id']}, **Company Name**: {item['customer_name']} \n"
    #         ticket_added_to_stats.append(item['ticket_id'])
    #         msg_to_send = f"### **Statistics from EMEA shift of today** \n " \
    #                       f"Total number of tickets: **{len(tickets_handled_today)}** \n " \
    #                       f"{stats_str}"
    #     else:
    #         for item in tickets_handled_today:
    #             for i in range(1, (len(tickets_handled_today))):
    #                 if item['ticket_id'] not in ticket_added_to_stats:
    #                     counter += i
    #                     stats_str += f"{counter}. **Ticket #**: {item['ticket_id']}, **Company Name**: {item['customer_name']} \n"
    #                     ticket_added_to_stats.append(item['ticket_id'])
    #         msg_to_send = f"### **Statistics from EMEA shift of today** \n " \
    #                       f"Total number of tickets: **{len(tickets_handled_today)}** \n " \
    #                       f"{stats_str}"
    #         self.logger.info("Generating statistics message... -> COMPLETED")
    #     return msg_to_send

    # def statsAutoCleanup(self) -> None:
    #     """
    #     Opens the stats.json file as soon as statistics have been posted to WxT.
    #     And as it's opened in write mode "w" and closed immediately, "NOTHING" is written, thus rendering the file empty
    #     :return: None
    #     """
    #     self.logger.info('Cleaning up stats.json file...')
    #     stats_file_to_clean = open("stats.json", 'w')
    #     stats_file_to_clean.close()
    #     self.logger.info('Cleaning up stats.json file... -> COMPLETED')
    #
    #     return None
