import csv
import random
from datetime import datetime, timedelta

class Varos:
    def __init__(self, penzkeret, elegedettseg, min_elegedettseg, kezdo_datum, honapok):
        self.penzkeret = penzkeret
        self.elegedettseg = elegedettseg
        self.min_elegedettseg = min_elegedettseg
        self.kezdo_datum = datetime.strptime(kezdo_datum, "%Y-%m-%d")
        self.honapok = honapok
        self.aktualis_datum = self.kezdo_datum
        self.epuletek = self.beolvas_csv("/mnt/data/verseny.csv", sep=';')
        self.lakosok = self.beolvas_csv("lakosok.csv")
        self.szolgaltatasok = self.beolvas_csv("szolgaltatasok.csv")
        self.varosfejlesztesek = self.beolvas_csv("varosfejlesztesek.csv")
        self.esemenyek = self.betolt_esemenyek()

    def beolvas_csv(self, fajlnev, sep=","):
        try:
            with open(fajlnev, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=sep)
                return [row for row in reader]
        except FileNotFoundError:
            print(f"Hiba: {fajlnev} nem található!")
            return []

    def betolt_esemenyek(self):
        return [
            {"nev": "Nincs esemény", "valoszinuseg": 0.4, "penzvaltozas": 0, "elegedettseg_valtozas": 0},
            {"nev": "Gazdasági növekedés", "valoszinuseg": 0.2, "penzvaltozas": 500000, "elegedettseg_valtozas": 2},
            {"nev": "Természeti katasztrófa", "valoszinuseg": 0.1, "penzvaltozas": -1000000, "elegedettseg_valtozas": -5},
            {"nev": "Új befektető érkezett", "valoszinuseg": 0.15, "penzvaltozas": 1000000, "elegedettseg_valtozas": 3},
            {"nev": "Közszolgáltatási zavar", "valoszinuseg": 0.15, "penzvaltozas": -500000, "elegedettseg_valtozas": -3},
            {"nev": "Tűzeset: Egy épület leégett", "valoszinuseg": 0.1, "penzvaltozas": -2000000, "elegedettseg_valtozas": -8}
        ]
    
    def alkalmaz_esemeny(self):
        esemeny = random.choices(self.esemenyek, weights=[e["valoszinuseg"] for e in self.esemenyek])[0]
        self.penzkeret += esemeny["penzvaltozas"]
        self.elegedettseg = max(0, min(100, self.elegedettseg + esemeny["elegedettseg_valtozas"]))
        print(f"Esemény történt: {esemeny['nev']} (Pénzváltozás: {esemeny['penzvaltozas']}, Elégedettség változás: {esemeny['elegedettseg_valtozas']})")
    
    def ev_fordulo(self):
        print(f"Év: {self.aktualis_datum.year}")
        self.alkalmaz_esemeny()
        print(f"Pénzkeret: {self.penzkeret}, Elégedettség: {self.elegedettseg}%")
        valasz = input("Szeretnél továbblépni a következő évre? (igen/nem): ")
        if valasz.lower() == "igen":
            self.aktualis_datum += timedelta(days=365)
            return True
        return False
    
    def futtat_szimulacio(self):
        for _ in range(self.honapok // 12):
            if self.penzkeret <= 0 or self.elegedettseg < self.min_elegedettseg:
                print("Játék vége!")
                break
            if not self.ev_fordulo():
                break

if __name__ == "__main__":
    varos = Varos(penzkeret=5000000, elegedettseg=70, min_elegedettseg=50, kezdo_datum="2025-01-01", honapok=36)
    varos.futtat_szimulacio()