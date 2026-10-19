import csv
from espositore import Espositore
from stand import Stand, StandPrese, StandPremium


class LingottoFiere:

    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome
        self.stand = []
        self.espositori = []

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        self.stand.clear()
        self.espositori.clear()

        try:
            with open(file_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if not row:
                        continue
                    codice = row[0]
                    if codice.startswith("ST"):
                        # Gestione stand
                        if len(row) == 4:  # Stand Base
                            s = Stand(*row)
                        elif len(row) == 5:  # Stand Prese o Premium
                            if row[4].isdigit():
                                s = StandPrese(
                                    row[0], row[1], row[2], row[3], row[4]
                                )
                            else:
                                s = StandPremium(
                                    row[0], row[1], row[2], row[3], row[4]
                                )
                        self.stand.append(s)
                    elif codice.startswith("ES"):
                        nome, cognome = row[1:]
                        espositore = Espositore(codice, nome, cognome)
                        self.espositori.append(espositore)
        except FileNotFoundError:
            raise FileNotFoundError("Il file CSV non è stato trovato.")

    def _trova_stand(self, codice):
        return next((s for s in self.stand if s.codice == codice), None)

    def _trova_espositore(self, codice):
        return next((e for e in self.espositori if e.codice == codice), None)

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        stand = self._trova_stand(codice_stand)
        espositore = self._trova_espositore(codice_espositore)

        if not stand:
            raise Exception("Stand non trovato.")
        if not espositore:
            raise Exception("Espositore non trovato.")
        if not stand.disponibile:
            raise Exception("Stand non disponibile.")
        for s in self.stand:
            if espositore == s.espositore:
                raise Exception("Espositore già associato ad uno stand.")

        stand.assegna(espositore)

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile"""
        for e in self.espositori:
            res = f"- {e}"
            for s in self.stand:
                if e == s.espositore:
                    res = f"{res} --> Assegnato allo stand: {s.codice}"
                    break
            print(res)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo sfruttando il metodo __lt__"""
        return sorted(self.stand)
