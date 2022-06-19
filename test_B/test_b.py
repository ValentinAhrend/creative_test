import collections
import math

from germanetpy.germanet import Germanet
from germanetpy.synset import Synset

from word_relatedness.word_relation import WordRelation


def define_test_words(list_of_words):

    """
    the method returns the words (from test a) that will be requested in test b
    :param list_of_words: list of words from test a
    :return: 3 words that will be requested in  task b
    """

    alphabet = "abcdefghijklmnopqrstuvwxyzäöüß- /())"
    w_zz: dict = {}
    for w in list_of_words:
        q = 0
        for x in w:
            q ^= alphabet.index(x.lower())
        w_zz[(q + len(w))] = w
    w_zz = collections.OrderedDict(sorted(w_zz.items()))
    return list(w_zz.values())


def start_test_b(input_dict, germanet: Germanet, spacy):

    """
    the test_b method checks the relation between the key and the values for each word line
    then checks the absolute amount of possible words and compares with the current amount
    :param spacy: the spacy attribute (already loaded)
    :param input_dict: a dict -> {"Word from Test A": ["Similar word", "Similar word", "Similar word", ...]
    :param germanet: the universal, final Germanet field
    :return: tuple -> (final_score, {"Word from Test A": (w_final_score, average_similarity, ["Similar word", ...])})
    """

    output_dict = {}

    key_sort0 = []

    for key, value in input_dict.items():
        if key_sort0.__contains__(key):
            continue
        key_sort0.append(key)
        value_sort0 = []
        s0 = germanet.get_synsets_by_orthform(key)
        s0_synset: Synset = s0[0]
        if len(s0) == 0:
            continue
        r_val = []
        for element in value:
            if value_sort0.__contains__(element):
                continue
            value_sort0.append(element)
            s_i = germanet.get_synsets_by_orthform(element)
            if len(s_i) == 0:
                continue
            wr = WordRelation(key, element, s0_synset, s_i[0], spacy)
            x = wr.calculate_relation(useG=True)
            r_val.append(x)
        if len(r_val) == 0:
            average = 0
        else:
            average = sum(r_val) / len(r_val)
        le0 = 0
        for hy in s0_synset.direct_hypernyms:
            le0 += len(hy.direct_hyponyms)
        print(le0)
        print(average)
        print(len(r_val))
        """
        average: the average value defines the semantic relatedness between each element and the key
        le0: le0 is the sum of all hyponyms of all hypernyms of the key synset
        
        var3 = average (should be high) * (le0 / len(r_val) 
        
        -----------
        
        average = 0.95
        
        le0 = 23
        
        len(r_val) = 6
        
        var3 = 3.641
        
        -----------
        
        average = 0.95
        
        le0 = 23
        
        len(r_val) = 22
        
        var3 = 0.993
        
        -----------
        
        average = 0.7
        
        le0 = 23
        
        len(r_val) = 22
        
        var3 = 0.732
        
        -----------
        
        average = 0.7
        
        le0 = 23
        
        len(r_val) = 6
        
        var3 = 2.683
        
        -----------
        
        average = 0.3
        
        le0 = 23
        
        len(r_val) = 22
        
        var3 = 0.993
        
        function is not valid, the output is caught in two different spaces (0...1) and (1...)
        
        -> var3 = len(r_val) * (average) / l0
        
        -----------
        
        average = 0.7
        
        le0 = 23
        
        len(r_val) = 6
        
        var3 = 0.183
        
        ------------
        
        average = 0.9
        
        le0 = 23
        
        len(r_val) = 22
        
        var3 = 0.861
        
        ------------
        
        the value is too low for only having one left and a avaerage score of 0.9
        
        adjustment: adding log with base 2
        
        var3 = log2+1-average(len(r_val) * average) / log2(l0)
        
        ------------
        
        average = 0.9
        
        le0 = 23
        
        len(r_val) = 22
        
        var3 = 0.95
        
        ------------
        
        average = 0.9
        
        le0 = 23
        
        len(r_val) = 6
        
        var3 = 0.538
        
        ------------
        
        average = 0.7
        
        le0 = 23
        
        len(r_val) = 6
        
        var3 = 0.458
        
        ------------
        
        average = 0.7
        
        le0 = 23
        
        len(r_val) = 22
        
        var3 = 0.872
        
        -----------
        
        perfect!
        
        """

        if len(r_val) == 0:
            var3 = 0
        else:
            var3 = math.log(len(r_val) * average, 2) / math.log(le0)

        output_dict[key] = (var3, average, value)

    average0 = 0

    for val in output_dict.values():
        average0 += val[0]

    average0 = average0 / len(output_dict.values())

    return average0, output_dict
