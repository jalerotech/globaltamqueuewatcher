import logging
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher
# from TamPtoTracker.ptoAvailabilityWatcher import returnTAMStatus
import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from bfgData.getBfgUrlFromList import createBfgUrls

env_path = Path('../statsHandler') / 'authkey.env'
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    pass

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class MondayDotCom:

    def __init__(self):
        """
        Monday's data collection and parsing class.
        """
        self.logger = logging.getLogger('MondayDotCom')
        self.monday_auth_keys = TamQueueWatcher().monday_auth_keys
        self.monday_api_url = TamQueueWatcher().monday_api_url
        self.monday_headers = TamQueueWatcher().monday_headers
        self.bfg_base_url = TamQueueWatcher().bfg_base_url

    def getDatafromdy(self) -> list:

        """
        Fetches data from TAM Deployment History and creates a mapping of the list of TAM assigned customers
        This uses the GraphQL API of Monday.com to pull the data from the appropriate board.
        :return: tam_customer_assignments [list]
        """
        query_workspace_4 = '{boards (ids: 588139441) {items () {id name column_values {id title value text }}}}'
        self.logger.info("Fetching data from Monday.com.")

        body_data = {'query': query_workspace_4}
        tam_customer_assignments = []
        self.logger.info("Fetching data from Monday.com and producing list of TAM-to-customer mappings.")
        r = requests.get(url=self.monday_api_url, json=body_data, headers=self.monday_headers)

        for board in r.json()['data']['boards']:
            cust_data = {}
            # print(board)
            for item in board['items']:
                company_name = item['name']
                for vals in item['column_values']:
                    # Checks for primary assigned TAM
                    if vals['id'] == 'person':
                        if vals['title'] == 'Primary':
                            cust_data = {
                                "company_name": company_name,
                                "primary_tam": vals['text']
                            }
                        else:
                            cust_data = {
                                "company_name": company_name,
                                "primary_tam": None
                            }
                    # Add BFG ORG URL to customer data
                    if vals['id'] == 'text6':
                        if vals['title'] == 'BFG Org ID':
                            if vals['value'] is not None:
                                # BFG Org ID is provided by Mdy as a string or values e.g. '123456, 789123.
                                # So creating a list from the returned data for further processing.
                                bfg_url_list = createBfgUrls(vals['text'].split(", "))
                                if len(bfg_url_list) == 1:
                                    cust_data.update({
                                        "bfg_org_id": bfg_url_list[0]
                                    })
                                else:
                                    cust_data.update({
                                        "bfg_org_id": bfg_url_list
                                    })
                    # Checks for backup assigned TAM from list of people on the Board.
                    if vals['id'] == 'people':
                        if vals['title'] == 'Backup':
                            if vals['text']:
                                cust_data.update({
                                    "backup_tam": vals['text']
                                })
                            else:
                                cust_data.update({
                                    "backup_tam": None
                                })
                        else:
                            cust_data.update({
                                "backup_tam": None
                            })
                    # Checks Customer region to capture data of EMEA and APAC customers:
                    if vals['id'] == 'dropdown':
                        if vals['title'] == 'Region':
                            if vals['text']:
                                # if vals['text'] == 'EMEA' or vals['text'] == 'APAC':
                                cust_data.update({
                                    "customer_region": vals['text']
                                })
                            else:
                                cust_data.update({
                                    "customer_region": None
                                })
                if "customer_region" in cust_data and cust_data not in tam_customer_assignments:
                    tam_customer_assignments.append(cust_data)
        self.logger.info("Fetching data from Monday.com and producing list of TAM-to-customer mappings -> COMPLETED.")
        self.logger.info(tam_customer_assignments)
        return tam_customer_assignments

    def getOrgNameMonday(self, tam_cust_assignments_from_Monday, Zendesk_New_ticks_w_orgnames) -> list[dict]:
        # Call function to return list of tams on PTO here.
        # tam_in_ooo_list = ptoWatcherMain('local')
        """
        Produces a list with the ticket_id, primary and backup TAMs including customer region information.
        :param tam_cust_assignments_from_Monday: list of primary and backup TAMs for each customer -> From Monday.com
        :param Zendesk_New_ticks_w_orgnames: list of tickets with org_names populated -> from Zendesk
        :return: list[dict] -> TAMs_data
        """
        self.logger.info('Parsing assigned TAM(s) from data received from Monday.com')

        tam_to_cust_w_ticket_id = []
        try:
            for ticket in Zendesk_New_ticks_w_orgnames:
                org_name = ''
                if ticket['org_name'] is not None:
                    org_name = ticket['org_name'].lower()
                tam_info = {
                    "ticket_id": ticket['ticket_id'],
                    "primary_tam": None,
                    "backup_tam": None,
                    "customer_region": None,
                    "bfg_org_id": None
                }

                for assignment in tam_cust_assignments_from_Monday:
                    company_name = assignment['company_name'].lower()
                    if org_name == company_name and assignment['bfg_org_id']:
                        tam_info['primary_tam'] = assignment['primary_tam']
                        tam_info['backup_tam'] = assignment['backup_tam']
                        tam_info['customer_region'] = assignment['customer_region']
                        tam_info['bfg_org_id'] = assignment['bfg_org_id']
                    if org_name == company_name and (not assignment['bfg_org_id']):
                        tam_info['primary_tam'] = assignment['primary_tam']
                        tam_info['backup_tam'] = assignment['backup_tam']
                        tam_info['customer_region'] = assignment['customer_region']
                        break
                tam_to_cust_w_ticket_id.append(tam_info)
        except AttributeError as e:
            self.logger.info(f'Error occurred while parsing data from Monday.com with {e.args}')
        self.logger.info(f'Parsing assigned TAM(s) from data received from Monday.com -> COMPLETED.')
        return tam_to_cust_w_ticket_id


if __name__ == "__main__":
    pass
