import csv
import os


# FORMAT (met index):
# ID(0);Naam kort;Naam lang;Prijs;Muntwaarde;BTW id;
# Actief(6);Keuken;Bar;Minimumleeftijd;Categorie(10);Hoofdproduct(11);Hardloper;Kleur;EAN Code;Open prijs;Theoretische
# brutowinstmarge(16);Winstmarge o.b.v. inkoopprijzen


def productenDict():
    with open(os.path.dirname(os.path.realpath(__file__)) + "/data/producten.csv") as csvDataFile:
        producten = csv.reader(csvDataFile, delimiter=";")

        # skip header
        next(producten)
        productCatDict = {}
        for product in producten:
            if "Bier" in product[11]:
                productCategorie = "Bier"
            elif "Wijn" in product[11]:
                productCategorie = "Wijn"
            elif "Fris" in product[11]:
                productCategorie = "Fris"
            elif "Snacks" in product[11]:
                productCategorie = "Snacks"
            else:
                productCategorie = "Overig"

            # map ID to productCategorie
            productCatDict[product[0]] = productCategorie

    return productCatDict
