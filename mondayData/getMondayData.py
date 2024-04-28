import logging
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher
import requests
from mondayData.returnMappings import ret_tam_cus_mappings
from mondayData.nextPageItems import next_page_results
from bfgData.getBfgUrlFromList import createBfgUrls

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Monday script')

monday_auth_keys = TamQueueWatcher().monday_auth_keys
monday_api_url = TamQueueWatcher().monday_api_url
monday_headers = TamQueueWatcher().monday_headers_api_versioning
bfg_base_url = TamQueueWatcher().bfg_base_url


def ret_tam_to_customer_mappings() -> list:
    """
    Fetches data from Monday.com using GraphQL API V2 (2024 version).
    Produces a list of TAM to Customer mapping from the "TAM Customers" group on Monday.com.
    ;returns: List -> TAM-to-Customer mappings.
    """
    # GraphQL API query for items page with items listed as columns and the values set on the columns - > ColumnValue to produce the txt and value fields of the Column value.
    # board_query = '{boards(ids: 588139441) {items_page {items {id name column_values {column {id title} ... on ColumnValue {text id value} id type value}}}}}'
    board_with_group = '{boards (ids: 588139441) {groups {title items_page (limit: 63) {cursor items {id name column_values {column {id title} ... on ColumnValue {text id} id type}}}}}}'
    logger.info("Fetching data from Monday.com.")
    body_data = {'query': board_with_group}
    # tam_customer_assignments = []
    full_tam_customer_assignments = []
    logger.info("Fetching data from Monday.com and producing list of TAM-to-customer mappings.")
    try:
        r = requests.get(url=monday_api_url, json=body_data, headers=monday_headers)
        if r.status_code == 200:
            # Cursor id is needed to get the bext group of results using the item_next_page graphQL API.
            # group_items is the list of items and corresponding values
            group_items, cursor_id = ret_group_items(r.json()['data']['boards'][0]['groups'])
            # Extend the list with the new list created (meaning ret_tam_cus_mappings(group_items) would give -> batch_0 in this case)
            full_tam_customer_assignments.extend(ret_tam_cus_mappings(group_items))
            # Send the cursor id to the get the next page results -> producing the next batch and further cursor (if still needed).
            batch_2, next_cursor = next_page_results(cursor_id)
            full_tam_customer_assignments.extend(batch_2)
            batch_3, next_cursor1 = next_page_results(next_cursor)
            # Final batch added to the list -> final because the TAM Customers group on the TAM Deployment History board has 165 entries.
            # Since each batch collected due to Monday.com's API specific complexity issue contains 63 entries, the process need to be repeated 3 times.
            full_tam_customer_assignments.extend(batch_3)
            return full_tam_customer_assignments
        #     for item in group_items:
        #         cust_data = {}
        #         company_name = item['name']
        #         for vals in item['column_values']:
        #             # Checks for primary assigned TAM
        #             if vals['column']['id'] == 'person':
        #                 if vals['column']['title'] == 'Primary':
        #                     cust_data = {
        #                         "company_name": company_name,
        #                         "primary_tam": vals['text']
        #                     }
        #
        #                 else:
        #                     cust_data = {
        #                         "company_name": company_name,
        #                         "primary_tam": None
        #                     }
        #             # Add BFG ORG URL to customer data
        #             if vals['column']['id'] == 'text6':
        #                 if vals['column']['title'] == 'BFG Org ID':
        #                     # print(vals['text'])
        #                     if vals['text'] is not None:
        #                         # BFG Org ID is provided by Mdy as a string or values e.g. '123456, 789123.
        #                         # So creating a list from the returned data for further processing.
        #                         bfg_url_list = createBfgUrls(vals['text'].split(", "))
        #                         if len(bfg_url_list) == 1:
        #                             cust_data.update({
        #                                 "bfg_org_id": bfg_url_list[0]
        #                             })
        #                         else:
        #                             cust_data.update({
        #                                 "bfg_org_id": bfg_url_list
        #                             })
        #             # Checks for backup assigned TAM from list of people on the Board.
        #             if vals['column']['id'] == 'people':
        #                 if vals['column']['title'] == 'Backup':
        #                     if vals['text']:
        #                         cust_data.update({
        #                             "backup_tam": vals['text']
        #                         })
        #                     else:
        #                         cust_data.update({
        #                             "backup_tam": None
        #                         })
        #                 else:
        #                     cust_data.update({
        #                         "backup_tam": None
        #                     })
        #             # Checks Customer region to capture data of EMEA and APAC customers:
        #             if vals['column']['id'] == 'dropdown':
        #                 if vals['column']['title'] == 'Region':
        #                     if vals['text']:
        #                         # if vals['text'] == 'EMEA' or vals['text'] == 'APAC':
        #                         cust_data.update({
        #                             "customer_region": vals['text']
        #                         })
        #                     else:
        #                         cust_data.update({
        #                             "customer_region": None
        #                         })
        #         if "customer_region" in cust_data and cust_data not in tam_customer_assignments:
        #             tam_customer_assignments.append(cust_data)
        # logger.info("Fetching data from Monday.com and producing list of TAM-to-customer mappings -> COMPLETED.")
        # logger.info(tam_customer_assignments)
        # print(len(tam_customer_assignments))
        # return tam_customer_assignments
    except ConnectionError as e:
        logger.info(f'While running "ret_tam_to_customer_mappings" the connection failed to Monday.com with error -> {e.args}')


def getOrgNameMonday(tam_cust_assignments_from_Monday, Zendesk_New_ticks_w_orgnames) -> list[dict]:
    """
    Produces a list with the ticket_id, primary and backup TAMs including customer region information.
    :param tam_cust_assignments_from_Monday: list of primary and backup TAMs for each customer -> From Monday.com
    :param Zendesk_New_ticks_w_orgnames: list of tickets with org_names populated -> from Zendesk
    :return: list[dict] -> TAMs_data
    """
    logger.info('Parsing assigned TAM(s) from data received from Monday.com')
    tam_to_cust_w_ticket_id = []
    try:
        for ticket in Zendesk_New_ticks_w_orgnames:
            org_name = ''
            # Updating ticket information since COVEA GROUP is not on Zendesk since only SFR opens tickets with Umbrella support for Covea.
            if ticket['org_name'] is not None:
                if ticket['org_name'] == 'Sfr':
                    ticket['org_name'] = "COVEA GROUP"
                    covea_data = ret_covea_data(ticket['ticket_id'])
                    if covea_data not in tam_to_cust_w_ticket_id:
                        tam_to_cust_w_ticket_id.append(covea_data)
                else:
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
        logger.info(f'Error occurred while parsing data from Monday.com with {e.args}')
    logger.info(f'Parsing assigned TAM(s) from data received from Monday.com -> COMPLETED.')
    return tam_to_cust_w_ticket_id


def ret_group_items(mndy_groups):
    logger.info('Returning data from  "TAM Customers" group from the TAM Deployment Monday Board. -> STARTED')
    for group in mndy_groups:
        if group['title'] == 'TAM Customers':
            logger.info('Returning data from "TAM Customers" group from the TAM Deployment Monday Board. -> COMPLETED')
            cursor_id = group['items_page']['cursor']
            return group['items_page']['items'], cursor_id


def ret_covea_data(ticket_id):
    tam_info = {
        "ticket_id": ticket_id,
        "primary_tam": "Joshua Alero",
        "backup_tam": "Anthony Attwood",
        "customer_region": "EMEA",
        "bfg_org_id": createBfgUrls([7948441])[0]
    }
    return tam_info


if __name__ == '__main__':
    ret_tam_to_customer_mappings()
