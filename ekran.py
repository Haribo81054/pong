from __future__ import print_function
import sys, os, shutil
from collections import namedtuple
from drawille import *
from pynput.keyboard import Key, KeyCode, Listener
import random
import time

RozmiarEkranu = namedtuple('RozmiarEkranu', ['w', 'h'])
t = Turtle()
c = Canvas()

pilka_x = 40 #kolumna
pilka_y = 26 #wiersz
#czy_ruch_prawo = True
#czy_ruch_gora = True
#czy_ruch_dol = False
#czy_ruch_prosto = False


class Pilka():
    def __init__(self):
        pass
        #self.czy_ruch_prawo = False
        #self.czy_ruch_gora = True
        #self.czy_ruch_prosto = False
    
    def narysuj_pilka(self, pilka_x, pilka_y):
        c.set_text(pilka_x-self.rozgrywka.zmiana_x, pilka_y+self.rozgrywka.zmiana_y, '0')
        c.set_text(self.rozgrywka.pilka_x_poprzednia, self.rozgrywka.pilka_y_poprzednia, ' ')


    def ruch(self, pilka_x, pilka_y):
        if self.rozgrywka.czy_ruch_prawo and pilka_x-self.rozgrywka.zmiana_x <= 76:
            self.rozgrywka.zmiana_x -= 2
            self.rozgrywka.pilka_x_poprzednia = pilka_x - self.rozgrywka.zmiana_x -2
        
        if not(self.rozgrywka.czy_ruch_prawo) and pilka_x-self.rozgrywka.zmiana_x >= 4:
            self.rozgrywka.zmiana_x += 2
            self.rozgrywka.pilka_x_poprzednia = pilka_x - self.rozgrywka.zmiana_x +2
       
        if self.rozgrywka.czy_ruch_gora: #do gory
            self.rozgrywka.zmiana_y -= 4
            self.rozgrywka.pilka_y_poprzednia = pilka_y + self.rozgrywka.zmiana_y +4

        if self.rozgrywka.czy_ruch_dol: #do dolu
            self.rozgrywka.zmiana_y += 4
            self.rozgrywka.pilka_y_poprzednia = pilka_y + self.rozgrywka.zmiana_y -4

    def odbicie_od_sciany(self, pilka_y):
        
        if pilka_y+self.rozgrywka.zmiana_y == 6: #gora
            self.rozgrywka.czy_ruch_gora = False
            self.rozgrywka.czy_ruch_dol = True
            self.rozgrywka.czy_ruch_prosto = False

        if pilka_y+self.rozgrywka.zmiana_y == 46: #dol
            self.rozgrywka.czy_ruch_gora = True
            self.rozgrywka.czy_ruch_dol = False
            self.rozgrywka.czy_ruch_prosto = False


class Odbijak():

    def narysuj_odbijak_gracz1(self, ruch):
        c.set_text(4, 24+ruch, '{')
        if 24+4+ruch < 48:
            c.set_text(4, 24+4+ruch, ' ')

        if 24-4+ruch > 0:
            c.set_text(4, 24-4+ruch, ' ')

    
    def narysuj_odbijak_gracz2(self, ruch):
        c.set_text(76, 24+ruch, '}')
        if 24+4+ruch < 48:
            c.set_text(76, 24+4+ruch, ' ')

        if 24-4+ruch > 0:
            c.set_text(76, 24-4+ruch, ' ')
    
    def odbicie_od_odbijaka(self, pilka_x, pilka_y, ruch_gracz1, ruch_gracz2):
        tmp = random.randint(1, 2)
        #print(24+self.rozgrywka.ruch_gracz2, '   ', pilka_y+self.rozgrywka.zmiana_y-2, '   ', pilka_x-self.rozgrywka.zmiana_x)
        if 24+ruch_gracz1 == pilka_y+self.rozgrywka.zmiana_y-2 and pilka_x-self.rozgrywka.zmiana_x == 6: #lewa strona
            self.rozgrywka.czy_ruch_prawo = True
            if tmp == 1:
                self.rozgrywka.czy_ruch_gora = False
                self.rozgrywka.czy_ruch_dol = True
            elif tmp == 2:
                self.rozgrywka.czy_ruch_gora = True
                self.rozgrywka.czy_ruch_dol = False
        elif 24+ruch_gracz2 == pilka_y+self.rozgrywka.zmiana_y-2 and pilka_x-self.rozgrywka.zmiana_x == 74: #prawa strona
            self.rozgrywka.czy_ruch_prawo = False
            if tmp == 1:
                self.rozgrywka.czy_ruch_gora = False
                self.rozgrywka.czy_ruch_dol = True
            elif tmp == 2:
                self.rozgrywka.czy_ruch_gora = True
                self.rozgrywka.czy_ruch_dol = False
        

