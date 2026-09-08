from os import path


PATH_SOURCE = path.dirname(path.abspath(__file__))
BASE_DIR  = path.dirname(PATH_SOURCE)
NXT_DIR = path.dirname(BASE_DIR )

PATH_DANCES = path.join(BASE_DIR,"dances")
PATH_MUSICS = path.join(BASE_DIR,"musics")
PATH_TEMPLATES = path.join(PATH_SOURCE,'templates')

NBC_PATH = path.join(
    path.dirname(BASE_DIR),
    "nbc-compiler",
    "NXT",
    "nbc"
)