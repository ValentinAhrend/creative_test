from random import randint

import spacy as spacy
from germanetpy.germanet import Germanet
from germanetpy.synset import WordCategory, Synset

from word_relatedness.experiment import semantic_distance_with_raster
from word_relatedness.ngd import NGD
from word_relatedness.semantic_context import semantic_context


def z0(wordA, wordB):
    print(wordA, wordB)
    distance = 1 - semantic_distance_with_raster(germanet.get_synsets_by_orthform(wordA)[0],
                                                 germanet.get_synsets_by_orthform(wordB)[0])

    # print(".1")
    ngd = 1 - NGD(wordA, wordB)
    # print(".2")
    context = 1 - semantic_context(wordA, wordB)
    # print(".3")
    vector = 1 - spacy(wordA).similarity(spacy(wordB))
    return str(distance).replace(".", ","), str(ngd).replace(".", ","),\
           str(context).replace(".", ","), str(vector).replace(".", ",")


def z1(wordA, wordB):
    vector = 1 - spacy(wordA).similarity(spacy(wordB))

    if vector <= 1:
        return ""

    distance = 1 - semantic_distance_with_raster(germanet.get_synsets_by_orthform(wordA)[0],
                                                 germanet.get_synsets_by_orthform(wordB)[0])

    # print(".1")
    ngd = 1 - NGD(wordA, wordB)
    # print(".2")
    context = 1 - semantic_context(wordA, wordB)
    # print(".3")
    print(wordA, wordB, vector)
    return str(distance).replace(".", ","), str(ngd).replace(".", ","),\
           str(context).replace(".", ","), str(vector).replace(".", ",")


def z2(wordA, wordB):

    vector = 1 - spacy(wordA).similarity(spacy(wordB))
    distance = 1 - semantic_distance_with_raster(germanet.get_synsets_by_orthform(wordA)[0],
                                                 germanet.get_synsets_by_orthform(wordB)[0])
    ngd = 1 - NGD(wordA, wordB)

    if vector - ngd <= distance:
        return ""

    # print(".1")
    # print(".2")
    context = 1 - semantic_context(wordA, wordB)
    # print(".3")
    print(wordA, wordB, vector)
    return str(distance).replace(".", ","), str(ngd).replace(".", ","),\
           str(context).replace(".", ","), str(vector).replace(".", ",")


def z3(wordA, wordB):
    vector = 1 - spacy(wordA).similarity(spacy(wordB))

    if vector >= 1:
        return ""

    distance = 1 - semantic_distance_with_raster(germanet.get_synsets_by_orthform(wordA)[0],
                                                 germanet.get_synsets_by_orthform(wordB)[0])

    # print(".1")
    ngd = 1 - NGD(wordA, wordB)
    # print(".2")
    context = 1 - semantic_context(wordA, wordB)
    # print(".3")
    print(wordA, wordB, vector)
    return str(distance).replace(".", ","), str(ngd).replace(".", ","),\
           str(context).replace(".", ","), str(vector).replace(".", ",")


def z4(wordA, wordB):
    vector = 1 - spacy(wordA).similarity(spacy(wordB))
    distance = 1 - semantic_distance_with_raster(germanet.get_synsets_by_orthform(wordA)[0],
                                                 germanet.get_synsets_by_orthform(wordB)[0])
    if vector + distance > 1:
        return ""

    # print(".1")
    ngd = 1 - NGD(wordA, wordB)
    # print(".2")
    context = 1 - semantic_context(wordA, wordB)
    # print(".3")
    print(wordA, wordB, vector)
    return str(distance).replace(".", ","), str(ngd).replace(".", ","),\
           str(context).replace(".", ","), str(vector).replace(".", ",")


if __name__ == '__main__':
    spacy = spacy.load(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität Quellen/project/application/creativity_test/spacy_data/de_core_news_md/de_core_news_md-3.2.0")

    germanet_file = str(__file__)[
                    0:str(__file__).rindex("word_relatedness")] + "germanet_data/germanet/GN_V160/GN_V160_XML"
    germanet = Germanet(germanet_file)

    """h: Synset = germanet.get_synset_by_id("s49774")
    o: Synset = germanet.get_synset_by_id("s83979")
    relatedness = PathBasedRelatedness(germanet=germanet, category=WordCategory.nomen, max_len=35,
                                       max_depth=20,
                                       synset_pair=(h, o))"""

    max_iterations = 1000
    iteration = 0

    """
    file format:
    ITERATION | DISTANCE | NGD | CONTEXT | VECTOR | MEDIAN | SIMILARITY  

    SIMILARITY: abs(median(all) - each_output) 

    """

    output_rows = []

    strings: list = germanet.get_lexunits_by_wordcategory(WordCategory.nomen)
    string_max = len(strings)

    output_rows.insert(0, ["Iteration", "Distance", "NGD", "Context", "Vector", "WordA", "WordB"])

    for iteration in range(max_iterations):
        print(iteration)
        wordA1: str = strings[randint(0, string_max)].orthform
        wordB1: str = strings[randint(0, string_max)].orthform
        print(output_rows[-1])
        output_rows.append(z0(wordA1, wordB1))