from random import randint

from germanetpy.germanet import Germanet
from germanetpy.synset import WordCategory

from word_relatedness.semantic_context import semantic_context

if __name__ == '__main__':
    germanet_file = str(__file__)[
                    0:str(__file__).rindex("word_relatedness")] + "germanet_data/germanet/GN_V160/GN_V160_XML"
    germanet = Germanet(germanet_file)

    max_iterations = 100

    strings: list = germanet.get_lexunits_by_wordcategory(WordCategory.nomen)
    string_max = len(strings)

    for iteration in range(max_iterations):
        print(iteration)
        wordA1: str = strings[randint(0, string_max)].orthform
        wordB1: str = strings[randint(0, string_max)].orthform
        print(str(semantic_context(wordA1, wordB1)) + " for " + wordA1 + "/ " + wordB1)

    """
    using this return arguments
    return var0, var_e, (var0 + var_e) / 2
    
    """
