import logging
from datetime import datetime

import requests
from cloudSecServiceStatus.listStringFromDict import stringFromList

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
status_base_url = "https://status.umbrella.com/#/detail/"


def fetchServicesStatusData() -> list:
    """
    Fetches the incidents data available on status.umbrella.com using the api endpoint
    """
    logger = logging.getLogger('fetchStatusData: ')
    logger.info('Fetching status data from "status.umbrella.com"')
    url = "https://api.status.umbrella.com/api/portal/incidents?services=&orgName=Cisco%20Umbrella&regions=&last=29&types=CRITICAL_OUTAGE,PARTIAL_OUTAGE,SERVICE_OUTAGE,SERVICE_DEGRADATION,SERVICE_NOTIFICATION,SERVICE_INVESTIGATING"
    resp = requests.get(url)
    returned_data = resp.json()['content']
    list_of_usableData = []
    for orgData in returned_data:
        if orgData['type'] == "SERVICE_DEGRADATION":
            if orgData['state'] != "RESOLVED":
                timestamp = datetime.strptime(orgData['incidentDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
                formatted_timestamp = timestamp.strftime("%H:%M:%S")
                formatted_date = timestamp.strftime("%Y-%m-%d")
                creation_timestamp = f"{formatted_date}, {formatted_timestamp}"
                usable_data = {
                    'namesOfServices': stringFromList(orgData['services']),
                    'creationDateTime': creation_timestamp,
                    'incidentType': orgData['type'],
                    'incidentState': orgData['state'],
                    'affectedRegions': stringFromList(orgData['regions']),
                    'incidentCode': orgData['incidentCode'],
                    'incidentId': orgData['incidentId'],
                    'incidentUrl': f"{status_base_url}{orgData['incidentId']}"
                }
                list_of_usableData.append(usable_data)
    return list_of_usableData


if __name__ == "__main__":
    fetchServicesStatusData()
