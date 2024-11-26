import tkinter as tk
import random


class Robot:
    def __init__(self, bludiste):
        self.bludiste = bludiste
        self.x = 0
        self.y = 0
        self.cesta = [(0, 0)]  # Uchovává cestu, kterou robot prošel

    def pohni_se(self):
        """Robot se pokusí pohnout do náhodného dostupného směru."""
        moznosti = self._moznosti()
        if moznosti:
            self.x, self.y = random.choice(moznosti)
            self.cesta.append((self.x, self.y))

    def _moznosti(self):
        """Vrací seznam možných sousedních polí, kam se může robot pohnout."""
        moznosti = []
        if self.x > 0 and self.bludiste.jeVolno(self.x - 1, self.y):
            moznosti.append((self.x - 1, self.y))
        if self.x < self.bludiste.getSirka() - 1 and self.bludiste.jeVolno(self.x + 1, self.y):
            moznosti.append((self.x + 1, self.y))
        if self.y > 0 and self.bludiste.jeVolno(self.x, self.y - 1):
            moznosti.append((self.x, self.y - 1))
        if self.y < self.bludiste.getVyska() - 1 and self.bludiste.jeVolno(self.x, self.y + 1):
            moznosti.append((self.x, self.y + 1))
        return moznosti

    def je_u_cile(self):
        """Kontroluje, zda robot dosáhl cíle."""
        return self.bludiste.jeVychod(self.x, self.y)


class RobotView:
    def __init__(self, robot, canvas):
        self.robot = robot
        self.canvas = canvas
        self.velikost_ctverecku = 20
        self.sprite = None

    def vykresli(self):
        """Vykreslí robota na aktuální pozici."""
        if self.sprite:
            self.canvas.delete(self.sprite)
        self.sprite = self.canvas.create_oval(
            self.robot.x * self.velikost_ctverecku + 5,
            self.robot.y * self.velikost_ctverecku + 5,
            (self.robot.x + 1) * self.velikost_ctverecku - 5,
            (self.robot.y + 1) * self.velikost_ctverecku - 5,
            fill="red"
        )


class BludisteApp:
    def __init__(self, root):
        self.root = root
        self.running = False

        # Nastavení okna a plátna
        self.canvas = tk.Canvas(self.root, width=420, height=420)
        self.canvas.grid(row=0, column=0, columnspan=3)

        # Vytvoření bludiště a zobrazení
        self.bludiste = Bludiste(21, 21)
        self.view = BludisteView(self.bludiste, self.canvas)
        self.view.vykresli()

        # Vytvoření robota a jeho zobrazení
        self.robot = Robot(self.bludiste)
        self.robot_view = RobotView(self.robot, self.canvas)
        self.robot_view.vykresli()

        # Tlačítka pro ovládání
        self.btn_start = tk.Button(self.root, text="Start", command=self.start)
        self.btn_start.grid(row=1, column=0)

        self.btn_stop = tk.Button(self.root, text="Stop", command=self.stop)
        self.btn_stop.grid(row=1, column=1)

        self.btn_reset = tk.Button(self.root, text="Reset", command=self.reset)
        self.btn_reset.grid(row=1, column=2)

    def start(self):
        """Spustí pohyb robota."""
        if not self.running:
            self.running = True
            self.update()

    def stop(self):
        """Zastaví pohyb robota."""
        self.running = False

    def reset(self):
        """Resetuje bludiště a robota."""
        self.running = False
        self.bludiste = Bludiste(21, 21)
        self.view = BludisteView(self.bludiste, self.canvas)
        self.view.vykresli()
        self.robot = Robot(self.bludiste)
        self.robot_view = RobotView(self.robot, self.canvas)
        self.robot_view.vykresli()

    def update(self):
        """Aktualizuje pozici robota a vykreslí změny."""
        if self.running:
            if not self.robot.je_u_cile():
                self.robot.pohni_se()
                self.robot_view.vykresli()
                self.root.after(200, self.update)
            else:
                self.running = False
                print("Robot dosáhl cíle!")


# Hlavní program
if __name__ == "__main__":
    root = tk.Tk()
    app = BludisteApp(root)
    root.mainloop()
