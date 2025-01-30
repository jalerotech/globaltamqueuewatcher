import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def stringFromList(source_list) -> str:
    """
    Create stringed using the list provided.
    Used to create the messages being sent to WxT as notification.
    """
    logger = logging.getLogger('stringFromList: ')
    logger.info(f'Generating string from list of items in received list -> {source_list}')
    stringListSource = []
    for item in source_list:
        stringListSource.append(item['name'])
    if stringListSource:
        string_list = ', '.join(stringListSource)
        logger.info(f"Result of generating string from dict list ->  {string_list}.")
        return string_list
