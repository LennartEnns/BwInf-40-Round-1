import numpy as np
import os
import random
import codecs
from string import ascii_uppercase
alphabet = list(ascii_uppercase)+["Ä", "Ö", "Ü"]

def abfrage_zahl(frage, fehler, fehler_antwort):
    while True:
        try:
            ausgabe = int(input(frage))
            if eval(fehler):
                raise Exception
            break
        except:
            print(fehler_antwort+"\n")
    return ausgabe

leer = "."
n_Dateien = len(os.listdir("Beispieldateien"))
datei_nummer = abfrage_zahl("Welche Textdatei soll verwendet werden? ", "not ausgabe in range(0, n_Dateien)",
                            "Bitte gebe eine Zahl von 0 bis "+str(n_Dateien-1)+" ein.")

print("\nSchwierigkeitsgrade:")
print("Stufe 1: Ohne diagonale Ausrichtung + Wörter einfach zu finden")
print("Stufe 2: Ohne diagonale Ausrichtung + einige wiederholte Fragmente")
print("Stufe 3: Alle Richtungen + einige wiederholte Fragmente + Verbindungen unwahrscheinlicher")
print("Stufe 4: Alle Richtungen + sehr viele wiederholte Fragmente + Verbindungen unwahrscheinlicher\n")

stufe = abfrage_zahl("Was ist der gewünschte Schwierigkeitsgrad (Zahl von 1 bis 4)? ",
                     "not ausgabe in range(1, 5)", "Bitte gebe eine Zahl von 1 bis 4 ein.")

with codecs.open("Beispieldateien\\"+os.listdir("Beispieldateien")[datei_nummer], "r", "utf-8") as file:
    Zeilen = file.readlines()
    for n in range(len(Zeilen)):
        Zeilen[n] = Zeilen[n].strip()
    maße = Zeilen[0].split(" ")
    maße = [int(maße[0]), int(maße[1])]
    gitter = np.empty(maße, str)
    gitter.fill(leer)
    n_wörter = int(Zeilen[1])
    del Zeilen[:2]
    wörter = list(wort.upper() for wort in Zeilen)
    print("\nZu findende Wörter:")
    print(", ".join(wörter)+"\n")

class Wort():
    def __init__(self, typ, string):
        self.typ = typ
        self.string = string
        self.string_echt = string
        self.len = len(self.string)
        if random.randint(0, 1):
            self.string = self.string[::-1]
        self.richtung = None
        self.anfang = None
        self.pos = None

    def einfügen(self, richtung, anfang):
        def ungültig(pos_z, pos_s):
            for i in range(len(pos_z)):
                if gitter[pos_z[i], pos_s[i]] != leer and gitter[pos_z[i], pos_s[i]] != self.string[i]:
                    raise Exception
            for i in list(pos_z)+list(pos_s):
                if abs(i) != i:
                    raise Exception
        if richtung == 0:
            pos_z = self.len*[anfang[0]]
            pos_s = range(anfang[1], anfang[1]+self.len)
        elif richtung == 1:
            pos_z = range(anfang[0], anfang[0]+self.len)
            pos_s = self.len*[anfang[1]]
        elif richtung == 2:
            pos_z = range(anfang[0], anfang[0]+self.len)
            pos_s = range(anfang[1], anfang[1]+self.len)
        else:
            pos_z = range(anfang[0], anfang[0]-self.len, -1)
            pos_s = range(anfang[1], anfang[1]+self.len)
        ungültig(pos_z, pos_s)
        gitter[pos_z, pos_s] = list(self.string)
        self.richtung = richtung
        self.anfang = anfang
        self.pos = list([pos_z[i], pos_s[i]] for i in range(self.len))

    def verbinden(self, index, pos):
        ausrichtungen = [0,1]
        if stufe > 2:
            ausrichtungen = [0,1,2,3]
        random.shuffle(ausrichtungen)
        for r in ausrichtungen:
            self.anfang = pos.copy()
            if r in [0, 2, 3]:
                if self.anfang[1]-len(self.string[:index]) < 0:
                    raise Exception
                self.anfang[1] -= len(self.string[:index])
            if r in [1, 2]:
                if self.anfang[0]-len(self.string[:index]) < 0:
                    raise Exception
                self.anfang[0] -= len(self.string[:index])
            if r == 3:
                if self.anfang[0]-len(self.string[index+1:]) < 0:
                    raise Exception
                self.anfang[0] += len(self.string[:index])
            try:
                self.einfügen(r, self.anfang)
                return
            except:
                pass
        raise Exception

    def posByIndex(self, index):
        return self.pos[index]

    def yx_bereich(self):
        max = maße.copy()
        min = [0, 0]
        if self.richtung in [2, 3]:
            if self.richtung == 2:
                max[0] -= self.len
            else:
                min[0] += self.len-1
                max[0] -= 1
            max[1] -= self.len
        else:
            max[abs(self.richtung-1)] -= self.len
            max[self.richtung] -= 1
        return [min, max]

def verbindungen(wort1, wort2):
    gleich = []
    for i in range(len(wort1)):
        for i2 in range(len(wort2)):
            if wort1[i] == wort2[i2]:
                gleich.append((i, i2))
    return gleich

def wörterMitPos(pos):
    obj = []
    for i in wörter_obj:
        if pos in i.pos:
            obj.append(i)
    return obj

