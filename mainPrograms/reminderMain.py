from reminderFeature.readfromReminderFile import read_json_file_line_by_line
from reminderFeature.processReminderData import retTickFromDataList
from reminderFeature.reminderMsgHandler import createRmndrMsg
import logging
import time

# logger = logging.getLogger("Remainder Main Service")

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def runReminderService():
    logger = logging.getLogger("runReminderService")
    logger.info("Running Reminder Service Program")
    while True:
        createRmndrMsg(retTickFromDataList(read_json_file_line_by_line()))
        time.sleep(60)


if __name__ == '__main__':
    runReminderService()
