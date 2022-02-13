import os

from sub import *
from package.api.produit import Produit, liste_magasins

if __name__ == '__main__':
    # TODO:
    #   add action: remove duplicates in past
    #   add action: edit past
    #   add action: edit list
    #   add action:
    actions = {"N": ["Ajouter un [N]ouvel article", add_article],
               "S": ["[S]upprimer un article", remove_article],
               "A": ["[A]fficher la liste", show_list],
               "H": ["Ne pas arc[H]iver", invert_archive_flag],
               "Q": ["[Q]uitter", exit]
               }

    keys = list()
    keys_str = ""
    for key in actions.keys():
        keys.append(key)
        keys_str += key + "/"
    keys_str = keys_str[:-1]
    setattr(invert_archive_flag, 'archive', True)

    while True:
        print()
        for key, val in actions.items():
            print(val[0])
        # TODO: change for raw keyboard input here and elsewhere
        choix = input("Choix [" + keys_str + "] : ").upper()

        if not choix in keys:
            print("Choix incorrect")
            continue

        res = actions[choix][1]()
    os.system('clear')

# TODO: add cleaning/editing functionalities for list and past list

    # a = Produit("jouets", "zeeman")
    # b = Produit("blaireau", "inter", "hygiène")
    # c = Produit("yaourt", "biocoop", "")
    # e = Produit("jouets", "Joué Club", "", save_in_past=False)
    # f = Produit("brosse à dents", "inter", "hygiène")
    # g = Produit("lames rasoir", "inter", "hygiène")
    # h = Produit("piles", "bricomarché", "électricité")
    #
    #
    #
    # # r = a.db_exact_instance
    # # print( "ok" if r else "non")
    # #
    # # print( b.is_same(b))
    # # print(liste_magasins())
    # # exit()
    # print(g.save())
    #

