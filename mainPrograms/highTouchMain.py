import logging
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tQw
import time
from zendeskData.fetchProcessZendeskData import getAllTickets, getOrgName
from highTouchCustomerTickets.filterTickets import retHighTouchTickets
from highTouchCustomerTickets.updateTicketData import updateTicketData
from highTouchCustomerTickets.highTouchMsgHandler import createMsg

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def runHighTouchMain():
    """
    Runs the main high touch alerting program.
    """
    while True:
        logger = logging.getLogger('runHighTouchMain: ')
        logger.info('runHighTouchMain Program')

        lont = getAllTickets()
        lont_with_org_name = getOrgName(lont)

        # List of Customer's that should be included in the high-touch notifications:
        high_touch_customers = ["Walmart", "GLIC"]

        if lont_with_org_name:
            # Filter and produce list of ticket from customers considered high-touch
            lonHTt = retHighTouchTickets(lont_with_org_name, high_touch_customers)
            if lonHTt:
                list_of_updated_tickets = updateTicketData(lonHTt)
                createMsg(list_of_updated_tickets)
        else:
            logger.info(f"No new high-touch tickets found, pausing for 30 seconds.")
            # Wait for the specified interval before making the next API call
        time.sleep(tQw().zendesk_polling_interval)


if __name__ == "__main__":
    runHighTouchMain()
