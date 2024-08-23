import logging
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher
import requests
from mondayData.returnMappings import ret_tam_cus_mappings
from mondayData.nextPageItems import next_page_results
from mondayData.tamCustMappingWriter import tTcmWriter

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Monday script')

monday_auth_keys = TamQueueWatcher().monday_auth_keys
monday_api_url = TamQueueWatcher().monday_api_url
monday_headers = TamQueueWatcher().monday_headers_api_versioning
bfg_base_url = TamQueueWatcher().bfg_base_url


def ret_tam_to_customer_mappings() -> None:
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
            print(f"full_tam_customer_assignments -> {full_tam_customer_assignments}")
            return tTcmWriter(full_tam_customer_assignments)
    except ConnectionError as e:
        logger.info(f'While running "ret_tam_to_customer_mappings" the connection failed to Monday.com with error -> {e.args}')


def ret_group_items(mndy_groups):
    logger.info('Returning data from  "TAM Customers" group from the TAM Deployment Monday Board. -> STARTED')
    for group in mndy_groups:
        if group['title'] == 'TAM Customers':
            logger.info('Returning data from "TAM Customers" group from the TAM Deployment Monday Board. -> COMPLETED')
            cursor_id = group['items_page']['cursor']
            return group['items_page']['items'], cursor_id