def verbindenTrue(n):
    fertig = False
    möglich = list(w for w in wörter_obj if w.pos != None and sum(
        c in wörter_obj[n].string for c in w.string))
    for wort2 in random.sample(möglich, len(möglich)):
        gleich = verbindungen(wörter_obj[n].string, wort2.string)
        if len(gleich):
            for i in random.sample(gleich, len(gleich)):
                try:
                    wörter_obj[n].verbinden(i[0], wort2.posByIndex(i[1]))
                    fertig = True
                    break
                except:
                    pass
        if fertig:
            break
    return fertig

def verbindenFalse(n):
    if stufe > 2:
        richtungen = random.sample([0, 1, 2, 3], 4)
    else:
        richtungen = random.sample([0, 1], 2)
    fertig = False
    for r in richtungen:
        wörter_obj[n].richtung = r
        bereich = wörter_obj[n].yx_bereich()
        zeilen = random.sample(
            list(range(bereich[0][0], bereich[1][0]+1)), bereich[1][0]-bereich[0][0]+1)
        spalten = random.sample(
            list(range(bereich[0][1], bereich[1][1]+1)), bereich[1][1]-bereich[0][1]+1)
        for z in zeilen:
            for s in spalten:
                try:
                    wörter_obj[n].einfügen(r, [z, s])
                    fertig = True
                    break
                except:
                    pass
            if fertig:
                break
        if fertig:
            break
    return fertig

def reset():
    gitter.fill(leer)
    wörter_obj.clear()
    for wort in wörter:
        wörter_obj.append(Wort(True, wort))
    random.shuffle(wörter_obj)
    wörter_obj.extend(Fragmente)

wörter_obj = []
for wort in wörter:
    wörter_obj.append(Wort(True, wort))
random.shuffle(wörter_obj)

def n_leer(): return sum(sum(s == leer for s in z) for z in gitter) 

Fragmente = []
if stufe < 4:
    for n in range(random.randint(round(n_leer()/3), round(n_leer()/2))):
        Fragmente.append(Wort(False, "".join(random.choice(alphabet)
                         for n in range(random.randint(1, 3)))))
if stufe > 1:
    if stufe < 4:
        F_Anzahl = len(Fragmente)
        Fragmente = Fragmente[:round(len(Fragmente)/2)]
    else:
        F_Anzahl = len(wörter)
    w_strings = list(w.string for w in wörter_obj)
    while len(Fragmente) < F_Anzahl:
        for s in w_strings:
            if random.randint(0, 1):
                if len(s) >= 5:
                    f_länge = random.randint(2, len(s)-2)
                else:
                    f_länge = min(2, len(s))
                start = random.randint(0, len(s)-f_länge)
                fragment = s[start:start+f_länge]
                if random.randint(0,2):
                    fragment="".join(random.sample(fragment,len(fragment)))
                if not fragment in w_strings+Fragmente and not fragment[::-1] in w_strings+Fragmente:
                    Fragmente.insert(random.randint(
                        0, len(Fragmente)), Wort(False, fragment))
                    if len(Fragmente) >= F_Anzahl:
                        break
    b_enthalten = list(set("".join(list(f.string for f in Fragmente))))
    if len(b_enthalten) < 3:
        raus = []
        for w in wörter:
            for b in alphabet:
                if b in w and b not in b_enthalten:
                    if len(w)-sum(w.count(i) for i in b_enthalten) == w.count(b):
                        raus.append(b)
                        break
        while len(b_enthalten) < 3:
            f = "".join(random.choice(alphabet) for n in range(random.randint(1, 2)))
            while sum(i in raus for i in f):
                f = "".join(random.choice(alphabet) for n in range(random.randint(1, 2)))
            Fragmente.append(Wort(False, f))
            b_enthalten = list(set("".join(list(f.string for f in Fragmente))))
wörter_obj.extend(Fragmente)

gelungen = False
while not gelungen:
    neustart = False
    for n in range(len(wörter_obj)):
        if stufe > 2:
            verbinden = not bool(random.randint(0, 2))
        else:
            verbinden = bool(random.randint(0, 1))
        if n > 0:
            func = [verbindenFalse, verbindenTrue]
            fertig = func[int(verbinden)](n)
            if not fertig:
                fertig = func[int(not verbinden)](n)
                if not fertig and n < len(wörter):
                    reset()
                    neustart = True
                    break
        else:
           verbindenFalse(n)
    if not neustart:
        gelungen = True

f_counter = 0
while n_leer() > 0:
    index = random.randint(len(wörter), len(wörter_obj)-1)
    if not verbindenFalse(index):
        f_counter+=1
        if f_counter >= 20:
            for z in range(maße[0]):
                for s in range(maße[1]):
                    if gitter[z,s] == leer:
                        gitter[z,s]=random.choice(random.choice(Fragmente).string)
    else:
        f_counter = 0

rem = []
for f in wörter_obj[len(wörter):]:
    if f.pos == None:
        rem.append(f)
for i in rem:
    wörter_obj.remove(i)

def gitter_ausgeben():
    for zeile in gitter:
        print("  ".join(zeile))
gitter_ausgeben()

input("\nZum Aufdecken der gesuchten Wörter Enter drücken. ")
for z in range(maße[0]):
    for s in range(maße[1]):
        if not sum(int(w.typ) for w in wörterMitPos([z,s])):
            gitter[z,s]=leer
gitter_ausgeben()

while True:
    pass
