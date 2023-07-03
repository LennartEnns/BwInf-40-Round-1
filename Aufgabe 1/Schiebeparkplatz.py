from string import ascii_uppercase as alphabet
import os

alphabet = list(alphabet)
n_Dateien = len(os.listdir("Beispieldateien"))

class Quer_auto:
    def __init__(self, nummer, name, pos):
        self.nummer = nummer
        self.name = name
        self.pos = pos
        Autos[pos],Autos[pos+1]=2*[nummer]

    def verschieben(self, richtung, kette):
        i1=Autos.index(self.nummer)
        i2=Autos.index(kette[-1])
        n_felder=2-Autos[i1:i2].count(-1)
        if richtung:
            return (self.name+" "+str(n_felder)+" links")
        else:
            return (self.name+" "+str(n_felder)+" rechts")

    def abfolge(self, posAuto):
        diff=posAuto-self.pos
        richtung = False
        leere_stellen = [i for i, stelle in enumerate(Autos) if stelle == -1]
        if Autos[:self.pos].count(-1) >= 2-diff:
            richtung = True
            leere_stellen_l = [i for i in leere_stellen if i < self.pos]
            bereich_l = Autos[leere_stellen_l[-2+diff]:self.pos]
            if Autos[self.pos:].count(-1) >= 1+diff:
                leere_stellen_r = [i for i in leere_stellen if i > self.pos]
                bereich_r = Autos[self.pos+2:leere_stellen_r[diff]+1]
                n_Autos_l, n_Autos_r = 0, 0
                for i in range(len(bereich_l)):
                    if bereich_l[i-1] != bereich_l[i] != -1:
                        n_Autos_l += 1
                for i in range(len(bereich_r)):
                    if bereich_r[i-1] != bereich_r[i] != -1:
                        n_Autos_r += 1
                if n_Autos_r < n_Autos_l:
                    richtung=False
                elif n_Autos_r == n_Autos_l:
                    richtung = bool(diff)
        elif Autos[self.pos:].count(-1) >= 1+diff:
            leere_stellen_r = [i for i in leere_stellen if i > self.pos]
            bereich_r = Autos[self.pos+2:leere_stellen_r[diff]+1]
            richtung = False
        else:
            return False
        kette=[]
        if richtung:
            for i in bereich_l:
                if i != -1 and not i in kette:
                    kette.append(i)
        else:
            for i in bereich_r[::-1]:
                if i != -1 and not i in kette:
                    kette.append(i)
        kette.append(self.nummer)
        return richtung, kette

while True:
    try:
        datei_nummer = int(input("Welche Beispieldatei soll verwendet werden? "))
        if not datei_nummer in range(0, n_Dateien):
            raise Exception
        break
    except:
        print("Bitte gebe eine Zahl von 0 bis "+str(n_Dateien-1)+" ein.\n")

with open("Beispieldateien\\"+os.listdir("Beispieldateien")[datei_nummer]) as file:
    Zeilen = file.readlines()
    bereich = Zeilen[0].strip().split(" ")
    Auto_namen = alphabet[alphabet.index(bereich[0]):alphabet.index(bereich[1])+1]
    n_normal = len(Auto_namen)
    Autos = n_normal*[-1]
    n_quer = int(Zeilen[1].strip())
    del Zeilen[:2]
    quer_obj = []
    for n in range(n_quer):
        name = Zeilen[n][0]
        pos = int(Zeilen[n][2:].strip())
        quer_obj.append(Quer_auto(len(quer_obj), name, pos))

for n in range(n_normal):
    print("\n"+Auto_namen[n]+": ",end="")
    if Autos[n] != -1:
        blockierend=quer_obj[Autos[n]]
        ausgabe=blockierend.abfolge(n)
        if ausgabe:
            richtung, kette=ausgabe
            print(quer_obj[kette[0]].verschieben(richtung, kette),end="")
            for i in kette[1:]:
                print(", "+quer_obj[i].verschieben(richtung, kette),end="")
        else:
            print("Dieses Auto ist unmöglich auszuparken!",end="")
print("")
while True:
    pass
