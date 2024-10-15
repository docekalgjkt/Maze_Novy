import tkinter as tk
import random


class Bludiste:
    def __init__(self, sirka, vyska):
        self.sirka = sirka
        self.vyska = vyska
        self.bludiste = [[random.choice([0, 1]) for _ in range(sirka)] for _ in range(vyska)]
        self.bludiste[0][0] = 0  # Startovní pozice je volná
        self.bludiste[vyska - 1][sirka - 1] = 0  # Východ je volný

    def jeVolno(self, x, y):
        return self.bludiste[y][x] == 0

    def getSirka(self):
        return self.sirka

    def getVyska(self):
        return self.vyska

    def getRozmery(self):
        return self.sirka, self.vyska

    def jeVychod(self, x, y):
        return x == self.sirka - 1 and y == self.vyska - 1


class BludisteView:
    def __init__(self, bludiste, canvas):
        self.bludiste = bludiste
        self.canvas = canvas
        self.velikost_ctverecku = 10

    def vykresli(self):
        self.canvas.delete("all")
        for y in range(self.bludiste.getVyska()):
            for x in range(self.bludiste.getSirka()):
                barva = "white" if self.bludiste.jeVolno(x, y) else "black"
                self.canvas.create_rectangle(
                    x * self.velikost_ctverecku,
                    y * self.velikost_ctverecku,
                    (x + 1) * self.velikost_ctverecku,
                    (y + 1) * self.velikost_ctverecku,
                    fill=barva
                )

    def setCanvas(self, canvas):
        self.canvas = canvas


class BludisteApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.bludiste = Bludiste(20, 20)
        self.view = BludisteView(self.bludiste, self.canvas)

        self.view.vykresli()


# Hlavní program
if __name__ == "__main__":
    root = tk.Tk()
    app = BludisteApp(root)
    root.mainloop()
