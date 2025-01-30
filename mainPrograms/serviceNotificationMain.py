import time
from cloudSecServiceStatus.cloudSecStatusMsgHandler import createMsg
from cloudSecServiceStatus.fetchStatus import fetchServicesStatusData
import logging


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def runServiceNotificationMain():
    """
    Runs the main Umbrella Service Status notification service.
    """
    while True:
        logger = logging.getLogger('runServiceNotificationMain: ')
        logger.info('Running runServiceNotificationMain')
        list_of_usableData = fetchServicesStatusData()
        if list_of_usableData:
            createMsg(list_of_usableData)
        else:
            logger.info("No new incidents detected, pausing for 30 seconds.")
        time.sleep(30)


if __name__ == "__main__":
    runServiceNotificationMain()
