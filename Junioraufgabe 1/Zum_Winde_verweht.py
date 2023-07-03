from math import sqrt #Quadratwurzel-Funktion, um den Satz des Pythagoras anwenden zu können.
import os #Ich verwende dieses Modul, um die Anzahl von vorhandenen Beispieldateien zu ermitteln.

n_Dateien=len(os.listdir("Beispieldateien")) #Dateianzahl wird ermittelt.

while True: #Es wird so lange nach einem input gefragt, bis eine Zahl eingegeben wurde, die zwischen 1 und n_Dateien liegt.
    try:
        datei_nummer=int(input("Welche Beispieldatei soll verwendet werden? "))
        if not datei_nummer in range(1,n_Dateien+1):
            raise Exception
        break
    except:
        print("Bitte gebe eine Zahl von 1 bis "+str(n_Dateien)+" ein.\n")

with open("Beispieldateien\\"+os.listdir("Beispieldateien")[datei_nummer-1]) as file: #Die entsprechende Textdatei wird geöffnet, wobei vom Index 1 abgezogen wird, weil es mit 0 statt 1 beginnt.
    Zeilen=file.readlines() #Eine Liste aus den einzelnen Zeilen wird erstellt.
    n_Häuser=int(Zeilen[0].split(" ")[0]) #Die Anzahlen der Häuser und Windräder werden ausgelesen, indem die beiden Zahlen mit Leerzeichen als Separator in eine Liste aus zwei Integern konveriert werden.
    n_Windräder=int(Zeilen[0].split(" ")[1].strip()) #Damit die Umwandlung in eine Ganzzahl funktioniert, muss hier noch das "unsichtbare" Zeilenendezeichen "\n" mit strip() entfernt werden.
    del Zeilen[0] #Die erste Zeile wird nun nicht mehr benötigt.
    for i in range(len(Zeilen)): #Alle übrigen Zeilen werden in dieser for-Schleife wie oben in Listen umgewandelt, die in diesem Fall jeweils den x- und den y-Wert enthalten.
        Zeilen[i]=Zeilen[i].split(" ")
        for i2 in range(len(Zeilen[i])):
            Zeilen[i][i2]=int(Zeilen[i][i2].strip())
    Häuser=Zeilen[0:n_Häuser] #Die Liste wird aufgeteilt in eine Liste für die Häuser-Positionen und eine für die Windrad-Positionen.
    Windräder=Zeilen[n_Häuser:]

max_höhen=[]
for w in Windräder:
    am_nächsten=None
    for h in Häuser:
        x_abstand=abs(w[0]-h[0]) #Es werden der x- und der y-Abstand zwischen dem Haus und dem Windrad berechnet.
        y_abstand=abs(w[1]-h[1])
        abstand=sqrt(x_abstand**2+y_abstand**2) #Nun wird mithilfe des Satzes des Pythagoras der genaue Abstand zwischen Haus und Windrad berechnet.
        if am_nächsten==None: #Wenn die Variable am_nächsten noch nicht verglichen wurde, also None beträgt, darf sie nicht direkt mit einer Zahl verglichen werden. Daher habe ich hier auf ein logisches "Oder" verzichtet.
            am_nächsten=abstand
        elif abstand<am_nächsten:
            am_nächsten=abstand
    max_höhe=round(am_nächsten/10,2) #Die maximale Höhe des Windrades wird auf zwei Nachkommastellen gerundet.
    max_höhen.append(max_höhe)

ausgabe_liste=[]
for n in range(len(max_höhen)): #Für jedes Windrad wird seine Position ausgegeben und ob bzw. wie hoch es gebaut werden darf. Zusätzlich wird eine Liste erstellt, damit die Daten auch in dieser Form dargestellt werden können.
    print("Das Windrad bei [x: "+str(Windräder[n][0])+", y: "+str(Windräder[n][1])+"] darf ",end="")
    if max_höhen[n]>0:
        print("maximal "+str(max_höhen[n])+" m hoch sein.\n")
    else:
        print("nicht gebaut werden.\n")
    ausgabe_liste.append(str((Windräder[n][0],Windräder[n][1]))+": "+str(max_höhen[n])+" m")

ausgabe_liste=str(ausgabe_liste).replace("'","") #Aus Schönheitsgründen werden alle Anführungszeichen aus dem String der Liste entfernt.
print("Als Liste:\n"+ausgabe_liste)
while True:
    pass
