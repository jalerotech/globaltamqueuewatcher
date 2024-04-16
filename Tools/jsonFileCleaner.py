import json
import logging


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger("Cleaning Json Files")


def cleanJsonFiles(file_name_input) -> bool:
    logger.info("Running File Cleanup.")
    """
    DOCSTRING HERE
    """
    if file_name_input:
        if isFileEmpty(file_name_input):
            return False
        else:
            file_name = file_name_input.split("/")[1]
            logger.info(f"Opening file {file_name}")
            with open(file_name_input, 'w') as json_file:
                logger.info(f"{file_name} opened")
                logger.info(f'Cleaning up {file_name} file')
                json_file.close()
                logger.info(f'{file_name} file cleaned \n ')
                return True
    else:
        file_name_list = ['stats.json']
        if isFileEmpty(file_name_input):
            logger.info(f"File {file_name_list[0]} is empty so no need to clean it up.")
            return False
        else:
            for file_name in file_name_list:
                logger.info(f"Opening file {file_name}")
                file_path = f"Files/{file_name}"
                with open(file_path, 'w') as json_file:
                    logger.info(f"{file_name} opened")
                    logger.info(f'Cleaning up {file_name} file')
                    json_file.close()
                    logger.info(f'{file_name} file cleaned \n ')
                    return True


def isFileEmpty(file_path):
    """
    Checks if the input file is empty or not.
    If empty, it returns True otherwise returns False
    """
    interesting_file_path = check_file_path(file_path)
    try:
        logger.info(f"Opening file '{interesting_file_path.split('/')[1]}'")
        with open(interesting_file_path, 'r') as file_opened:
            logger.info(f"File '{interesting_file_path.split('/')[1]}' opened ")
            for line in file_opened:
                data = json.loads(line)
                if data:
                    logger.info(f"File '{interesting_file_path.split('/')[1]}' is not empty, the first line of its content is {data}")
                    return False
            else:
                logger.info(f"File {interesting_file_path.split('/')[1]} is empty.")
    except json.JSONDecodeError:
        logger.info(f"File '{interesting_file_path.split('/')[1]}' is empty, so no cleanup needed")
        return True


def check_file_path(file_path):
    """
    Checks the file paths and returns the file path string depending on the file_path input provided.
    None input means that the file path to return is the hardcoded one, in this case stats.json file.
    """
    if file_path is None:
        interesting_file_path = "Files/stats.json"
        logger.info(f"Checking if '{interesting_file_path.split('/')[1]}' is empty or not")
        return interesting_file_path
    else:
        logger.info(f"Checking if '{file_path.split('/')[1]}' is empty or not")
        return file_path


if __name__ == '__main__':
    # file = None
    # cleanJsonFiles(file)
    fp = 'Files/reminder_data.json'
    isFileEmpty(fp)

