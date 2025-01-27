import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def retHighTouchTickets(lont, high_touch_customers) -> list:
    """
    Produces a list of tickets from high touch customers.
    """

    logger = logging.getLogger('retHighTouchTickets: ')
    logger.info('Filtering for high-touch customers.')

    filtered_list_of_tickets = []
    for ticket in lont:
        if ticket['org_name'] in high_touch_customers:
            logger.info(f"High-touch customer {ticket['org_name']} found.")
            logger.info(f"Adding High-touch customer {ticket['org_name']} to filtered list.")
            filtered_list_of_tickets.append(ticket)
            logger.debug(f"High-touch customer {ticket['org_name']} added to filtered list.")
    if filtered_list_of_tickets:
        logger.info(f"Produced filtered ticket list {filtered_list_of_tickets}.")
        return filtered_list_of_tickets
    logger.info('Ticket filtering high-touch customers completed.')
