import os
import re

from package.api.sub import *

if __name__ == '__main__':
    actions = {"N": ["Ajouter un [N]ouvel article", add_article],
               "S": ["[S]upprimer un article", remove_article],
               "A": ["[A]fficher la liste", show_list],
               "Q": ["[Q]uitter", exit]
               }
    keys = list()
    keys_str = ""
    for key in actions.keys():
        keys.append(key)
        keys_str += key + "/"
    keys_str = keys_str[:-1]

    while True:
        print()
        for key, val in actions.items():
            print(val[0])
        # TODO: change for raw keyboard input
        choix = input("Choix [" + keys_str + "] : ").upper()

        if not choix in keys:
            print("Choix incorrect")
            continue

        actions[choix][1]()

    os.system('clear')

