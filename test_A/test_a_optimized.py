import time
from multiprocessing.pool import ThreadPool

from germanetpy.germanet import Germanet
from word_relatedness.word_relation import WordRelation
from test_A.matrix import Matrix
from germanetpy.path_based_relatedness_measures import PathBasedRelatedness
from random import randint


def start_test_a(list_of_words, germanet: Germanet) -> tuple:
    """
    load for each word in the list all possible synsets
    :param germanet: the universal, final Germanet field
    :param list_of_words: list of words entered by the user
    :return: list of synset options and the old list of words which will be needed
    """
    global output
    output = []
    list_of_synset_lists = []
    for word in list_of_words:
        if word == "ra\ndom":
            s_id = randint(10000, 12203)
            sy = [germanet.get_synset_by_id('s'+str(s_id))]
        else:
            sy = germanet.get_synsets_by_orthform(word)
        list_of_synset_lists.append(sy)

    return list_of_synset_lists, list_of_words


pool = None
output = []


def finish_test_a(edited_list_of_synsets, list_of_words, spacy) -> tuple:
    """
    calculating the relatedness in the matrix
    :param spacy: the spacy attribute (already loaded)
    :param edited_list_of_synsets: the defined and chosen synsets
    :param list_of_words: the word list entered by the user
    :return: the matrix with the results and the final score
    """
    global pool, output
    matrix = Matrix(len(edited_list_of_synsets))
    pool = ThreadPool(len(edited_list_of_synsets))
    for i in range(0, len(edited_list_of_synsets)):
        # time.sleep(0.05), bug too early access
        output.append(pool.apply_async(func=calculate_relation, args=(edited_list_of_synsets, list_of_words, spacy, i)))
    output = [o.get() for o in output]
    a0 = 0
    a1 = 0
    # print(output)
    for row_id, row in output:
        index = 0
        # print(row)
        for element in row:
            if index + row_id != row_id:
                matrix.add(element, index + row_id, row_id)
                # print(str(row_id)+"/"+str(index + row_id))
                a1 += 1
                a0 += element
            index += 1
    return matrix.get_value(), (a0 / a1)


def calculate_relation(edited_list_of_synsets, list_of_words, spacy, i: int) -> tuple:
    """
    calculating the relation per line
    :param spacy: the spacy attribute (already loaded)
    :param edited_list_of_synsets: the defined and chosen synsets
    :param list_of_words: the word list entered by the user
    :param i: the row number
    :return: tuple of row id and the complete row of the matrix
    """
    row = []
    for j in range(0 + i, len(edited_list_of_synsets)):
        print(str(i)+"."+str(j))
        if i == j:
            v = 1.0
        else:
            wr = WordRelation(list_of_words[i], list_of_words[j], edited_list_of_synsets[i],
                              edited_list_of_synsets[j],
                              spacy)
            v = wr.calculate_relation(useG=True)
        row.append(v)
    return i, row
