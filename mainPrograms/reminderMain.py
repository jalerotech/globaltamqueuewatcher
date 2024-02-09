from reminderFeature.readfromReminderFile import read_json_file_line_by_line
from reminderFeature.processReminderData import retTickFromDataList
from reminderFeature.reminderMsgHandler import createRmndrMsg
import logging
import time
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

    currentDateAndTime = datetime.now()
    today = currentDateAndTime.strftime('%A')

    while True:
        createRmndrMsg(retTickFromDataList(read_json_file_line_by_line()))
        if (today == "Saturday" and (currentDateAndTime.hour > 2 and currentDateAndTime.minute > 0)) or (today == "Sunday"):
            logger.info(f"Weekend is here, cleaning up the reminder_data.json file. - STARTED.")
            with open("Files/reminder_data.json", 'w') as json_file:
                json_file.close()
            logger.info(f"Weekend is here, cleaning up the reminder_data.json file. - COMPLETED.")
        time.sleep(60)


if __name__ == '__main__':
    runReminderService()
