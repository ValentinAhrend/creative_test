import spacy

from test_C.test_c import test_c0

if __name__ == '__main__':



    list_of_sentences = [
        "Der Wert von Geld ist mehr als von Gold.",
        "Das Haus im Garten hat einen Balkon",
        "Die Tapete an den Wänden ist voller Farbe",
        "Die Kugel ist ein Ball aus Holz",
        "Der Taschenrechner rechnet Zahlen in Taschen",
        "Die Figur ist ein Gemälde",
        "Flasche, Trinken, Essen",
        "Die Tiere heißen Maus, Katze und Hund",
        "Die Zahl heißt entweder Pi, Baum oder Matrix.",
        "Die Würfel haben eine Kantenlänge von 5 Fußballfeldern",
        "Die Frage ist eine Heizung der Antwort",
        "Bücher beschreiben bemalte Gemälde der Antike."
    ]
    list_of_winner_dicts = [
        {
            "Wert":"Zahl",
            "Geld": "Lunge",
            "Gold" : "Magie"
        },
        {
            "Haus":"Getreide",
            "Garten":"Maschine",
            "Balkon":"Sohn"
        },
        {
            "Tapete":"Rakete",
            "Wand":"Strand",
            "Farbe":"Narbe"
        },
        {
            "Kugel":"Uhrzeit",
            "Ball":"Fall",
            "Holz":"Rotze"
        },
        {
            "Taschenrechner":"Gerechtigkeit",
            "Zahl":"Mahnmal",
            "Tasche":"Flasche",
        },
        {
            "Figur":"Geburt",
            "Gemälde":"Physik",
        }, {
            "Flasche":"Wasser",
            "Trinken":"Fluss",
            "Essen":"Geld"
        },
        {
            "Maus":"Käse",
            "Katze":"Straße",
            "Hund":"Erdkunde"
        },
        {
            "Pi":"Vieh",
            "Baum":"Schaum",
            "Matrix":"Physik"
        },
        {
            "Würfel":"Scheibe",
            "Kantenlänge":"Schreibschrift",
            "Fußballfeld":"Tier"
        },
        {
            "Frage":"Klage",
            "Heizung":"Meinung",
            "Antwort":"Kirche"
        },
        {
            "Buch":"Fluch",
            "Gemälde":"Tesla",
            "Antike":"Maus"
        }
    ]

    spacyy = spacy.load(str(__file__)[
                                    0:str(__file__).rindex(
                                        "test_C")] + "spacy_data/de_core_news_md/de_core_news_md-3.2.0")

    for sentence in list_of_sentences.__reversed__():
        print(test_c0(input_str=sentence, winners=list_of_winner_dicts[list_of_sentences.index(sentence)], space=spacyy))
        print("_________________________-")
        break