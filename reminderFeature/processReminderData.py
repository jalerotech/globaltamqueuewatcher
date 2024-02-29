import logging


logger = logging.getLogger("Reminder Data Processor")

processed_reminder_tickets = []


def retTickFromDataList(ticket_dict_list) -> list:
    """
    Returns the ticket_dict_list. (This is not really needed and can be removed in the future.)
    :param ticket_dict_list:
    :return: ticket_dict_list
    """
    # for ticket_dict in ticket_dict_list:
    #     if ticket_dict['ticket_id'] not in processed_reminder_tickets:
    #         processed_reminder_tickets.append(ticket_dict)
    return ticket_dict_list
    # print(processed_reminder_tickets)
