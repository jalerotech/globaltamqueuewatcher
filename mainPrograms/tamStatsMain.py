import logging
from tamTicketStats.createAndPostTamStats import createStatsMsg
from ticketAndMsgHandlers.msgPoster import sendMessageToWxT
import time
from datetime import datetime
from Tools.jsonFileCleaner import cleanJsonFiles

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("TAM Ticket stats generator")


def tamStatsMain():
    while True:
        currentDateAndTime = datetime.now()
        today = currentDateAndTime.strftime('%A')
        if (today == "Saturday" and (currentDateAndTime.hour >= 2 and currentDateAndTime.minute >= 0)) or (
                today == "Sunday"):
            logger.info(f"Weekend is here. Time to clean up database file. \n")
            reminder_file_path = "Files/tamTicketStats.json"
            cleanJsonFiles(reminder_file_path)
        else:
            stats_msg = createStatsMsg()
            if stats_msg:
                logger.info("TAM stats message received.")
                logger.info("Waiting 20 seconds before posting the message.")
                time.sleep(45)
                logger.info("Posting TAM stats message - STARTED")
                sendMessageToWxT(stats_msg)
                logger.info("Posting TAM stats message - COMPLETED")
            else:
                logger.info("No Stats message received, waiting for next stats message. \n")
        time.sleep(20)


if __name__ == '__main__':
    tamStatsMain()

