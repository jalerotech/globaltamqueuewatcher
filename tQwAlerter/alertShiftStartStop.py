from tQwAlerter.shiftTimeDataClass import ShifttimeData
import logging
from ticketAndMsgHandlers.msgPoster import sendMessageToWxT
from statsHandler.createAndPostStats import postDailyShiftTicketSummary, apacPreWeekendStatsSummary
from ticketAndMsgHandlers.handleTicketMessages import returnCurrentDataForStats, reset_tickets_handled_today, reset_processed_tickets
from zendeskData.fetchProcessZendeskData import reset_sets_of_tickets_no_time_check, reset_ticket_msg_sent
from Tools.jsonFileCleaner import cleanJsonFiles
# from mainPrograms.ptoAvailabilityWatcherMain import ptoWatcherMain

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def alertshiftstart() -> None:
    shift_data = ShifttimeData().theatre_shift_time()
    """
    Post messages to WxT when shift starts at 08:00 and ends at 16:00 CEST (EMEA)
    or
    Post messages to WxT when shift starts at 15:00 and ends at 02:00 CEST (US with 1 hour overlap with APAC)
    or 
    Post messages to WxT when shift starts at 01:00 and ends at 09:00 CEST (APAC with 1 hour overlap with EMEA)
    :param shift_data
    :return: None
    """
    if shift_data:
        logger = logging.getLogger('Alerting shift start/stop.')
        logger.info(f"Shift data produced -> {shift_data}")
        logger.info(f"Posting {shift_data['theatre']} Shift {shift_data['status']} message.")
        data = {
            "text": f"Time is now {shift_data['shift_time']}, {shift_data['theatre']} shift has {shift_data['status']}",
            "markdown": f"**Time is now {shift_data['shift_time']}, _{shift_data['theatre']}_ shift has {shift_data['status']}**."
        }
        logger.info(f"{shift_data['theatre']} shift {shift_data['status']}.")
        sendMessageToWxT(data)
        logger.info(f"Posting Shift {shift_data['status']} message. -> COMPLETED")
        # Handle stats posting after shift end alert sent.
        if shift_data['status'] == "ended 🏁":
            postDailyShiftTicketSummary(returnCurrentDataForStats(), shift_data)
        # # Checks that the status in the shift data is "started" before posting the PTO alerts.
        # if shift_data['status'] == "started 🎬":
        #     ptoWatcherMain('Not_local')


def weekendAlert() -> bool:
    """
    posts weekend alert when conditions are met.
    :return: None
    """
    shift_data = ShifttimeData().weekendAlertData()
    # logger = logging.getLogger('Generating Weekend Alert.')
    if shift_data:
        logger = logging.getLogger('Generating Weekend Alert.')
        logger.info(f"Data produced -> {shift_data}")
        logger.info(f"Posting {shift_data['status']} Alert for ALL {shift_data['theatre']} message. -> STARTED")
        data = {
            "text": f"Time is now {shift_data['shift_time']}, it's {shift_data['status']} for ALL theatres.",
            "markdown": f"**Time is now {shift_data['shift_time']}, it's {shift_data['status']} for ALL theatres**."
        }
        logger.info(f"{shift_data['theatre']} with status {shift_data['status']}.")
        sendMessageToWxT(data)
        logger.info(f"Posting {shift_data['status']} Alert for ALL {shift_data['theatre']} message. -> COMPLETED")
        # Create APAC TSE stats to be sent before resetting counters.
        # HardCoded shift data for APAC TSE timeslot
        TSE_APAC_Custom_shift_data = {
            "theatre": "TSE_APAC",
            "status": "ended 🏁"
        }
        apacPreWeekendStatsSummary(returnCurrentDataForStats(), TSE_APAC_Custom_shift_data)
        reset_processed_tickets()
        reset_tickets_handled_today()
        reset_sets_of_tickets_no_time_check()
        reset_ticket_msg_sent()
        # Clean up files hardcoded in the cleanJsonFiles function.
        cleanJsonFiles(None)
        return True
    # else:
    #     logger.info("No shift data produced - Not weekend yet")


if __name__ == '__main__':
    alertshiftstart()
    # weekendAlert()
