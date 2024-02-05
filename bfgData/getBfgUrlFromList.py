from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tQw
bfgBaseUrl = tQw().bfg_base_url


def createBfgUrls(list_bfg_org_id) -> list:
    """
    Creates the BFG Hyper links with the BFG ORG ID received from Monday.com.
    And produces a list of the URL(s), if it's a single org company, a single URL is produced (in the form of a list).
    The functions consuming this would then index the needed value e.g. ['12345'] becomes 12345 when consumed by other functions.
    If the company is a multi-org, a list of BFG URLs for each org id is produced also in form of a list.
    But if the list is longer than one item, it's cleaned up to make it a single string with all the URLs.
    :param list_bfg_org_id:
    :return: bfg_url_list - > List of URLs wrapped with in the Org ID.
    """
    bfg_url_list = []
    for org_id in list_bfg_org_id:
        fullUrl = f"{bfgBaseUrl}{org_id}"
        bfg_url = f"[ORG_ID:{org_id}]({fullUrl})"
        bfg_url_list.append(bfg_url)
    if len(bfg_url_list) > 1:
        bfg_url_list = ', '.join(bfg_url_list)
    return bfg_url_list

