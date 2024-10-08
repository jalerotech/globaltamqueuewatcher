import logging
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tQw
from mainPrograms.weeklyStatsMain import weeklyStatsMain
import time
from mondayData.getMondayData import ret_tam_to_customer_mappings, getOrgNameMonday
from datetime import datetime
from ticketAndMsgHandlers.handleTicketMessages import postMsgTicketInfo
from zendeskData.fetchProcessZendeskData import getAllTickets, getOrgName
from mondayData.fetchProcessMdyDataClass import MondayDotCom as mdy
from tQwAlerter.alertShiftStartStop import alertshiftstart, weekendAlert
from TamPtoTracker.updatePTOData import update_tam_to_cust_w_ticket_id
from mondayData.mdyTamCustStandalone import mdyTamCustMain
from zendeskData.fetchProcessZendeskData import validateTickets

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

current_time = datetime.now().time()
working_days = ["Tuesday", "Wednesday", "Thursday", "Friday"]


def main():
    """
    Runs the main program

    :return:
    """

    while True:
        logger = logging.getLogger('Running TamQueueWatcher')
        currentDateAndTime = datetime.now()
        today = currentDateAndTime.strftime('%A')
        currentTime = currentDateAndTime.strftime("%H:%M:%S")
        # Not working after 02:00 AM CEST on Saturday.
        # Allow 60 seconds more for the shift alert to be run to alert US shift end - As the last to be posted before global weekend start.
        # Sunday is a full day of not running the scripts.
        # While the script should still run until after 2 am on Saturday.
        if (today == "Saturday" and (currentDateAndTime.hour >= 2 and currentDateAndTime.minute >= 0)) or (
                today == "Sunday"):
            if weekendAlert():
                weeklyStatsMain()
            logger.info("It's the weekend, waiting for new week to start.")
        else:
            alertshiftstart()
            mdyTamCustMain()
            # 24 hours shift cover.
            # Except to start polling Zendesk on Monday from 1:00 AM CEST.
            # And to continue polling until Saturday as long as hour is less than 2:00 AM CEST -> since US shift ends on Saturday at 02:00 (From CEST point of view).
            if today in working_days or (today == "Monday" and currentDateAndTime.hour >= 1) or (
                    today == "Saturday" and currentDateAndTime.hour <= 2):
                logger.info(f'The current time is {currentTime}')
                try:
                    # lont = List of new tickets.
                    lont = getAllTickets()
                    if lont:
                        validated_tickets, lont_w_orgName_local = validateTickets(lont)
                        if validated_tickets and lont_w_orgName_local:
                            updated_tam_to_cust_w_ticket_id = update_tam_to_cust_w_ticket_id(validated_tickets)
                            postMsgTicketInfo(lont_w_orgName_local, updated_tam_to_cust_w_ticket_id)
                    # if lont:
                    #     logger.info(f"Found {len(lont)} new tickets in the queue!")
                    #     # list with company names added
                    #     lont_w_OrgNames = getOrgName(lont)
                    #     if lont_w_OrgNames:
                    #
                    #         # Check for the customer assigned TAM name from Monday.com only upon the detection of 'new tickets'
                    #         # tam_cust_assignments_from_Monday = mdy().getDatafromdy()
                    #         tam_cust_assignments_from_Monday = ret_tam_to_customer_mappings()
                    #         # print(f"tam_cust_assignments_from_Monday -> {tam_cust_assignments_from_Monday}")
                    #         tam_to_cust_w_ticket_id = getOrgNameMonday(tam_cust_assignments_from_Monday,
                    #                                                    lont_w_OrgNames)
                    #         updated_tam_to_cust_w_ticket_id = update_tam_to_cust_w_ticket_id(tam_to_cust_w_ticket_id)
                    #         # print(f"updated_tam_to_cust_w_ticket_id -> {updated_tam_to_cust_w_ticket_id}")
                    #         # print(f"length of updated_tam_to_cust_w_ticket_id -> {len(updated_tam_to_cust_w_ticket_id)}")
                    #         # # Posts messages created to the WxT space
                    #         postMsgTicketInfo(lont_w_OrgNames, updated_tam_to_cust_w_ticket_id)
                except Exception or KeyboardInterrupt as e:
                    logger.info(f"An error occurred to execute the main task: {str(e)}")
            else:
                logger.info(f"Shift to start at 02:00 CEST on Monday morning. Sleeping for now")
        # Wait for the specified interval before making the next API call
        time.sleep(tQw().zendesk_polling_interval)

        # # Testing without any time checking
        # lont = getAllTickets()
        # if lont:
        #     logger.info(f"Found {len(lont)} new tickets in the queue!")
        #     # list with company names added
        #     lont_w_OrgNames = getOrgName(lont)
        #     if lont_w_OrgNames:
        #         # Check for the customer assigned TAM name from Monday.com only upon the detection of 'new tickets'
        #         # tam_cust_assignments_from_Monday = mdy().getDatafromdy()
        #         tam_cust_assignments_from_Monday = ret_tam_to_customer_mappings()
        #         tam_to_cust_w_ticket_id = getOrgNameMonday(tam_cust_assignments_from_Monday,
        #                                                    lont_w_OrgNames)
        #         updated_tam_to_cust_w_ticket_id = update_tam_to_cust_w_ticket_id(tam_to_cust_w_ticket_id)
        #         # # Posts messages created to the WxT space
        #         postMsgTicketInfo(lont_w_OrgNames, updated_tam_to_cust_w_ticket_id)
        # time.sleep(tQw().zendesk_polling_interval)


if __name__ == "__main__":
    main()
