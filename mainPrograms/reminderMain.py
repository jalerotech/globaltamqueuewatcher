from reminderFeature.readfromReminderFile import read_json_file_line_by_line
from reminderFeature.processReminderData import retTickFromDataList
from reminderFeature.reminderMsgHandler import createRmndrMsg, reset_tam_assigned_tickets_stats
from tQwAlerter.shiftTimeDataClass import ShifttimeData as sd
import logging
import time
from Tools.jsonFileCleaner import cleanJsonFiles

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def runReminderService() -> None:
    """
    Runs the reminder program
    :return: None
    """
    logger = logging.getLogger("runReminderService")
    logger.info("Running Reminder Service Program")

    while True:
        weekend_data = sd().weekendAlertData()
        # Start clean up process once weekend data is received.
        if weekend_data:
            logger.info(f"Weekend is here. Time to clean up database file. \n")
            reminder_file_path = "Files/reminder_data.json"
            is_cleaned = cleanJsonFiles(reminder_file_path)
            if is_cleaned:
                logger.info(f"Reminder file clean status -> {is_cleaned} thus Cleaned. \n ")
        else:
            createRmndrMsg(retTickFromDataList(read_json_file_line_by_line()))
            shift_data = sd().theatre_shift_time()
            if shift_data:
                # Resets the tam_assigned_tickets_stats dict after every shift has ended.
                if shift_data['status'] == "ended 🏁":
                    # wait 30 seconds before resetting the tam_assigned_ticket_stats
                    time.sleep(30)
                    reset_tam_assigned_tickets_stats()
            else:
                logger.info(f"Continuing as usual in 60 seconds, no shift data received. \n ")
        time.sleep(60)


if __name__ == '__main__':
    runReminderService()
