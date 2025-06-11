from ekran import Ekran, Pilka, Odbijak
from drawille import Turtle, Canvas
from pynput.keyboard import Key, KeyCode, Listener
import time



class Rozgrywka:
    def __init__(self, rozgrywka):
        self.rozgrywka = rozgrywka
        self.ekran = Ekran(self)
        self.ekran.wyczysc()
        self.wyjsc = False
        self.fps = 5
        self.zmiana_x = 2
        self.zmiana_y = 0
        self.pilka_x_poprzednia = 40
        self.pilka_y_poprzednia = 26
        self.ruch_gracz2 = 0
        self.ruch_gracz1 = 0
        self.czy_ruch_gora = False
        self.czy_ruch_dol = False
        self.czy_ruch_prawo = False
        self.czy_ruch_prosto = True

    def start(self):
        while True and self.wyjsc == False:
            time.sleep(1/self.fps)
            self.ekran.start()

    

    