from tinydb import Query

from package.api.produit import Produit, full_list_by_stores
from package.api.produit import full_list_by_items, look_for_items

class bcolors:
    # TODO: does not work with windows, see colorama extension
    # TODO: move this to an utilities module
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR


#         FONCTIONS PUBLIQUES


def add_article():
    item = input("Article : ")
    article = _get_article(item)

    print(article.save())


def remove_article():
    l = full_list_by_items()
    for i in range(len(l)):
        a = l[i]
        num = '{}{:3d}{}'.format(bcolors.FAIL, i+1, bcolors.RESET)
        print(num, '-> ', end="")
        print(bcolors.WARNING + a['item'] + bcolors.RESET +
              ":" +
              a['magasin'].upper()
              )
    while True:
        choix = input("Numéro de l'article à supprimer : ")
        try:
            choix = int(choix) - 1
        except ValueError:
            if choix == "":
                return -1
            print(bcolors.FAIL, 'Entrez un nombre', bcolors.RESET)
            continue
        if not (choix in range(len(l))):
            print(bcolors.FAIL, "Choix incorrect", bcolors.RESET)
            continue
        a = l[choix]
        return (Produit(**a)).supprimer()


def show_list():
    list_ = full_list_by_stores()
    for key1, val1 in list_.items():
        print(bcolors.FAIL, key1.upper(), bcolors.RESET)
        for key2, val2 in val1.items():
            if not key2 == "@":
                print(" ", key2.title())
            for i in range(len(val2)):
                print('\t+', bcolors.WARNING, val2[i], bcolors.RESET)
        print()
    print(invert_archive_flag.archive)

def invert_archive_flag():
    invert_archive_flag.archive = not invert_archive_flag.archive
    print()
    if(invert_archive_flag.archive):
        print(bcolors.WARNING, "Les nouveaux articles seront archivés", bcolors.RESET)
    else:
        print(bcolors.WARNING, "Les nouveaux articles ne seront plus archivés", bcolors.RESET)


#         FONCTIONS PRIVÉES


def _flat_list():
    list_ = full_list_by_items()
    res = []
    j = 0
    for key1, val1 in list_.items():
        for key2, val2 in val1.items():
            shelf = "" if key2 == "@" else key2
            for i in range(len(val2)):
                res.append([val2[i], key1.upper(), shelf.title()])
                print(j+1, val2[i] + ":" + key1.upper() + ":" + shelf.title())
                j += 1

    return res


def _get_article(item: str):
    article = Produit(item)
    if article.exists_in_list(False):
        look_for_items(item=item, in_list=False)
        # look_for_items(item=item, in_list=False)
        store = _proposals(articles, 'magasin')
        shelf = _proposals(articles, 'rayon')
    else:
        store = input('Magasin : ')
        shelf = input('Rayon : ')

    save = invert_archive_flag.archive
    article = Produit(item=item, magasin=store, rayon=shelf, save_in_past=save)

    if article.db_exact_instance():
        article = Produit("")

    return article


def _proposals(articles: Produit, param: str):
    lg = len(articles)
    for i in range(lg):
        old = articles[i][param]
        new = input(f"{param.capitalize()} [{old}] : ")
        if new:
            if new == "+":
                return old
            else:
                return "" if new == "*" else new
            # break
        if i+1 == lg:
            return ""


