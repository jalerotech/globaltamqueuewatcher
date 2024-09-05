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
        file_name = file_name_input.split("/")[1]
        if isFileEmpty(file_name):
            logger.info(f"File {file_name} is empty so no need to clean it up. \n ")
            return False
        else:
            logger.info(f"Opening file {file_name} to start the cleanup process")
            with open(file_name_input, 'w') as json_file:
                logger.info(f"{file_name} opened")
                logger.info(f'Cleaning up {file_name} file')
                json_file.close()
                logger.info(f'{file_name} file cleaned \n ')
                return True
    else:
        file_name_list = ['stats.json', 'parentMsgIds.json']
        for file_name in file_name_list:
            if isFileEmpty(file_name):
                logger.info(f"File {file_name} is empty so no need to clean it up. \n ")
            else:
                logger.info(f"Opening file {file_name} to start the cleanup process")
                file_path = f"Files/{file_name}"
                with open(file_path, 'w') as json_file:
                    logger.info(f"{file_name} opened")
                    logger.info(f'Cleaning up {file_name} file')
                    json_file.close()
                    logger.info(f'{file_name} file cleaned \n ')


def isFileEmpty(file):
    """
    Checks if the input file is empty or not.
    If empty, it returns True otherwise returns False
    """
    file_path = f"Files/{file}"
    interesting_file_path = file_path
    # reminder_data.json and parentMsgIds.json are in format where the data are written one line at a time. So the json decoding of this should be treated differently.
    if file == 'reminder_data.json' or file == 'parentMsgIds.json' or file == "weeklyStats.json":
        logger.info(f"Cleaning json files with contents written one line at a time.")
        try:
            logger.info(f"Checking if '{interesting_file_path.split('/')[1]}' is empty or not")
            logger.info(f"Opening file '{interesting_file_path.split('/')[1]}'")
            with open(interesting_file_path, 'r') as file_opened:
                logger.info(f"File '{interesting_file_path.split('/')[1]}' opened")
                for line in file_opened:
                    data = json.loads(line)
                    if data:
                        logger.info(f"File '{interesting_file_path.split('/')[1]}' is not empty, the first line of its content is {data}")
                        return False
                else:
                    # logger.info(f"File {interesting_file_path.split('/')[1]} is empty, so no cleanup needed.")
                    return True
        except json.JSONDecodeError as e:
            logger.info(f"File '{interesting_file_path.split('/')[1]}' is empty, so no cleanup needed -> error raised {e.args}")
            return True
    else:
        # Stats.json and tamPTOStatus.json are list of dict to needs to be read differently from the reminder_data and parentMsgIds files.
        logger.info(f"Checking if '{interesting_file_path.split('/')[1]}' is empty or not")
        logger.info(f"Opening file '{interesting_file_path.split('/')[1]}'")
        with open(interesting_file_path, 'r') as file_opened:
            logger.info(f"File '{interesting_file_path.split('/')[1]}' opened")
            json_data = file_opened.read()  # Read the entire content of the file
            try:
                data = json.loads(json_data)
                if data:
                    logger.info(
                        f"File '{interesting_file_path.split('/')[1]}' is not empty, the first line of its content is {data}")
                    return False
                else:
                    # logger.info(f"File {interesting_file_path.split('/')[1]} is empty, so no cleanup needed.")
                    return True
            except json.JSONDecodeError as e:
                logger.info(f"Failed to read json file due to error -> {e.args}, likely meaning that the json file is empty.")
                return True


def check_file_path(file_path):
    # Redundant function.
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
    # file = 'Files/reminder_data.json'
    file = None
    cleanJsonFiles(file)
    # fp = 'Files/reminder_data.json'
    # isFileEmpty(fp)

