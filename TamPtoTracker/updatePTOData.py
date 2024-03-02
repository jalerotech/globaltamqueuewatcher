import logging
from TamPtoTracker.readfromPTOTrackerFile import read_json_file_line_by_line

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Updating {tam_to_cust_w_ticket_id list}")


def update_tam_to_cust_w_ticket_id(tam_to_cust_w_ticket_id) -> list:
    """
    Produces an updated list of "tam_to_cust_w_ticket_id" after checking which TAM is on PTO.
    :param tam_to_cust_w_ticket_id:
    :return:List -> updated_tam_to_cust_w_ticket_id
    """
    logger.info("Updating tam_to_cust_w_ticket_id list with TAM PTO status where needed - STARTED")
    pto_data = read_json_file_line_by_line()
    updated_tam_to_cust_w_ticket_id = []
    for mapping in tam_to_cust_w_ticket_id:
        if pto_data:
            for data in pto_data[0]:
                # print(data)
                if mapping['primary_tam']:
                    if mapping['primary_tam'] == data['name']:
                        mapping['primary_tam'] = f"{mapping['primary_tam']} 🛫"
                        updated_tam_to_cust_w_ticket_id.append(mapping)
                    else:
                        updated_tam_to_cust_w_ticket_id.append(mapping)
        else:
            logger.info("No PTO data yet")
    logger.info("Updating tam_to_cust_w_ticket_id list with TAM PTO status where needed - COMPLETED")
    return updated_tam_to_cust_w_ticket_id


if __name__ == '__main__':
    data_list = [{'ticket_id': 1766438, 'primary_tam': 'Konrad Porzezynski', 'backup_tam': 'Andres Mijael Paredez Marhemberg, Walter Gardeazabal', 'customer_region': 'EMEA', 'bfg_org_id': '[ORG_ID:2578504](https://bfg.umbrella.com/organizations/organization/2578504)'}, {'ticket_id': 1759570, 'primary_tam': None, 'backup_tam': None, 'customer_region': None, 'bfg_org_id': None}, {'ticket_id': 1770263, 'primary_tam': 'Kevin Hudson', 'backup_tam': None, 'customer_region': 'AMER', 'bfg_org_id': '[ORG_ID:5404265](https://bfg.umbrella.com/organizations/organization/5404265)'}, {'ticket_id': 1765954, 'primary_tam': None, 'backup_tam': None, 'customer_region': None, 'bfg_org_id': None}, {'ticket_id': 1770240, 'primary_tam': None, 'backup_tam': None, 'customer_region': None, 'bfg_org_id': None}, {'ticket_id': 1769595, 'primary_tam': 'Kevin Hudson', 'backup_tam': None, 'customer_region': 'AMER', 'bfg_org_id': '[ORG_ID:5404265](https://bfg.umbrella.com/organizations/organization/5404265)'}, {'ticket_id': 1765009, 'primary_tam': 'Andres Mijael Paredez Marhemberg', 'backup_tam': None, 'customer_region': 'EMEA', 'bfg_org_id': '[ORG_ID:8064755](https://bfg.umbrella.com/organizations/organization/8064755)'}, {'ticket_id': 1601995, 'primary_tam': 'Anthony Attwood', 'backup_tam': None, 'customer_region': 'EMEA', 'bfg_org_id': '[ORG_ID:2505472](https://bfg.umbrella.com/organizations/organization/2505472)'}, {'ticket_id': 1769574, 'primary_tam': 'Walter Gardeazabal', 'backup_tam': 'Brett Parnell', 'customer_region': 'AMER', 'bfg_org_id': '[ORG_ID:5383162](https://bfg.umbrella.com/organizations/organization/5383162)'}, {'ticket_id': 1765913, 'primary_tam': 'Konrad Porzezynski', 'backup_tam': 'Andres Mijael Paredez Marhemberg, Walter Gardeazabal', 'customer_region': 'EMEA', 'bfg_org_id': '[ORG_ID:2578504](https://bfg.umbrella.com/organizations/organization/2578504)'}, {'ticket_id': 1760367, 'primary_tam': 'Kevin Hudson', 'backup_tam': None, 'customer_region': 'AMER', 'bfg_org_id': '[ORG_ID:5404265](https://bfg.umbrella.com/organizations/organization/5404265)'}, {'ticket_id': 1753216, 'primary_tam': 'Handy Putra', 'backup_tam': None, 'customer_region': 'APAC', 'bfg_org_id': '[ORG_ID:3000216](https://bfg.umbrella.com/organizations/organization/3000216)'}, {'ticket_id': 1767159, 'primary_tam': 'Diego Barrantes Rivera', 'backup_tam': 'Arjun Raina', 'customer_region': 'AMER', 'bfg_org_id': '[ORG_ID:5404909](https://bfg.umbrella.com/organizations/organization/5404909)'}]
    update_tam_to_cust_w_ticket_id(data_list)
    # print(tam_to_cust_w_ticket_id)
