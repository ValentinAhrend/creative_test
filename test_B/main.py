from germanetpy.germanet import Germanet
from germanetpy.path_based_relatedness_measures import PathBasedRelatedness
from germanetpy.synset import WordCategory
from pygermanet import Synset

import test_b

if __name__ == '__main__':
    list_of_words = ["Kindergarten", "Computerspiele", "Literatur", "Kochbücher", "Möbel", "Schmuck", "Oper"]
    """
    list_of_words value is the same as in test_a
    the test_b depends on the test_a...
    
    task of this test:
    
    Nenne max. 10 Wörter, die zu den folgenden Wörtern passen.
    Probiere die Begriffe im Kontext möglichst verschieden zu gestalten.
    
    Die Wörter soll eine geringen Abstand zu wort0 haben. Die Wörter untereinander sollen aber möglichst weit
    außereinander liegen.
    
    Welche Wörter von list_of_words werden allerdings abgefragt?
    
    Die Wörter, die abgefragt werden, müssen die Bedingung erfüllen, möglichst viele ähnliche Wörter zu haben.
    Die Wörter werden nach muter0 sortiert.
    
    """

    test_words = test_b.define_test_words(list_of_words)[0:3]

    print(test_words)

    input_dict = {
        "Schule": ["Institution", "Folter", "Bildung", "Lehrer"],
        "Möbel": ["Stuhl", "Tisch", "Holzmöbel", "Lampe", "Sofa", "Leiter"],
        "Schmuck": ["Kette", "Amulett", "Armband", "Uhr", "Goldkette", "Telefon"]
    }

    germanet = Germanet(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
        "Quellen/project/application/test/germanet_data/germanet/GN_V160/GN_V160_XML")
    h: Synset = germanet.get_synset_by_id("s49774")
    o: Synset = germanet.get_synset_by_id("s83979")
    rn = PathBasedRelatedness(germanet=germanet, category=WordCategory.nomen, max_len=35, max_depth=20,
                              synset_pair=(h, o))

    print(test_b.start_test_b(input_dict, germanet, rn))



