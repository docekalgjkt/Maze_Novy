#DAO interface
from abc import ABC, abstractmethod

from Bludistě import Bludiste


class BludisteDAO(ABC):
    @abstractmethod
    def nacti_bludiste(self):
        pass

    @abstractmethod
    def uloz_bludiste(self, bludiste):
        pass
#DAO pro textový soubor
class TextFileBludisteDAO(BludisteDAO):
    def __init__(self, soubor):
        self.soubor = soubor

    def nacti_bludiste(self):
        with open(self.soubor, 'r') as f:
            data = f.readlines()
            sirka, vyska = map(int, data[0].split())
            bludiste = Bludiste(sirka, vyska)
            for y in range(vyska):
                radek = data[y + 1].strip()
                for x in range(sirka):
                    bludiste.bludiste[y][x] = int(radek[x])
            return bludiste

    def uloz_bludiste(self, bludiste):
        with open(self.soubor, 'w') as f:
            sirka, vyska = bludiste.getRozmery()
            f.write(f"{sirka} {vyska}\n")
            for radek in bludiste.bludiste:
                f.write("".join(map(str, radek)) + "\n")
#DAO pro XML soubor
import xml.etree.ElementTree as ET

class XMLBludisteDAO(BludisteDAO):
    def __init__(self, soubor):
        self.soubor = soubor

    def nacti_bludiste(self):
        strom = ET.parse(self.soubor)
        koren = strom.getroot()
        sirka = int(koren.find('sirka').text)
        vyska = int(koren.find('vyska').text)
        bludiste = Bludiste(sirka, vyska)

        for y, radek in enumerate(koren.find('data').text.splitlines()):
            for x, hodnota in enumerate(radek.strip()):
                bludiste.bludiste[y][x] = int(hodnota)
        return bludiste

    def uloz_bludiste(self, bludiste):
        koren = ET.Element("bludiste")
        sirka_elem = ET.SubElement(koren, "sirka")
        sirka_elem.text = str(bludiste.getSirka())
        vyska_elem = ET.SubElement(koren, "vyska")
        vyska_elem.text = str(bludiste.getVyska())

        data_elem = ET.SubElement(koren, "data")
        data_elem.text = "\n".join("".join(map(str, radek)) for radek in bludiste.bludiste)

        strom = ET.ElementTree(koren)
        strom.write(self.soubor)
#Úprava třídy BludisteApp pro použití DAO
class BludisteApp:
    def __init__(self, root, dao):
        self.root = root
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.dao = dao
        self.bludiste = self.dao.nacti_bludiste()  # Načítáme bludiště z DAO
        self.view = BludisteView(self.bludiste, self.canvas)

        self.view.vykresli()

    def uloz_bludiste(self):
        self.dao.uloz_bludiste(self.bludiste)  # Uloží bludiště pomocí DAO
#Hlavní program s výběrem DAO
if __name__ == "__main__":
    root = tk.Tk()

    # Použití DAO pro textový soubor
    text_dao = TextFileBludisteDAO('bludiste.txt')

    # Použití DAO pro XML soubor
    xml_dao = XMLBludisteDAO('bludiste.xml')

    # Vytvoření aplikace s textovým DAO
    app = BludisteApp(root, text_dao)

    # Možnost uložit bludiště
    app.uloz_bludiste()

    root.mainloop()
