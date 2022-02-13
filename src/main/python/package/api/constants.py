import os
from pathlib import Path

DIR_LIST = os.path.join(Path.home(),  ".liste_courses/liste.json")
PAST_LIST = os.path.join(Path.home(), ".liste_courses/past_list.json")

ALREADY_IN_LIST = -1
EQUIV_IN_LIST = 0
NOT_SAVED_IN_PAST = -1
