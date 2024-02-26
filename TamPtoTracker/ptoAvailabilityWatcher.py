import logging
from TamPtoTracker.getPersonDataWebEx import get_users_status
from TamPtoTracker.ptoMsgGenerator import genPTOMsg
from ticketAndMsgHandlers.msgPoster import sendMessageToWxT

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('TAM PTO Bot')


def ptoWatcherMain() -> None:
    logger.info(f"Running the PTO Watcher Main function with a fixed list of TAM resources.")
    """
    Runs the main PTO programs using the imported modules "get_users_status", "genPTOMsg" and "sendMessageToWxT".
    :param:
    :return: None
    """
    list_of_tam = ['anattwoo@cisco.com', 'aely@cisco.com', 'jalero@cisco.com',
                   'aparedez@cisco.com', 'arjraina@cisco.com', 'ajavaher@cisco.com', 'bewallac@cisco.com',
                   'brparnel@cisco.com', 'ccoral@cisco.com', 'ccardina@cisco.com', 'dforcade@cisco.com',
                   'diebarra@cisco.com', 'hputra@cisco.com', 'harmeije@cisco.com', 'ianave@cisco.com',
                   'halijenn@cisco.com', 'jesshepp@cisco.com', 'jonleduc@cisco.com', 'kahowes@cisco.com',
                   'kevhudso@cisco.com', 'kporzezr@cisco.com', 'kvindas@cisco.com',
                   'magainer@cisco.com', 'mneibert@cisco.com', 'nnwobodo@cisco.com', 'paulth2@cisco.com',
                   'pwijenay@cisco.com',
                   'sknez@cisco.com', 'tarrashi@cisco.com', 'tingwa2@cisco.com', 'ugandhi@cisco.com',
                   'wgardeaz@cisco.com',
                   'xiaoshya@cisco.com', 'yusito@cisco.com']

    tam_in_ooo = get_users_status(list_of_tam)
    pto_msg = genPTOMsg(tam_in_ooo)
    sendMessageToWxT(pto_msg)


if __name__ == '__main__':
    ptoWatcherMain()
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
