import csv
import random
from datetime import datetime, timedelta

class Varos:
    def __init__(self, penzkeret, elegedettseg, min_elegedettseg, kezdo_datum):
        self.penzkeret = penzkeret
        self.elegedettseg = elegedettseg
        self.min_elegedettseg = min_elegedettseg
        self.aktualis_datum = datetime.strptime(kezdo_datum, "%Y-%m-%d")
        self.epuletek = self.beolvas_csv("verseny.csv", sep=';')
        self.lakosok = self.beolvas_csv("Lakosok.csv", sep=';')
        self.szolgaltatasok = self.beolvas_csv("Szolgaltatasok.csv", sep=';')
        self.varosfejlesztesek = self.beolvas_csv("Varosfejlesztes.csv", sep=';')
        self.esemenyek = self.betolt_esemenyek()

    def beolvas_csv(self, fajlnev, sep=","):
        try:
            with open(fajlnev, newline='', encoding='utf-8') as file:
                return list(csv.DictReader(file, delimiter=sep))
        except FileNotFoundError:
            print(f"Hiba: {fajlnev} nem található!")
            return []
    
    def ment_csv(self, fajlnev, adatok, fejlec):
        with open(fajlnev, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fejlec, delimiter=';')
            writer.writeheader()
            writer.writerows(adatok)

    def betolt_esemenyek(self):
        return [
            {"nev": "Gazdasági fellendülés", "valoszinuseg": 0.2, "penzvaltozas": 750000, "elegedettseg_valtozas": 5},
            {"nev": "Lakáspiaci válság", "valoszinuseg": 0.15, "penzvaltozas": -500000, "elegedettseg_valtozas": -4},
            {"nev": "Új lakótelep épült", "valoszinuseg": 0.1, "penzvaltozas": -1000000, "elegedettseg_valtozas": 8},
            {"nev": "Tűzeset egy lakóházban", "valoszinuseg": 0.1, "penzvaltozas": -750000, "elegedettseg_valtozas": -6},
            {"nev": "Infláció megugrott", "valoszinuseg": 0.1, "penzvaltozas": -1000000, "elegedettseg_valtozas": -3},
            {"nev": "Új kórház épült", "valoszinuseg": 0.1, "penzvaltozas": -2000000, "elegedettseg_valtozas": 10},
            {"nev": "Tornádó egy teljes negyedet lerombolt", "valoszinuseg": 0.05, "penzvaltozas": -4000000, "elegedettseg_valtozas": -15}
        ]
    
    def alkalmaz_esemenyek(self):
        esemenyek_szama = random.randint(1, 3)  # Több esemény is történhet egy év alatt
        for _ in range(esemenyek_szama):
            esemeny = random.choices(self.esemenyek, weights=[e["valoszinuseg"] for e in self.esemenyek])[0]
            self.penzkeret += esemeny["penzvaltozas"]
            self.elegedettseg = max(0, min(100, self.elegedettseg + esemeny["elegedettseg_valtozas"]))
            print(f"Esemény történt: {esemeny['nev']} (Pénz: {esemeny['penzvaltozas']}, Elégedettség: {esemeny['elegedettseg_valtozas']}%)")
    
    def ev_fordulo(self):
        print(f"Év: {self.aktualis_datum.year}, Pénzkeret: {self.penzkeret}, Elégedettség: {self.elegedettseg}%")
        self.alkalmaz_esemenyek()
        return input("Tovább lépsz a következő évre? (igen/nem): ").strip().lower() == "igen"
    
    def futtat_szimulacio(self):
        while self.penzkeret > 0 and self.elegedettseg >= self.min_elegedettseg:
            if not self.ev_fordulo():
                break
        print("Játék vége!")

if __name__ == "__main__":
    varos = Varos(penzkeret=5000000, elegedettseg=70, min_elegedettseg=50, kezdo_datum="2025-01-01")
    varos.futtat_szimulacio()

