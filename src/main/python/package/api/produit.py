import tinydb.table
from tinydb import TinyDB, where, Query
from pathlib import Path

# import tinydb
# from tinydb.table import Document

from package.api.constants import DIR


class Produit:
    DB = TinyDB(DIR, indent=4, ensure_ascii=False)

    def __init__(self, item: str, magasin: str = "", rayon: str = "") -> None:
        self.item = item
        self.magasin = magasin
        self.rayon = rayon

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
    def db_instance(self) -> tinydb.table.Document:
        """
        Return the object whose item field equals self.item

        Returns: tinydb.table.Document
        """
        return Produit.DB.get(where('item') == self.item)

    def exists(self):
        """
        Test if the object whose item field is self.item exists

        Returns: bool: True if object exists, False if not

        """
        return bool(self.db_instance)

    def save(self) -> int:
        """
        Add the item self in DB

        Returns: int: id of the added item
        """
        # print(Produit.DB.insert(self.__dict__))
        # # l'utilisation de __dict__ semble incompatible avec les setters/getters, d'où le recours à tmp ci-dessous
        tmp = {"item": self.item, "magasin": self.magasin, "rayon": self.rayon}
        return Produit.DB.insert(tmp)

    def supprimer(self):
        """
        If self exists in the DB, it is deleted

        Returns: list: id of the removed item

        """
        if self.exists():
            return Produit.DB.remove(doc_ids=[self.db_instance.doc_id])
        return []


# PRIVATE METHODS


def _get_all_items():
    return [Produit(**produit) for produit in Produit.DB.all()]


# CLASS METHODS


def full_list()->dict:
    list_ = dict()
    look = Query()
    for magasin in liste_magasins():
        tmp_mag = Produit.DB.search(look.magasin == magasin)
        liste_rayons = sorted(list({tmp_mag[i]['rayon'] for i in range(len(tmp_mag))}))
        list_shelf = dict()
        for rayon in liste_rayons:
            shelf = rayon if rayon else '@'
            articles = Produit.DB.search((look.magasin == magasin) & (look.rayon == rayon))
            list_items = list()
            for article in articles:
                list_items.append(article['item'])
            list_shelf[shelf] = list_items
        list_[magasin] = list_shelf
    return list_


def liste_magasins() -> list:
    return sorted(list({item.magasin for item in _get_all_items()}))

# =============================================================================================================================
# =============================================================================================================================


if __name__ == "__main__":
    full_list = full_list()
    for k1, v1 in full_list.items():
        print(k1.upper())
        for k2, v2 in v1.items():
            if not k2 == '@':
                print(" ",k2.title())
            for i in range(len(v2)):
                print('\t+', v2[i])
        print("------------------")



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



