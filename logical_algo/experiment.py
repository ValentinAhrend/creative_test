import spacy

import time
from logical_algo import lingual_index

if __name__ == '__main__':
    list_of_sentences = [
        "Das Haus ist grün.",
        "Die Flasche hat keinen Deckel.",
        "Gegen alle Erwartungen wurde der Fall absgeschlossen.",
        "Die Bank macht heute schon um 2 Uhr zu.",
        "Die Relativitätstheorie ist eine Theorie von Albert Einstein.",
        "Die Welt besteht aus Fehlern",
        "Ich hole die goldenen Gaben",
        "Der Versuch ist gut.",
        "Heizungen sind eine wichtige Erfindung",
        "Der Lebkuchen wurde in Sachsen entdeckt",
        "Fragen über Fragen sammeln sich im Zelt"
    ]
    list_of_unlogical_sentences = [
        "Die Maus fängt den Hund auf der Katze",
        "Der Computer isst Essen",
        "Fragezeichen beißt den Teufel",
        "Die Mutter ist bei der Geburt geboren worden",
        "Taschenrechner rechnen Taschen in Zahlen",
        "Bäume sind heller als Lichter",
        "Holz ist schwerer als die Situation",
        "Ohne Luft kein Tot",
        "Würfel malen gerne Spinnen",
        "Unlogische Sätze zu schreiben ist logisch",
        "Schleim ist besser als die Statue",
    ]
    spacyy = spacy.load(str(__file__)[
                        0:str(__file__).rindex(
                            "logical_algo")] + "spacy_data/de_core_news_md/de_core_news_md-3.2.0")
    seconds = 0
    for sentence in list_of_unlogical_sentences:
        seconds = time.time_ns() / 1000000000
        print(lingual_index.run(sentence, spacyy))
        print(time.time_ns() / 1000000000 - seconds)
        print("_____________________________")