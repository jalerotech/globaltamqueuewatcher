import logging
from datetime import datetime
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class ShifttimeData:
    def __init__(self):
        self.logger = logging.getLogger('ShifttimeData')
        self.currentDateAndTime = datetime.now()
        self.today = self.currentDateAndTime.strftime('%A')

    def theatre_shift_time(self) -> dict:
        """
        Produces the theatre name, and shift time needed to send the start and stop of shift alert.
        """
        # Test data:
        # if (self.currentDateAndTime.hour == 20) and (self.currentDateAndTime.minute == 0) and (self.today != "Saturday" or self.today != "Sunday"):
        # if (self.today != "Saturday" or self.today != "Monday"):
        # if (self.currentDateAndTime.hour == 20) and (self.currentDateAndTime.minute > 8):
        #     self.logger.info('Getting shift time and status...')
        #     shift_data = {
        #         "theatre": "CYBERTRON",
        #         "shift_time": "17:10 CEST",
        #         "status": "started 🎬"
        #     }
        #     return shift_data
        # if (self.currentDateAndTime.hour == 20) and (self.currentDateAndTime.minute == 48) and (self.today != "Monday"):
        #     self.logger.info('Getting shift time and status...')
        #     shift_data = {
        #         "theatre": "CYBERTRON",
        #         "shift_time": "17:15 CEST",
        #         "status": "ended"
        #     }
        #     return shift_data

        # # Shift start
        # APAC
        # Except for Saturday and Sunday
        if self.today != "Saturday" and self.today != "Sunday":
            if (self.currentDateAndTime.hour == 1) and (self.currentDateAndTime.minute == 0):
                self.logger.info('Getting shift time and status...')
                shift_data = {
                    "theatre": "TSE_APAC",
                    "shift_time": "10:00 AEDT",
                    "status": "started 🎬"
                }
                return shift_data

            # # TSE-APAC
            # if self.today != "Saturday" and self.today != "Sunday":
            #     if (self.currentDateAndTime.hour == 1) and (self.currentDateAndTime.minute == 0):
            #         self.logger.info('Getting shift time and status...')
            #         shift_data = {
            #             "theatre": "TSE_APAC",
            #             "shift_time": "10:00 AEDT",
            #             "status": "started 🎬"
            #         }
            #         return shift_data

        # EMEA-TAM
        #     if (self.currentDateAndTime.hour == 8) and (self.currentDateAndTime.minute == 0):
        #         self.logger.info('Getting shift time and status...')
        #         shift_data = {
        #             "theatre": "TAM_EMEA",
        #             "shift_time": "08:00 CET",
        #             "status": "started 🎬"
        #         }
        #         return shift_data
            # TSE-EMEA (TSE_EMEA (9am-4pm CET))
            if (self.currentDateAndTime.hour == 9) and (self.currentDateAndTime.minute == 1):
                self.logger.info('Getting shift time and status...')
                shift_data = {
                    "theatre": "TSE_EMEA",
                    "shift_time": "09:00 CET",
                    "status": "started 🎬"
                }
                return shift_data

        # US-TAM
        #     if (self.currentDateAndTime.hour == 15) and (self.currentDateAndTime.minute == 0):
        #         self.logger.info('Getting shift time and status...')
        #         shift_data = {
        #             "theatre": "TAM_US",
        #             "shift_time": "09:00 EST/EDT",
        #             "status": "started 🎬"
        #         }
        #         return shift_data
        # US-EAST (TSE_US_EAST (3pm CET-10PM CET))
            if (self.currentDateAndTime.hour == 15) and (self.currentDateAndTime.minute == 0):
                self.logger.info('Getting shift time and status...')
                shift_data = {
                    "theatre": "TSE_US_EAST",
                    "shift_time": "09:00 EST/EDT",
                    "status": "started 🎬"
                }
                return shift_data

        # US-WEST (TSE_US_WEST (6pm CET-2:30am CET))
            if (self.currentDateAndTime.hour == 18) and (self.currentDateAndTime.minute == 0):
                self.logger.info('Getting shift time and status...')
                shift_data = {
                    "theatre": "TSE_US_WEST",
                    "shift_time": "12:00 EST/EDT",
                    "status": "started 🎬"
                }
                return shift_data
        ################ Shift end #################
        if self.today != "Saturday":
            if (self.currentDateAndTime.hour == 8) and (self.currentDateAndTime.minute == 59):
                self.logger.info('Getting shift time and status...')
                shift_data = {
                    "theatre": "TSE_APAC",
                    "shift_time": "17:00 AEDT",
                    "status": "ended 🏁"
                }
                return shift_data

            # # EMEA-TAM
            # if (self.currentDateAndTime.hour == 16) and (self.currentDateAndTime.minute == 0):
            #     self.logger.info('Getting shift time and status...')
            #     shift_data = {
            #         "theatre": "TAM_EMEA",
            #         "shift_time": "16:00 CET",
            #         "status": "ended 🏁"
            #     }
            #     return shift_data

            # TSE-EMEA (TSE_EMEA (9am-4pm CET))
            if (self.currentDateAndTime.hour == 16) and (self.currentDateAndTime.minute == 0):
                self.logger.info('Getting shift time and status...')
                shift_data = {
                    "theatre": "TSE_EMEA",
                    "shift_time": "16:00 CET",
                    "status": "ended 🏁"
                }
                return shift_data

            # US-EAST (TSE_US_EAST (3pm CET-10PM CET))
            if (self.currentDateAndTime.hour == 22) and (self.currentDateAndTime.minute == 0):
                self.logger.info('Getting shift time and status...')
                shift_data = {
                    "theatre": "TSE_US_EAST",
                    "shift_time": "16:00 EDT/EST",
                    "status": "ended 🏁"
                }
                return shift_data

            # # US-WEST (TSE_US_WEST (6pm CET-2:30am CET)) (except for Monday morning)
            # if (self.currentDateAndTime.hour == 2) and (self.currentDateAndTime.minute == 30) and (self.today != "Monday"):
            #     self.logger.info('Getting shift time and status...')
            #     shift_data = {
            #         "theatre": "TSE_US_WEST",
            #         "shift_time": "20:30 EDT/EST",
            #         "status": "ended 🏁"
            #     }
            #     return shift_data

        # US-WEST (TSE_US_WEST (6pm CET-2:30am CET)) (except for Monday morning)
        if (self.currentDateAndTime.hour == 2) and (self.currentDateAndTime.minute == 0) and (self.today != "Monday"):
            self.logger.info('Getting shift time and status...')
            shift_data = {
                "theatre": "TSE_US_WEST",
                "shift_time": "20:00 EDT/EST",
                "status": "ended 🏁"
            }
            return shift_data

        # # US (except for Monday morning) - TAM
        # if (self.currentDateAndTime.hour == 2) and (self.currentDateAndTime.minute == 0) and (self.today != "Monday"):
        #     self.logger.info('Getting shift time and status...')
        #     shift_data = {
        #         "theatre": "TAM_US",
        #         "shift_time": "20:00 EST/EDT",
        #         "status": "ended 🏁"
        #     }
        #     return shift_data

    def weekendAlertData(self):
        # Global weekend alert!
        if (self.currentDateAndTime.hour == 2) and (self.currentDateAndTime.minute == 0) and (
                self.today == "Saturday"):
            self.logger.info('Getting weekend time and status/message...')
            shift_data = {
                "theatre": "All",
                "shift_time": "20:00 EST/EDT, 02:00 CEST and 11:00 AEDT",
                "status": "weekend 😴"
            }
            return shift_data
