from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tQw
bfgBaseUrl = tQw().bfg_base_url
import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('BGF org links generator')


def createBfgUrls(list_bfg_org_id):
    """
    Creates the BFG Hyperlinks with the BFG ORG ID received from Monday.com.
    And produces a list of the URL(s), if it's a single org company, a single URL is produced (in the form of a list).
    The functions consuming this would then index the needed value e.g. ['12345'] becomes 12345 when consumed by other functions.
    If the company is a multi-org, a list of BFG URLs for each org id is produced also in form of a list.
    But if the list is longer than one item, it's cleaned up to make it a single string with all the URLs.
    :param list_bfg_org_id:
    :return: bfg_url_list - > List of URLs wrapped with in the Org ID.
    """
    bfg_url_list = []
    if list_bfg_org_id:
        try:
            list_of_bfg_org_ids = (list_bfg_org_id[0].split(', '))
            logger.info("List of org_id is greater than 1")
            for org_id in list_of_bfg_org_ids:
                fullUrl = f"{bfgBaseUrl}{org_id}"
                if org_id:
                    bfg_url = f"[ORG_ID:{org_id}]({fullUrl})"
                    bfg_url_list.append(bfg_url)
                else:
                    bfg_url = None
                    bfg_url_list.append(bfg_url)
        except AttributeError as e:
            logger.info(f"Not a splittable value/data {list_bfg_org_id}")
            fullUrl = f"{bfgBaseUrl}{list_bfg_org_id[0]}"
            if list_bfg_org_id[0]:
                bfg_url = f"[ORG_ID:{list_bfg_org_id[0]}]({fullUrl})"
                bfg_url_list.append(bfg_url)
            else:
                bfg_url = None
                bfg_url_list.append(bfg_url)
    if bfg_url_list:
        return bfg_url_list
    else:
        return None

