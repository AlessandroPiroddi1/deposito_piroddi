import re
from collections import Counter
from typing import List, Tuple

def leggi_e_normalizza(file_path: str) -> str:
    """
    Legge il file in UTF-8 e normalizza il testo:
    - converte in minuscolo;
    - rimuove la punteggiatura e i simboli, mantenendo cifre, lettere latine (incluse accentate) e i ritorni a capo.
    Non modifica i caratteri di newline, così il conteggio righe rimane corretto.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        testo = f.read()
    testo = testo.lower()
    # Mantieni \n, cifre e lettere latine (A–Z, a–z, accentate in Latin-1); sostituisci tutto il resto con spazio.
    testo = re.sub(r"[^0-9a-zà-öø-ÿ\n]+", " ", testo)
    # Comprimi spazi multipli; non tocchiamo i newline
    testo = re.sub(r"[ ]{2,}", " ", testo)
    return testo

def conta_righe(testo_normalizzato: str) -> int:
    """
    Conta il numero di righe sul testo già normalizzato, preservando i newline originali.
    Una riga vuota conta come riga.
    """
    # splitlines(True) mantiene l'informazione delle righe; qui basta splitlines() per contare
    return len(testo_normalizzato.splitlines())

def conta_parole(testo_normalizzato: str) -> int:
    """
    Conta il numero totale di parole sul testo normalizzato.
    La tokenizzazione avviene separando su whitespace, con newline già preservati.
    """
    # Sostituiamo i newline con spazi per una tokenizzazione uniforme, senza alterare il conteggio parole
    tokens = testo_normalizzato.replace("\n", " ").split()
    return len(tokens)

def top5_parole(testo_normalizzato: str) -> List[Tuple[str, int]]:
    """
    Restituisce la top-5 parole più frequenti (parola, conteggio) dal testo normalizzato.
    """
    tokens = testo_normalizzato.replace("\n", " ").split()
    counter = Counter(tokens)
    return counter.most_common(5)


if __name__ == "__main__":
    path = r"18-08-2025\es_1\data\bot code.txt"
    testo_norm = leggi_e_normalizza(path)

    # 1) numero totale di righe
    n_righe = conta_righe(testo_norm)
    print(f"Numero totale di righe: {n_righe}")

    # 2) numero totale di parole
    n_parole = conta_parole(testo_norm)
    print(f"Numero totale di parole: {n_parole}")

    # 3) top-5 parole più frequenti
    for parola, cnt in top5_parole(testo_norm):
        print(f"{parola}:{cnt}")
    