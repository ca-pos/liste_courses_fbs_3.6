import re
import tinydb.table
from tinydb import TinyDB, where, Query

from package.api.constants import DIR_LIST, PAST_LIST


class Produit:
    db_list = TinyDB(DIR_LIST, indent=4, ensure_ascii=False)
    db_past = TinyDB(PAST_LIST, indent=4, ensure_ascii=False)

    def __init__(self, item: str, magasin: str = "", rayon: str = "") -> None:
        self.item = self._normalize(item)
        self.magasin = self._normalize(magasin)
        self.rayon = self._normalize(rayon)

    def _normalize(self, regex):
        regex = re.sub(r"^(\s*\b)((\w* *\b)+)(\ *)$", r"\2", regex, re.LOCALE)
        regex = re.sub(r"(\s+)", r" ", regex, re.LOCALE)
        return regex.lower()

    def __str__(self) -> str:
        return f"{self.item}, {self.magasin}, {self.rayon}"

    def __repr__(self) -> str:
        return f"Produit({self.item})"

    # GETTERS & SETTERS

    @property
    def item(self) -> str:
        return self._item

    @item.setter
    def item(self, value: str):
        self._item = value

    @property
    def magasin(self) -> str:
        return self._magasin

    @magasin.setter
    def magasin(self, value: str):
        self._magasin = value

    @property
    def rayon(self) -> str:
        return self._rayon

    @rayon.setter
    def rayon(self, value: str):
        self._rayon = value

    # OBJECT METHODS

    @property
    def db_exact_instance(self):
        """
        Return the object whose items match those of  self.item

        Returns: tinydb_list.table.Document
        """
        return (Produit.db_list.get((where("item") == self.item) &
                                   (where("magasin") == self.magasin) &
                                   (where("rayon") == self.rayon)))

    @property
    def db_instance(self) -> tinydb.table.Document:
        """
        Return the object whose item field equals self.item

        Returns: tinydb_list.table.Document
        """
        return Produit.db_list.get(where("item") == self.item)

    def exists_in_list(self):
        """
        Test if the object whose item field is self.item exists

        Returns: bool: True if object exists, False otherwise
        """
        return bool(self.db_instance)

    def exists_in_past(self) -> bool:
        """
        Test if the object whose item field is self.item exists in the past list

        Returns: bool: True if object exists, False otherwise
        """
        return bool(Produit.db_past.get(where("item") == self.item))

    def save(self) -> int:
        """
        Add the item self in db_list if it is not yet present

        Returns: int: id of the added item, -1 if item already in list
        """
        if self.exists_in_list():
            return -1
        # print(Produit.db_list.insert(self.__dict__))
        # # l'utilisation de __dict__ semble incompatible avec les setters/getters, d'où le recours à tmp ci-dessous
        tmp = {"item": self.item, "magasin": self.magasin, "rayon": self.rayon}
        return Produit.db_list.insert(tmp)

    def supprimer(self):
        """
        If self exists in the db_list, it is deleted

        Returns: list: id of the removed item
        """
        if self.exists_in_list():
            return Produit.db_list.remove(doc_ids=[self.db_exact_instance.doc_id])
        return []


# PRIVATE METHODS


def _get_all_items():
    return [Produit(**produit) for produit in Produit.db_list.all()]

def _get_past_items():
    return [Produit(**p) for p in Produit.db_past.all()]


# CLASS METHODS

def full_list_by_items():
    list_ = list()
    l = liste_items()
    for i in range(len(l)):
        articles = look_for_items(l[i])
        list_.extend(articles)
    return list_

def full_list_by_stores() -> dict:
    list_ = dict()
    look = Query()
    for magasin in liste_magasins():
        tmp_mag = Produit.db_list.search(look.magasin == magasin)
        liste_rayons = sorted(list({tmp_mag[i]['rayon'] for i in range(len(tmp_mag))}))
        list_shelf = dict()
        for rayon in liste_rayons:
            shelf = rayon if rayon else '@'
            articles = Produit.db_list.search((look.magasin == magasin) & (look.rayon == rayon))
            list_items = list()
            for article in articles:
                list_items.append(article['item'])
            list_shelf[shelf] = list_items
        list_[magasin] = list_shelf

    return list_


def liste_items() -> list:
    return sorted(list({item.item for item in _get_all_items()}))

def liste_magasins() -> list:
    return sorted(list({item.magasin for item in _get_all_items()}))


def look_for_items(item: str):
    look = Query()
    return Produit.db_list.search(look.item == item)

# =============================================================================================================================
# =============================================================================================================================


if __name__ == "__main__":
    pass
    full_list_by_items()

    # q = Produit('brosse à dent', 'inter', 'hygiène')
    # q.save()
    # p = Produit('brosse à dents', 'inter', 'hygiène')
    # e = p.db_exact_instance
    # print(e.doc_id if e else "Pas d'article")
    #
    # full_list = full_list()
    # for k1, v1 in full_list.items():
    #     print(k1.upper())
    #     for k2, v2 in v1.items():
    #         if not k2 == '@':
    #             print(" ",k2.title())
    #         for i in range(len(v2)):
    #             print('\t+', v2[i])
    #     print("------------------")

    # croquettes = Produit('croquettes', 'inter', 'animaux')
    # croquettes = Produit('croquettes')

    # print('supprimer', croquettes.supprimer())
    # if not croquettes.exists():
    #     print('save', croquettes.save())

    # from faker import Faker
    # from faker.providers import DynamicProvider
    # rayon_provider = DynamicProvider(
    #     provider_name="rayon",
    #     elements=["légumes", "produits ménagers", "liquides", "vêtements", "hygiène", "animaux", "", "", "", ""]
    # )
    # magasin_provider = DynamicProvider(
    #     provider_name="magasin",
    #     elements=["inter", "superU", "bricomarché", "botanic", "nature & couleurs", "biocoop"]
    # )
    # fake = Faker("fr_FR")
    # fake.add_provider(rayon_provider)
    # fake.add_provider(magasin_provider)
    # for _ in range(3):
    #     produit = Produit(fake.word(), fake.magasin(), fake.rayon())
    #     print(produit.save())
    #     print(produit)
    # print( ">>>", db.search(chercher.magasin == "inter"))
    # liste_triee = list()
    # for tmp in liste_magasins():
    #     liste_triee.extend(db.search(chercher.magasin == tmp))
    # for tmp in liste_triee:
    #     print((tmp))
    # if croquettes.exists():
    #     print('---',  croquettes.db_instance['magasin'])

    # User.DB.get((where('first_name')== self.first_name) & (where('last_name')==self.last_name))
    # for j in range(len(rayons)):
    #     if not rayons[j] == "":
    #         print( "  ", rayons[j].capitalize())
