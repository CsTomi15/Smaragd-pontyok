import csv
#epuletek = open(r"C:\Users\orosz\Desktop\Smaragd-pontyok\ac#\verseny.csv","r", encoding="UTF-8")

#print(epuletek.read())
'''
class Epulet:
    def __init__(self,azonosito,nev,tipus,epitesiEve,hasznosTerulet):
        self.azonosito = int(azonosito)
        self.nev = nev
        self.tipus = tipus
        self.epitesiEve = int(epitesiEve)
        self.hasznosTerulet = int(hasznosTerulet)
'''


def csv_to_dict_list(fajlnev):
    with open(fajlnev, newline='', encoding='utf-8') as file:
        olvaso = csv.DictReader(file, delimiter=";")
        return [sor for sor in olvaso]

# Betöltés
epuletek = csv_to_dict_list(r"C:\Users\orosz\Desktop\Smaragd-pontyok\ac#\verseny.csv")

# Kiírás
for epulet in epuletek:
    print(epulet)




