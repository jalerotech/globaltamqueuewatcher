from tQwAlerter.shiftTimeDataClass import ShifttimeData as sD
import logging
from mondayData.tamCustomerMapping import ret_tam_to_customer_mappings

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Running mdyTamCustMain')


def mdyTamCustMain():
    logger.info(f"Running mdyTamCustMain function.")
    """
    Runs the main function.
    """
    # Checks for shift alert before creating mappings.
    shift_data = sD().theatre_shift_time()
    if shift_data:
        ret_tam_to_customer_mappings()

