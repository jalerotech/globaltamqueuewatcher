import logging


logger = logging.getLogger("Remindder Data Processor")

processed_reminder_tickets = []


def retTickFromDataList(ticket_dict_list):
    # print(ticket_dict_list)
    for ticket_dict in ticket_dict_list:
        processed_reminder_tickets.append(ticket_dict)
    return processed_reminder_tickets
    # print(processed_reminder_tickets)
