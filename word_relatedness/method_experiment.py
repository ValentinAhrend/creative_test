import spacy as spacy
from scipy import spatial
from germanetpy.germanet import Germanet
import csv
from random import randint

from germanetpy.path_based_relatedness_measures import PathBasedRelatedness
from germanetpy.synset import Synset, WordCategory
from spacy import displacy

from word_relatedness.experiment import semantic_distance_with_raster
from word_relatedness.ngd import NGD
from word_relatedness.semantic_context import semantic_context


def z0(wordA: str, wordB: str):
    distance = 1 - semantic_distance_with_raster(germanet.get_synsets_by_orthform(wordA)[0],
                                                 germanet.get_synsets_by_orthform(wordB)[0])

    # print(".1")
    ngd = 1 - NGD(wordA, wordB)
    # print(".2")
    context = 1 - semantic_context(wordA, wordB)
    # print(".3")
    vector = 1 - spacy(wordA).similarity(spacy(wordB))
    # print(".4")

    # print(ngd)

    """
    
    calculate a realtion of each number with modified influency
    
    """

    # take the median of distance and vector

    median_a = (distance + vector) / 2
    median_b = (distance + context) / 2
    median_c = (distance + ngd) / 2
    median_1 = (vector + context) / 2
    median_2 = (vector + ngd) / 2

    filling = [0, 0, 0, 0]
    if vector > 1.0 and context == 1:
        filling[3] = 68.75
        filling[2] = 5.8035714
        # filling[1] = 4.9107143
        filling[0] = 20.5357143
    elif vector - ngd > distance and context != 1 and vector > distance:
        print("current topic")
        filling[3] = 18.75
        # filling[2] = 5.8035714
        filling[1] = 50
        filling[0] = 20.5357143
    else:
        filling[0] = 41.0714286
        # filling[1] = 9.8214286
        # filling[2] = 11.6071429
        filling[3] = 37.5

    # fill all equally until 100
    while sum(filling) < 100:
        filling[0] += 1
        filling[1] += 1
        filling[2] += 1
        filling[3] += 1

    """
    Normalverteilung:
    
    0: 40
    1: 10
    2: 10
    3: 40
    
    Verteilung Aktueller Fall von NGD:
    
    0: 17
    1: 49
    2: 17
    3: 17
    
    Verteilung großer Vector:
    
    0: 9
    1: 1
    2: 1
    3: 89
    
    """

    result = (distance * filling[0] + ngd * filling[1] + context * filling[2] + vector * filling[3]) / sum(filling)
    print(str(result).replace(".", ","))
    print(distance)
    print("?")
    print([iteration, distance, ngd, context, vector, wordA, wordB, distance + ngd + context + vector])


if __name__ == '__main__':
    print(".")
    spacy = spacy.load(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität Quellen/project/application/creativity_test/spacy_data/de_core_news_md/de_core_news_md-3.2.0")
    print("..")

    """t = spacy("Ich finde Katzen toll.")
    displacy.serve(t, port=1022)
    exit(1)"""

    germanet_file = str(__file__)[
                    0:str(__file__).rindex("word_relatedness")] + "germanet_data/germanet/GN_V160/GN_V160_XML"
    germanet = Germanet(germanet_file)

    h: Synset = germanet.get_synset_by_id("s49774")
    o: Synset = germanet.get_synset_by_id("s83979")
    relatedness = PathBasedRelatedness(germanet=germanet, category=WordCategory.nomen, max_len=35,
                                       max_depth=20,
                                       synset_pair=(h, o))

    max_iterations = 100
    output_data_name = "output.csv"
    iteration = 0
    z0("Himmel", "Wolkenkratzer")
    z0("Gefühlschaos", "Regenrinne")
    z0("Relativitätstheorie", "Schmetterling")
    z0("Stadt", "Zentrum")
    z0("Affe", "Mensch")
    z0("Wolkenkratzer", "Wolke")
    z0("Zettel", "Blatt")
    z0("Regenrinne", "Gefühlschaos")
    z0("Synapse", "Test")
    z0("Haus", "Garten")
    z0("Theorie", "Praxis")
    z0("König", "Massage")
    z0("Reflex", "Zerstörung")
    z0("Schokolade", "Katze")


    exit(1)

    """
    file format:
    ITERATION | DISTANCE | NGD | CONTEXT | VECTOR | MEDIAN | SIMILARITY  
    
    SIMILARITY: abs(median(all) - each_output) 
      
    """

    output_rows = []

    strings: list = germanet.get_lexunits_by_wordcategory(WordCategory.nomen)
    string_max = len(strings)

    for iteration in range(max_iterations):
        print(iteration)
        wordA1: str = strings[randint(0, string_max)].orthform
        wordB1: str = strings[randint(0, string_max)].orthform
        output_rows.append(z0(wordA1, wordB1))
        print(output_rows[-1])

    output_rows.insert(0, ["Iteration", "Distance", "NGD", "Context", "Vector", "WordA", "WordB"])

    print(output_rows)

    with open(output_data_name, "w") as file:
        writer = csv.writer(file)
        writer.writerows(output_rows)

    """
    
    Die Methoden können nicht durch eine Durchschnittsberechnung in einen finalen Wert übertragen werden.
    Daher muss ein Algorthmus die Verteilung erstellen. 
    
    """
