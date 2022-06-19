import math
from multiprocessing.pool import ThreadPool

import spacy
from germanetpy.germanet import Germanet
from germanetpy.path_based_relatedness_measures import PathBasedRelatedness
from germanetpy.synset import WordCategory
from typing import List

from mechanics.mechanic import bound
from test_A.test_a import Synset
from word_relatedness.word_relation import WordRelation


class LinkedListElement:
    def __init__(self, str_value, previous_element):
        """
        init
        :param str_value: the word a str
        :param previous_element: previous element in list
        """
        self.value: str = str_value
        self.previous_element: LinkedListElement = previous_element

    def __str__(self):
        return "[value:" + self.value + ", time:" + str(self.time) + "]"

    def __repr__(self):
        return self.__str__()


def form_test_e(str_time_combination_list, sim: tuple):
    """
    creates a linked list and return the run_test_e method
    :param str_time_combination_list: the list of 3 lists of tuples of a string value (the input word)
    :param sim: (germanet, spacy)
    :return: the run_test_e return value
    """

    if len(str_time_combination_list) != 3:
        return None

    output_list = []
    total_average = 0

    for str_time_combination in str_time_combination_list:

        def next_element(index_in_list):
            if index_in_list >= 0:
                element: LinkedListElement = LinkedListElement(str_time_combination[index_in_list],
                                                               next_element(index_in_list - 1))
                return element
            else:
                return None

        if len(str_time_combination) != 0:
            base = next_element(len(str_time_combination) - 1)

            xy = run_test_e_row(base, sim)

            total_average += xy[0]

            output_list.append(xy)

    return (total_average / 3), output_list


def run_test_e_row(base, sim: tuple) -> tuple:
    """
    running the test e method
    :param sim: (germanet, relatedness)
    :param base: a linked list, each Element holds str-value, [synset-value], time and previous element
    :return: a tuple containing the final output score and a list of all scores for defining a graph
    """

    # score_list: List[float] = []
    score_list = []
    print(base.value)

    pool = ThreadPool(12)

    def iter_base(base0: LinkedListElement):
        print(base0.previous_element.value)
        wr: WordRelation = WordRelation(base0.value, base0.previous_element.value,
                                        sim[0].get_synsets_by_orthform(base0.value)[0],
                                        sim[0].get_synsets_by_orthform(base0.previous_element.value)[0], sim[1])
        # score_list.append(1 - wr.calculate_relation())
        score_list.append(pool.apply_async(func=ry, args=(wr,)))
        if base0.previous_element.previous_element:
            iter_base(base0.previous_element)

    iter_base(base)
    score_list = list(reversed([1 - sc.get() for sc in score_list]))
    # len(score_list) / 16.77 / 8 * (average)
    # len(score_list) / average_length / 8 * average
    # len(score_list) / (average_length * 8 * average)

    # len = 20
    # sum = 15
    # c = 1,33333

    # len = 20
    # sum = 1
    # c =

    # len = 20
    # sum = 100
    # c =
    # d / d/2 = d2/2

    # len(score_list) / (genereller_durch_le) * (len / sum)
    return len(score_list) / 16.77777 / 8 * (len(score_list) / sum(score_list)), score_list


def ry(wr: WordRelation):
    return 1 - wr.calculate_relation(useG=False)


if __name__ == '__main__':
    space = spacy.load(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität Quellen/project/application/creativity_test/spacy_data/de_core_news_md/de_core_news_md-3.2.0")
    germanet = Germanet(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
        "Quellen/project/application/creativity_test/germanet_data/germanet/GN_V160/GN_V160_XML")
    h: Synset = germanet.get_synset_by_id("s49774")
    o: Synset = germanet.get_synset_by_id("s83979")
    rn = PathBasedRelatedness(germanet=germanet, category=WordCategory.nomen, max_len=35, max_depth=20,
                              synset_pair=(h, o))
    """create list"""
    l0 = ["Buch", "Zeit", "Gedanke", "Luft", "Wolke", "Relativitätstheorie", "Auftragskiller", "Madeira", "Philosophie"]
    print(form_test_e([l0, l0, l0], (germanet, space)))
