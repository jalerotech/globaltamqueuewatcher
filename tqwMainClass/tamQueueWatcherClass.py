from pathlib import Path
from dotenv import load_dotenv
import os
import json

env_path = Path('.') / 'authkey.env'
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    pass


class TamQueueWatcher:

    def __init__(self):
        # Content type for request headers
        self.contentType = 'application/json'

        # Loading AuthKeys via environment variables:

        self.zendesk_auth_key = os.getenv('zendesk_auth_key')
        self.WebEx_teams_auth_key = os.getenv('WebEx_teams_auth_key')
        self.monday_auth_keys = os.getenv('monday_auth_keys')

        # Tests Bot and space:
        self.tqw_webex_token = os.getenv('tqw_webex_token')
        self.tamqueuewatcher_room_id = os.getenv('tamqueuewatcher_room_id')
        self.Global_TAM_UMB_Queue_watcher = os.getenv('Global_TAM_UMB_Queue_watcher')

        self.cstat_access_token = os.getenv('CloudSecTeamAvailabilityTracker_access_token')
        # Set the header Webex API Endpoint - specifically for CSTAT.
        self.cstat_webex_headers = {
            'Content-Type': self.contentType,
            'Authorization': f'Bearer {self.cstat_access_token}'
        }

        # Requests Variables #

        # Set the API Zendesk Endpoint to fetch all tickets
        self.zendesk_api_url = 'https://opendns.zendesk.com/api/v2/views/159080128/tickets.json'
        self.zendesk_org_url = "https://opendns.zendesk.com/api/v2/organizations/"
        self.zendesk_user_url = "https://opendns.zendesk.com/api/v2/users/"

        # BFG base url
        self.bfg_base_url = "https://bfg.umbrella.com/organizations/organization/"

        # Monday API URL

        self.monday_api_url = "https://api.monday.com/v2"

        # Set the headers for ZenDesk Q
        self.zendesk_headers = {
            'Content-Type': self.contentType,
            'Authorization': f'Basic {self.zendesk_auth_key}'
        }

        self.monday_headers = {
            'Content-Type': self.contentType,
            'Authorization': {self.monday_auth_keys}
        }

        # Set the url Webex API Endpoint
        self.webex_api_url = 'https://webexapis.com/v1/messages'

        # WebEx base URL:
        self.webex_base_url = 'https://webexapis.com/v1/'

        # Set the header Webex API Endpoint - Production.
        self.webex_headers = {
            'Content-Type': self.contentType,
            'Authorization': f'Bearer {self.WebEx_teams_auth_key}'
        }

        # Set the header for Monday.com API
        self.monday_headers = {
            "Authorization": f"Bearer {self.monday_auth_keys}"
        }

        # Set the header for Monday.com API
        self.monday_headers_api_versioning = {
            "Authorization": self.monday_auth_keys,
            'Content-Type': 'application/json',
            'API-Version': '2024-01'
        }

        # Set the ticket status to monitor
        self.ticket_status = 'new'

        # Excluded tickets with this string in the no_reply_recipient:
        self.no_reply_recipient = 'umbrella-research-noreply@cisco.com'

        # TAC collab:
        self.tac_collab = 'tac-to-umbrella-premium@cisco.com'
        self.csone_short_base_url = 'http://mwz/'
        self.ext_tac_case_base_url = 'https://mycase.cloudapps.cisco.com/'

        # Set the interval for the API to Zendesk call (in seconds)
        self.zendesk_polling_interval = 60

        # Initialize an empty set to keep track of processed tickets
        self.processed_tickets = set()

        # Zendesk Agent Base URL -> Used by agents to access tickets on Zendesk
        self.zend_agent_tickets_url = f"https://opendns.zendesk.com/agent/tickets/"
        self.zendesk_ticket_base_url = f"https://opendns.zendesk.com/api/v2/tickets/"

        # Ticket message label(s):
        self.unassigned_label = "None Assigned"
        self.not_set = "Not Set"
        self.hour_trigger = "HOUR"
        self.half_hour_trigger = "HALF_HOUR"
        self.quarter_hour_trigger = "QUARTER_HOUR"

        self.EMEA_region = ['GB', 'BE', 'PL', 'ES', 'PT']
        self.US_region = ['CR', 'US', 'CA']
        self.APAC_region = ['AU', 'CN', 'JP', 'IN']
        self.cloud_sec_team_members = ['anattwoo@cisco.com', 'jalero@cisco.com', 'prersinh@cisco.com',
                                       'aparedez@cisco.com', 'arjraina@cisco.com', 'ajavaher@cisco.com',
                                       'bewallac@cisco.com',
                                       'brparnel@cisco.com', 'ccoral@cisco.com',
                                       'dforcade@cisco.com',
                                       'diebarra@cisco.com', 'hputra@cisco.com', 'harmeije@cisco.com',
                                       'ianave@cisco.com',
                                       'halijenn@cisco.com', 'jesshepp@cisco.com', 'jonleduc@cisco.com',
                                       'kahowes@cisco.com',
                                       'kevhudso@cisco.com', 'kporzezr@cisco.com', 'kvindas@cisco.com',
                                       'magainer@cisco.com', 'mneibert@cisco.com', 'nnwobodo@cisco.com',
                                       'paulth2@cisco.com',
                                       'pwijenay@cisco.com',
                                       'sknez@cisco.com', 'tarrashi@cisco.com', 'tingwa2@cisco.com',
                                       'ugandhi@cisco.com',
                                       'wgardeaz@cisco.com', 'rgwillia@cisco.com',
                                       'xiaoshya@cisco.com', 'yusito@cisco.com', "hputra@cisco.com"]

        self.tams = ['jalero@cisco.com', 'aparedez@cisco.com', 'anattwoo@cisco.com', 'dforcade@cisco.com',
                     'kporzezr@cisco.com', 'nnwobodo@cisco.com', 'arjraina@cisco.com',
                     'ajavaher@cisco.com', 'brparnel@cisco.com', 'ccoral@cisco.com', 'kevhudso@cisco.com',
                     'kvindas@cisco.com', 'mneibert@cisco.com', 'paulth2@cisco.com', 'pwijenay@cisco.com',
                     'tarrashi@cisco.com', 'tingwa2@cisco.com', 'ugandhi@cisco.com', 'wgardeaz@cisco.com',
                     'xiaoshya@cisco.com', 'yusito@cisco.com', "magainer@cisco.com", "diebarra@cisco.com",
                     "jesshepp@cisco.com", "jonleduc@cisco.com", "hputra@cisco.com", "harmeije@cisco.com"]

        # TSE team members:
        self.tse_TLs = ["mbignell@cisco.com", "roavrame@cisco.com", "dbarksda@cisco.com", "deqpowel@cisco.com",
                        "rmargall@cisco.com", "dsaludes@cisco.com", "chrstew2@cisco.com"]
        self.tse_Mngrs = ["prersinh@cisco.com", "msarband@cisco.com", "dpetrezs@cisco.com", "micolema@cisco.com",
                          "rwamer@cisco.com", "ezgable@cisco.com", "kendang@cisco.com", "vesenthi@cisco.com"]
        # EMEA

        self.TSE_EMEA = ["roavrame@cisco.com", "mbignell@cisco.com", "beash@cisco.com", "cloupas@cisco.com",
                         "harpraja@cisco.com", "kloxdale@cisco.com", "rosahni@cisco.com", "rysia@cisco.com",
                         "bilbarne@cisco.com", "gonzamar@cisco.com",
                         "arataj@cisco.com", "nucabral@cisco.com", "balka@cisco.com",
                         "malnadi@cisco.com", "namro@cisco.com", "oghawi@cisco.com", "zalali@cisco.com"]
        self.TSE_Mngrs_EMEA = ["vesenthi@cisco.com", "dpetrezs@cisco.com"]
        self.TSE_TLs_EMEA = ["mbignell@cisco.com", "roavrame@cisco.com"]

        # APAC

        self.TSE_APAC = ["chrstew2@cisco.com", "hmushtaq@cisco.com", "syedsyed@cisco.com", "esgoyal@cisco.com"]
        self.TSE_Mngrs_APAC = ["prersinh@cisco.com"]
        self.TSE_TLs_APAC = ["chrstew2@cisco.com"]

        # US-EAST

        self.TSE_US_EAST = ["dbarksda@cisco.com", "deqpowel@cisco.com", "aakindel@cisco.com", "ftodote@cisco.com",
                            "henrthom@cisco.com", "janeandr@cisco.com", "ljoyner@cisco.com", "mzejli@cisco.com",
                            "pragagra@cisco.com", "skeckii@cisco.com", "tinclark@cisco.com", "tkeshinr@cisco.com",
                            "ookon@cisco.com", "stegille@cisco.com"]

        self.TSE_Mngrs_EAST = ["rwamer@cisco.com", "ezgable@cisco.com"]
        self.TSE_TLs_EAST = ["dbarksda@cisco.com", "deqpowel@cisco.com"]

        # US-WEST:
        self.TSE_US_WEST = ["rmargall@cisco.com", "dsaludes@cisco.com", "alihass@cisco.com", "awaramma@cisco.com",
                            "daadum@cisco.com", "jaishah2@cisco.com", "mpourman@cisco.com", "nidsaxen@cisco.com",
                            "nimoalle@cisco.com", "skarimia@cisco.com", "sshaghay@cisco.com", "zchiang@cisco.com",
                            "atrahbar@cisco.com", "cupan@cisco.com", "davidng3@cisco.com", "robchu@cisco.com",
                            "santjana@cisco.com"]
        self.TSE_Mngrs_WEST = ["kendang@cisco.com", "msarband@cisco.com", "micolema@cisco.com"]
        self.TSE_TLs_WEST = ["rmargall@cisco.com", "dsaludes@cisco.com"]

