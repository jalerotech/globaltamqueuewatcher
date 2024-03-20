import logging
from bfgData.getBfgUrlFromList import createBfgUrls

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Returning Mappings")


def ret_tam_cus_mappings(group_items) -> list:
    """
    Produces the list of TAM to Customer Mappings with the group_items data provided.
    Searches the tree of data provided to parse out necessary fields.
    ;returns: List[]
    """
    tam_customer_assignments = []
    logger.info('Parsing out, Primary TAM, Backup TAM(s), Customer Region, BFG_org and generating Tam-customer mapping - STARTED')
    for item in group_items:
        cust_data = {}
        company_name = item['name']
        for vals in item['column_values']:
            # Checks for primary assigned TAM
            if vals['column']['id'] == 'person':
                if vals['column']['title'] == 'Primary':
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
            if vals['column']['id'] == 'text6':
                if vals['column']['title'] == 'BFG Org ID':
                    # print(vals['text'])
                    if vals['text'] is not None:
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
            if vals['column']['id'] == 'people':
                if vals['column']['title'] == 'Backup':
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
            if vals['column']['id'] == 'dropdown':
                if vals['column']['title'] == 'Region':
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
    logger.info("Fetching data from Monday.com and producing list of TAM-to-customer mappings -> COMPLETED.")
    logger.info(f"tam_customer_assignments -> {tam_customer_assignments}")
    logger.info('Parsing out, Primary TAM, Backup TAM(s), Customer Region, BFG_org and generating Tam-customer mapping - COMPLETED')
    return tam_customer_assignments


