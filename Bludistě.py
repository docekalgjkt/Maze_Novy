import tkinter as tk
import random


class Bludiste:
    def __init__(self, sirka, vyska):
        self.sirka = sirka
        self.vyska = vyska
        self.bludiste = [[1 for _ in range(sirka)] for _ in range(vyska)]  # 1 = zeď, 0 = volné pole
        self._vygeneruj_cestu()

    def _vygeneruj_cestu(self):
        # Startovní a koncový bod
        start = (0, 0)
        exit = (self.sirka - 1, self.vyska - 1)

        # Nastavení volných polí pro start a exit
        self.bludiste[start[1]][start[0]] = 0
        self.bludiste[exit[1]][exit[0]] = 0

        # Generování náhodné cesty z DFS algoritmu
        stack = [start]
        navstiveno = {start}

        while stack:
            x, y = stack.pop()
            sousedi = self._moznosti(x, y)
            random.shuffle(sousedi)  # Zamíchání sousedů pro náhodnost

            for nx, ny in sousedi:
                if (nx, ny) not in navstiveno:
                    navstiveno.add((nx, ny))
                    self.bludiste[ny][nx] = 0  # Vytvoříme cestu
                    self.bludiste[(y + ny) // 2][(x + nx) // 2] = 0  # Otevření mezi sousedy
                    stack.append((nx, ny))

    def _moznosti(self, x, y):
        moznosti = []
        if x > 1 and self.bludiste[y][x - 2] == 1:
            moznosti.append((x - 2, y))
        if x < self.sirka - 2 and self.bludiste[y][x + 2] == 1:
            moznosti.append((x + 2, y))
        if y > 1 and self.bludiste[y - 2][x] == 1:
            moznosti.append((x, y - 2))
        if y < self.vyska - 2 and self.bludiste[y + 2][x] == 1:
            moznosti.append((x, y + 2))
        return moznosti

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
        self.velikost_ctverecku = 20

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

        self.bludiste = Bludiste(21, 21)  # Liché rozměry zajišťují lepší generování
        self.view = BludisteView(self.bludiste, self.canvas)

        self.view.vykresli()


# Hlavní program
if __name__ == "__main__":
    root = tk.Tk()
    app = BludisteApp(root)
    root.mainloop()