class Ekran(Odbijak, Pilka):

    def __init__(self, rozgrywka):
        self.wyjsc = False
        self.rozgrywka = rozgrywka
        self.pkt_gracz1 = 0
        self.pkt_gracz2 = 0


    def start(self):
        self.odswiez()
        with Listener(on_press = self.on_press) as listener:
            listener.join()


    def wyczysc(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def zliczanie_pkt(self, pilka_x, pilka_y, ruch_gracz1, ruch_gracz2):
        if pilka_x-self.rozgrywka.zmiana_x == 4 and 24+ruch_gracz1 != pilka_y:
            self.pkt_gracz2 += 1
            self.reset(ruch_gracz1, ruch_gracz2)
        elif pilka_x-self.rozgrywka.zmiana_x == 76 and 24+ruch_gracz2 != pilka_y:
            self.pkt_gracz1 += 1
            self.reset(ruch_gracz1, ruch_gracz2)

    def plansza(self):
        self.odbicie_od_sciany(pilka_y)
    
        self.ruch(pilka_x, pilka_y)
        self.narysuj_pilka(pilka_x, pilka_y)

        self.zliczanie_pkt(pilka_x, pilka_y, self.rozgrywka.ruch_gracz1, self.rozgrywka.ruch_gracz2)
        for i in range(80):
            c.set(1+i, 1)
            c.set(1+i, 50)
        
        for i in range(50):
            c.set(1, 1+i)
            c.set(80, 1+i)
        
        self.narysuj_odbijak_gracz1(self.rozgrywka.ruch_gracz1)
        self.narysuj_odbijak_gracz2(self.rozgrywka.ruch_gracz2)
        self.odbicie_od_odbijaka(pilka_x, pilka_y, self.rozgrywka.ruch_gracz1, self.rozgrywka.ruch_gracz2)
        
        self.tabela_wynikow()
        print(c.frame())
        

        

    def tabela_wynikow(self):
        print("Gracz 1", ' '*24, "Gracz 2")
        print("PKT: " +str(self.pkt_gracz1), ' '*26, "PKT: " +str(self.pkt_gracz2))
        #print(24+self.rozgrywka.ruch_gracz2, '   ', pilka_y+self.rozgrywka.zmiana_y-2, '   ', pilka_x-self.rozgrywka.zmiana_x)
        #print(24+self.rozgrywka.ruch_gracz1, '    ',pilka_y-2)

    def wygrana(self):
        if self.pkt_gracz1 == 3:
            print('Wygrywa gracz 1!')
            time.sleep(3)
            self.wyjsc = True
        elif self.pkt_gracz2 == 3:
            print('Wygrywa gracz 2!')
            time.sleep(3)
            self.wyjsc = True


    
    def odswiez(self):
        self.wyczysc()
        self.wygrana()
        self.plansza()

    def reset(self, ruch_gracz1, ruch_gracz2):
        c.set_text(4, 24+ruch_gracz1, ' ')
        c.set_text(76, 24+ruch_gracz2, ' ')
        self.rozgrywka.zmiana_x = 2
        self.rozgrywka.zmiana_y = 0
        self.rozgrywka.ruch_gracz1 = 0
        self.rozgrywka.ruch_gracz2 = 0
        czy_ruch_prawo = False
        czy_ruch_gora = False
        czy_ruch_prosto = True

    
    def on_press(self, key):
        

        if key == Key.end:
            self.wyjsc = True
        elif key == Key.up:
            if 24-4+self.rozgrywka.ruch_gracz2 > 0:
                self.rozgrywka.ruch_gracz2 -= 4
        elif key == Key.down:
            if self.rozgrywka.ruch_gracz2+4+24 < 48:
                self.rozgrywka.ruch_gracz2 += 4
        elif key == (KeyCode.from_char('w') or KeyCode.from_char('W')):
            if 24-4+self.rozgrywka.ruch_gracz1 > 0:
                self.rozgrywka.ruch_gracz1 -= 4
        elif key == (KeyCode.from_char('s') or KeyCode.from_char('S')):
            if self.rozgrywka.ruch_gracz1+4+24 < 48:
                self.rozgrywka.ruch_gracz1 += 4
        
        self.odswiez()
        
        
        if self.wyjsc:
            self.wyczysc()
            self.rozgrywka.wyjsc = True
            return False


