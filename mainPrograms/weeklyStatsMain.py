import logging
from weeklyStats.readWeeklyStatsfromFile import readHandledTicketsDataFromFile
# from tQwAlerter.shiftTimeDataClass import ShifttimeData as sd
from weeklyStats.weeklyStatsMsgGenerator import createWeeklyStatsMsg
from ticketAndMsgHandlers.msgPoster import sendMessageToWxT
from weeklyStats.weeklyStatsPerRegionMsgGenerator import createWeeklyStatsPerRegionMsg
# import time
# from datetime import datetime
from Tools.jsonFileCleaner import cleanJsonFiles

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Weekly Team stats generator")

def weeklyStatsMain():
    read_data = readHandledTicketsDataFromFile()
    if read_data:
        sendMessageToWxT(createWeeklyStatsMsg(read_data))
        sendMessageToWxT(createWeeklyStatsPerRegionMsg(read_data))
        file_path = "Files/weeklyStats.json"
        cleanJsonFiles(file_path)
        logger.info("Weekend is here... resting...")


if __name__ == '__main__':
    weeklyStatsMain()
    # file_path = "Files/weeklyStats.json"
    # cleanJsonFiles(file_path)
