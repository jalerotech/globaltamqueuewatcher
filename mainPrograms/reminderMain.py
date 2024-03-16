from reminderFeature.readfromReminderFile import read_json_file_line_by_line
from reminderFeature.processReminderData import retTickFromDataList
from reminderFeature.reminderMsgHandler import createRmndrMsg, reset_tam_assigned_tickets_stats
from tQwAlerter.shiftTimeDataClass import ShifttimeData as sd
import logging
import time
from datetime import datetime
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

    currentDateAndTime = datetime.now()
    today = currentDateAndTime.strftime('%A')
    while True:
        createRmndrMsg(retTickFromDataList(read_json_file_line_by_line()))
        shift_data = sd().theatre_shift_time()
        if shift_data:
            # Reset the tam_assigned_tickets_stats dict after every shift has ended.
            if shift_data['status'] == "ended 🏁":
                reset_tam_assigned_tickets_stats()
                # reminder_file_path = "Files/reminder_data.json"
                # cleanJsonFiles(reminder_file_path)
        if (today == "Saturday" and (currentDateAndTime.hour > 2 and currentDateAndTime.minute > 0)) or (today == "Sunday"):
            logger.info(f"Weekend is here, cleaning up the reminder_data.json file. - STARTED.")
            reminder_file_path = "Files/reminder_data.json"
            cleanJsonFiles(reminder_file_path)
            logger.info(f"Weekend is here, cleaning up the reminder_data.json file. - COMPLETED.")
        time.sleep(60)


if __name__ == '__main__':
    runReminderService()
