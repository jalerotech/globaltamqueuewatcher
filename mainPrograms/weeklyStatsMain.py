import logging
from weeklyStats.readWeeklyStatsfromFile import readHandledTicketsDataFromFile
# from tQwAlerter.shiftTimeDataClass import ShifttimeData as sd
from weeklyStats.weeklyStatsMsgGenerator import createWeeklyStatsMsg
from ticketAndMsgHandlers.msgPoster import sendMessageToWxT
# import time
# from datetime import datetime
from Tools.jsonFileCleaner import cleanJsonFiles

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Weekly Team stats generator")


# def weeklyStatsMain():
#     currentDateAndTime = datetime.now()
#     today = currentDateAndTime.strftime('%A')
#     weekend_data = sd().weekendAlertData()
#     # read_data = readHandledTicketsDataFromFile()
#     # sendMessageToWxT(createWeeklyStatsMsg(read_data))
#     while True:
#         if (today == "Saturday" and (currentDateAndTime.hour >= 2 and currentDateAndTime.minute >= 0)) or (today == "Sunday"):
#             file_path = "Files/weeklyStats.json"
#             cleanJsonFiles(file_path)
#             logger.info("Weekend is here... resting...")
#         if weekend_data:
#             read_data = readHandledTicketsDataFromFile()
#             sendMessageToWxT(createWeeklyStatsMsg(read_data))
#         else:
#             logger.info(f"Not yet time for weekly stats.")
#         # else:
#         #     if weekend_data:
#         #         read_data = readHandledTicketsDataFromFile()
#         #         sendMessageToWxT(createWeeklyStatsMsg(read_data))
#         #     else:
#         #         logger.info(f"Not yet time for weekly stats.")
#         time.sleep(60)

def weeklyStatsMain():
    read_data = readHandledTicketsDataFromFile()
    if read_data:
        sendMessageToWxT(createWeeklyStatsMsg(read_data))
        file_path = "Files/weeklyStats.json"
        cleanJsonFiles(file_path)
        logger.info("Weekend is here... resting...")


if __name__ == '__main__':
    weeklyStatsMain()
    # file_path = "Files/weeklyStats.json"
    # cleanJsonFiles(file_path)
