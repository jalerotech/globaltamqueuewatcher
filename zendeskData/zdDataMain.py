import logging
from zendeskData.fetchProcessZendeskData import validateTickets

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Zendesk Data Main')

def runZdDataMain(lont):
    validateTickets(lont)
