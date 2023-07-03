from string import ascii_uppercase as alphabet #Importieren des Alphabets in Großbuchstaben in Form eines Strings
import os #Ich verwende dieses Modul, um, wie bei Junioraufgabe 1, die Anzahl von vorhandenen Beispieldateien zu ermitteln.

alphabet = list(alphabet) #Der String wird in eine Liste mit den einzelnen Buchstaben des Alphabets umgewandelt.
n_Dateien = len(os.listdir("Beispieldateien")) #Dateianzahl wird ermittelt.

class Quer_auto: #Ein Objekt dieser Klasse repräsentiert ein quer stehendes Auto mit seinen wichtigen Attributen.
    def __init__(self, nummer, name, pos):
        self.nummer = nummer #Das Attribut Nummer ist der Index des späteren Objektes in der Liste der quer stehenden Autos.
        self.name = name #Dieses Attribut ist der Buchstabe, mit dem das Auto benannt ist.
        self.pos = pos #Hier wird die Ausgangsposition des Autos gespeichert. Diese ist für die mehrfache Simulation aus derselben Startposition wichtig.
        Autos[pos],Autos[pos+1]=2*[nummer] #In die Liste Autos wird an der entsprechenden Position die Nummer des Autos eingetragen.

    def verschieben(self, richtung, kette): #Wird in der Dokumentation genauer erklärt.
        i1=Autos.index(self.nummer)
        i2=Autos.index(kette[-1])
        n_felder=2-Autos[i1:i2].count(-1)
        if richtung:
            return (self.name+" "+str(n_felder)+" links")
        else:
            return (self.name+" "+str(n_felder)+" rechts")

    def abfolge(self, posAuto): #Genaueres zu dieser Funktion erkläre ich in der Dokumentation.
        diff=posAuto-self.pos #Die Differenz aus der Position des blockierenden Autos und der des Ausfahrenden wird zum Nutzen von späteren Berechnungen gebildet.
        richtung = False #Enthält später den Wert dafür, ob das blockierende Auto nach links oder nach rechts verschoben werden soll, je nachdem, was effizienter ist.
        leere_stellen = [i for i, stelle in enumerate(Autos) if stelle == -1]
        if Autos[:self.pos].count(-1) >= 2-diff:
            richtung = True #True steht für links und False für rechts.
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

while True: #Dieser Teil ist derselbe wie in Junioraufgabe 1 und allen weiteren Aufgaben mit Beispieldateien.
    try:
        datei_nummer = int(input("Welche Beispieldatei soll verwendet werden? "))
        if not datei_nummer in range(0, n_Dateien):
            raise Exception
        break
    except:
        print("Bitte gebe eine Zahl von 0 bis "+str(n_Dateien-1)+" ein.\n")

with open("Beispieldateien\\"+os.listdir("Beispieldateien")[datei_nummer]) as file: #Die entsprechende Textdatei wird geöffnet.
    Zeilen = file.readlines() #Eine Liste aus den einzelnen Zeilen wird erstellt.
    bereich = Zeilen[0].strip().split(" ") #Die erste Zeile wird in eine Liste mit den beiden Buchstaben aufgeteilt, davor wird noch mit der Funktion strip() das Zeilenende-Zeichen entfernt.
    Auto_namen = alphabet[alphabet.index(bereich[0]):alphabet.index(bereich[1])+1] #Eine Liste Aller im vorgegebenen Bereich liegenden Autonamen wird erstellt.
    n_normal = len(Auto_namen) #Aus der Länge der Liste mit den Namen der normal geparkten Autos wird deren Anzahl ermittelt.
    Autos = n_normal*[-1] #Eine -1 bedeutet, dass die entsprechende Stelle zum Ausparken frei ist. Ansonsten steht an der Stelle die Nummer des dort geparkten quer stehenden Autos.
    n_quer = int(Zeilen[1].strip())
    del Zeilen[:2] #Nachdem der Buchstabenbereich und die Anzahl der quer stehenden Autos ermittelt wurde, werden die ersten beiden Zeilen gelöscht.
    quer_obj = []
    for n in range(n_quer): #Aus den Daten der restlichen Zeilen werden Objekte der Klasse Quer_auto erstellt.
        name = Zeilen[n][0]
        pos = int(Zeilen[n][2:].strip())
        quer_obj.append(Quer_auto(len(quer_obj), name, pos))

for n in range(n_normal): #Die eingeparkten Autos werden durchgegangen und für jedes wird ausgegeben, ob es blockiert ist und falls ja, was die beste Lösung ist.
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
