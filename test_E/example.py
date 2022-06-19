from germanetpy.germanet import Germanet
from germanetpy.path_based_relatedness_measures import PathBasedRelatedness
from germanetpy.synset import WordCategory
from germanetpy.synset import Synset

from word_relatedness.word_relation import WordRelation

if __name__ == '__main__':
    list_of_words = ["Tennis", "Ball", "Gummiball", "Sprung", "Leichtathletik", "Sprint", "Langlauf", "Skifahren", "Schnee", "Winter", "Sommer", "Sonne", "Strand", "Sand", "Meer", "Wasser", "Welle", "Palme", "Sonne"]

    germanet = Germanet(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
        "Quellen/project/application/test/germanet_data/germanet/GN_V160/GN_V160_XML")
    h: Synset = germanet.get_synset_by_id("s49774")
    o: Synset = germanet.get_synset_by_id("s83979")
    rn = PathBasedRelatedness(germanet=germanet, category=WordCategory.nomen, max_len=35, max_depth=20,
                              synset_pair=(h, o))

    relation_graph = []

    for x in range(len(list_of_words)):
        if x > 2:
            w1 = list_of_words[x - 3]
            w2 = list_of_words[x]
            print(w1, w2)
            wr = WordRelation(w1, w2, germanet.get_synsets_by_orthform(w1)[0], germanet.get_synsets_by_orthform(w2)[0],
                              rn)
            relation_graph.append(wr.calculate_relation(useG=True))

    print(relation_graph)