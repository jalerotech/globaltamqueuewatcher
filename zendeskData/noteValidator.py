import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Zendesk Notes Validator')


def isNoteViable(note) -> bool:
    # Strip leading and trailing whitespaces from the input string
    stripped_string = note.strip()
    # Check if the stripped string starts with "PRIMARY_TAM"
    return stripped_string.startswith("PRIMARY_TAM")

