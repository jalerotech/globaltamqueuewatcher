from reminderFeature.readfromReminderFile import read_json_file_line_by_line
from reminderFeature.processReminderData import retTickFromDataList
from reminderFeature.reminderMsgHandler import createRmndrMsg, reset_tam_assigned_tickets_stats,  reset_is_assigned_msg_sent, ret_tam_assigned_tickets_stats, ret_is_assigned_msg_sent
from tQwAlerter.shiftTimeDataClass import ShifttimeData as sd
import logging
import time
from Tools.jsonFileCleaner import cleanJsonFiles
from datetime import datetime

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
        # weekend_data = sd().weekendAlertData()
        currentDateAndTime = datetime.now()
        today = currentDateAndTime.strftime('%A')
        # Start clean up process once weekend data is received.
        # if weekend_data:
        if (today == "Saturday" and (currentDateAndTime.hour >= 2 and currentDateAndTime.minute >= 0)) or (
                today == "Sunday"):
            logger.info(f"Weekend is here. Time to clean up database file. \n")
            reminder_file_path = "Files/reminder_data.json"
            is_cleaned = cleanJsonFiles(reminder_file_path)
            if is_cleaned:
                logger.info(f"Reminder file clean status -> {is_cleaned} thus Cleaned. \n ")
                # Reset tam_ticket_assignment_data after cleaning reminder file
                # But only reset if the length is not 0
                if len(ret_tam_assigned_tickets_stats()) > 0:
                    reset_tam_assigned_tickets_stats()
                if len(ret_is_assigned_msg_sent()) > 0:
                    reset_is_assigned_msg_sent()
            else:
                logger.info(f"Reminder json file already cleaned.")
                logger.info(f"Weekend... resting...")
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
