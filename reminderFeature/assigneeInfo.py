import requests
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

# treated_tickets = set()


def get_user_info(ticket):
    logger = logging.getLogger("Running 'get_user_info' function..")
    """
    Produces the assignee email and name using the assignee id fetched from Zendesk
    :param assignee_id: Assignee_id from ticket data fetched from Zendesk.
    :return: User information in dict format.
    """

    logger.info(f"Linking assignee_id to user information.")
    assignee_id = get_assignee_id(ticket)
    if assignee_id:
        url = f"{tqw().zendesk_user_url}{assignee_id}.json"
        zendesk_response = requests.get(url, headers=tqw().zendesk_headers)
        if zendesk_response.status_code == 200:
            # Parse the JSON response
            user_data = zendesk_response.json()
            # Extract and return relevant user information
            user_info = {
                'ID': user_data['user']['id'],
                'Name': user_data['user']['name'],
                'Email': user_data['user']['email']
            }
            logger.info(f"Returning user info dict -> {user_info}.")
            return user_info

    # if ticket['ticket_id'] not in treated_tickets:
    #     treated_tickets.add(ticket['ticket_id'])
    #     logger.info(f"Linking assignee_id to user information.")
    #     assignee_id = get_assignee_id(ticket)
    #     if assignee_id:
    #         url = f"{tqw().zendesk_user_url}{assignee_id}.json"
    #         zendesk_response = requests.get(url, headers=tqw().zendesk_headers)
    #         if zendesk_response.status_code == 200:
    #             # Parse the JSON response
    #             user_data = zendesk_response.json()
    #             # Extract and return relevant user information
    #             user_info = {
    #                 'ID': user_data['user']['id'],
    #                 'Name': user_data['user']['name'],
    #                 'Email': user_data['user']['email']
    #             }
    #             logger.info(f"Returning user info dict -> {user_info}.")
    #             return user_info


def get_assignee_id(ticket) -> int:
    logger = logging.getLogger('Reminder service - assignee_id')
    logger.info("Getting Ticket specific data containing the assignee ID.")
    ticket_url = f"{tqw().zendesk_ticket_base_url}{ticket['ticket_id']}.json"
    zendesk_response = requests.get(ticket_url, headers=tqw().zendesk_headers)
    if zendesk_response.status_code == 200:
        # Parse the JSON response
        ticket_data = zendesk_response.json()
        return ticket_data['ticket']['assignee_id']

#
# if __name__ == '__main__':
#     ticket = {'ticket_counter': 3, 'subject': 'SCTASK0782762 - Provide access to blocked website', 'assignee': 360606549946, 'ticket_id': 1729693, 'created_at': '2024-01-10T18:45:18Z'}
#     # get_user_info(12466330566932)
#     # print(get_assignee_id(ticket))
#     print(get_user_info(ticket))
