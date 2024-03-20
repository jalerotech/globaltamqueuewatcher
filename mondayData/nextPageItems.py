import requests
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tQw
import logging
from mondayData.returnMappings import ret_tam_cus_mappings

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Returning Mappings from the next page (batches of 63 items)")

monday_auth_keys = tQw().monday_auth_keys
monday_api_url = tQw().monday_api_url
monday_headers = tQw().monday_headers_api_versioning
bfg_base_url = tQw().bfg_base_url


def next_page_results(cursor_id):
    """
    Produces the next group_items and passes that onto "ret_tam_cus_mappings" function to produce the actual
    TAM-to-Customer mappings and the next cursor id (for next "next_page" call).
    """
    query = '''
    query ($cursor: String!) {
      next_items_page(limit: 63, cursor: $cursor) {
        cursor
        items {
          id
          name
          column_values {
          column {id title} ... on ColumnValue {text id} id type}
        }
      }
    }
    '''
    variables = {
        "cursor": cursor_id
    }
    request = requests.post(monday_api_url, json={'query': query, 'variables': variables}, headers=monday_headers)
    if request.status_code == 200:
        new_mapping = ret_tam_cus_mappings(request.json()['data']['next_items_page']['items'])
        next_cursor = request.json()['data']['next_items_page']['cursor']
        return new_mapping, next_cursor
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


