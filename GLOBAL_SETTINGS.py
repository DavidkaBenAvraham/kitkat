from pathlib import Path
import datetime , time
from script_logger import logger
from strings_formatter import StringFormatter as SF
import execute_json as json


def get_now(strformat : str = '%m%d%H%M%S') -> datetime :
        ##штамп текущего времени
        #------------------
        # @param strformat : в каком формате вернуть штамп (by default : %m%d%H%M%S)
        return  datetime.datetime.now().strftime(strformat)

ROOT_DIRECTORY = Path.cwd().absolute()
_ = Path(ROOT_DIRECTORY,'launcher.json').absolute()
LAUNCHER_SETTINGS = json.loads(_)
_paths = LAUNCHER_SETTINGS['program_paths']

_ = Path
SCENARIES_DIRECTORY = Path(ROOT_DIRECTORY,_paths['scenaries_dir']).absolute()
INI_DIRECTORY = Path(ROOT_DIRECTORY,_paths['ini_files_dir']).absolute()
EXPORT_DIRECTORY = Path(ROOT_DIRECTORY.parent,_paths['export_dir']).absolute()
COOKIES_DIRECTORY:Path = Path(ROOT_DIRECTORY,_paths['cookies_dir']).absolute()
COOKIES_FILE = None
LOG_DIRECTORY = Path(ROOT_DIRECTORY.parent,_paths['export_dir']).absolute()
API_DIRECTORY:Path = None
BINARY_FILES_DIRECTORY = Path(ROOT_DIRECTORY,_paths['binary_files_dir']).absolute()
START_TIME = get_now()

SUPPLIERS_LIST_FOR_SCRAPPING: list = LAUNCHER_SETTINGS['suppliers']


categories_excluded_from_keywords_path = Path(INI_DIRECTORY,'categories_excluded_from_keywords.json').absolute()
CATEGORIES_EXCLUDED_FROM_METAWORDS: dict = json.loads(categories_excluded_from_keywords_path)



THREADS: bool = LAUNCHER_SETTINGS['threads']

NUM_OF_IMAGES_TO_BE_SAVED = 3