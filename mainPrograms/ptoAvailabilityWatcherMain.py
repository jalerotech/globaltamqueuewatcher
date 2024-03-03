import logging
import time
from TamPtoTracker.getPersonDataWebEx import get_users_status
from TamPtoTracker.ptoMsgGenerator import genPTOMsg
from ticketAndMsgHandlers.msgPoster import sendMessageToWxT, sendMessageToWxT4Cstat
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw
from TamPtoTracker.TamPTOMsgDataGenerator import tamPTOMsgDataWriter
from tQwAlerter.shiftTimeDataClass import ShifttimeData as sd

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('TAM PTO script')

tam_in_ooo_export = []


def ptoWatcherMain(label) -> list:
    logger.info(f"Running the PTO Watcher Main function with a fixed list of TAM resources.")
    """
    Runs the main PTO programs using the imported modules "get_users_status", "genPTOMsg" and "sendMessageToWxT".
    :param:
    :return: None
    """

    tam_in_ooo = get_users_status(tqw().list_of_tam)
    if label == 'local':
        pto_msg = genPTOMsg(tam_in_ooo, "For_CloudSec_Only")
        sendMessageToWxT4Cstat(pto_msg)
        tamPTOMsgDataWriter(tam_in_ooo)
        return tam_in_ooo
    else:
        # Could be redundant as PTO alerts are not sent to the Queue Watcher space anymore due to the "noise" on that space.
        pto_msg = genPTOMsg(tam_in_ooo, "For_TAM_Only")
        sendMessageToWxT(pto_msg)
        tamPTOMsgDataWriter(tam_in_ooo)


def StandalonePTOWatcherMain(label) -> None:
    """
    Runs the standalone PTO alert function and adds label string "local" to ensure that the Alert is posted to the For_CloudSec_Only space.
    :param label:
    :return: None
    """
    logger_local = logging.getLogger('Running StandalonePTOWatcherMain Function')
    while True:
        logger_local.info('Running StandalonePTOWatcherMain - STARTED.')
        shift_data = sd().theatre_shift_time()
        if shift_data:
            logger_local.info(f'Shift data received {shift_data}.')
            if shift_data['status'] == "started 🎬":
                ptoWatcherMain(label)
            logger_local.info('Running StandalonePTOWatcherMain - COMPLETED.')
        logger_local.info('No new shift data received - Not yet time for PTO alert - COMPLETED.')
        logger.info("Pausing for 60 seconds before trying again.")
        time.sleep(tqw().zendesk_polling_interval)


if __name__ == '__main__':
    # ptoWatcherMain("local")
    StandalonePTOWatcherMain('local')
    # user_email = ['anattwoo@cisco.com', 'aely@cisco.com', 'jalero@cisco.com',
    #               'aparedez@cisco.com', 'arjraina@cisco.com', 'ajavaher@cisco.com', 'bewallac@cisco.com',
    #               'brparnel@cisco.com', 'ccoral@cisco.com', 'ccardina@cisco.com', 'dforcade@cisco.com',
    #               'diebarra@cisco.com', 'hputra@cisco.com', 'harmeije@cisco.com', 'ianave@cisco.com',
    #               'halijenn@cisco.com', 'jesshepp@cisco.com', 'jonleduc@cisco.com', 'kahowes@cisco.com',
    #               'kajus@cisco.com', 'kevhudso@cisco.com', 'kporzezr@cisco.com', 'kvindas@cisco.com',
    #               'magainer@cisco.com', 'mneibert@cisco.com', 'nnwobodo@cisco.com', 'paulth2@cisco.com',
    #               'pwijenay@cisco.com',
    #               'sknez@cisco.com', 'tarrashi@cisco.com', 'tingwa2@cisco.com', 'ugandhi@cisco.com',
    #               'wgardeaz@cisco.com',
    #               'xiaoshya@cisco.com', 'yusito@cisco.com']
    # ptoWatcherMain(user_email)