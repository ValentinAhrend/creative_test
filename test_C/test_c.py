import math
from multiprocessing.pool import ThreadPool
from math import log
import language_tool_python
import spacy
from germanetpy.germanet import Germanet
from germanetpy.path_based_relatedness_measures import PathBasedRelatedness
from germanetpy.synset import Synset, WordCategory

from logical_algo.lingual_analysis import SentenceScheme, lingual_logic_parse, Origin
from logical_algo.exception import LogicException
from logical_algo.lingual_index import run
from logical_algo.logical_analysis import generate_logical_binding
from word_relatedness.word_relation import WordRelation


def validate_input_sentence_on_grammar(input_sentence, tool) -> list:
    print(",")
    """ 
    the location of the german LanguageTool is: /Users/valentinahrend/.cache/language_tool_python
    
    """
    problems = tool.check(input_sentence)
    if len(problems) != 0:
        print("finish")
        return problems
    else:
        print("finish")
        return []


def validate_input_sentence_on_structure(input_sentence, space):
    try:
        sentence_scheme = lingual_logic_parse(SentenceScheme(input_sentence=input_sentence,space=space), None)
        return sentence_scheme
    except LogicException as e:
        return e


def start_test_c(input_sentence, space) -> list:
    """
        This method is for the validation of the input_sentence,
    :param input_sentence: the input sentence
    :return: list of problems or exceptions, if there are no errors the sentence_scheme will be returned
    """
    tool = language_tool_python.LanguageTool('de-DE') # optimized
    problems_grammar = validate_input_sentence_on_grammar(input_sentence, tool)
    if len(problems_grammar) != 0:
        return problems_grammar
    vx = validate_input_sentence_on_structure(input_sentence, space)
    if isinstance(vx, LogicException):
        return [vx]
    return [True, vx]


def large_logic_control(sentence_scheme, space) -> bool:
    return generate_logical_binding(sentence_scheme, space)


def check_usage_of_labels(sentence_scheme: SentenceScheme, labels: list) -> [bool, list]:
    labels0 = labels.copy()
    lw = []
    for w in sentence_scheme.words:
        if labels0.__contains__(w.word) or labels0.__contains__(w.lemma):
            if labels0.__contains__(w.lemma):
                labels0.remove(w.lemma)
            else:
                labels0.remove(w.word)
            lw.append(w)
        else:
            if sentence_scheme.origin_field:
                for field in sentence_scheme.origin_field:
                    for origin in field:
                        origin: Origin = origin
                        for word in origin.origin:
                            if labels0.__contains__(word.word):
                                labels0.remove(word.word)
                                lw.append(word)
                                break
    return len(labels0) == len(labels) - 3, lw


results = []
pool = ThreadPool(3)


def score_validation(input_sentence, sentence_scheme, used_labels_str: list, winners: dict, spacy) -> tuple:
    """
    :param winners: winners: the most non fitting words for each label (from test a)
    :param input_sentence: input string
    :param sentence_scheme: sentence scheme
    :param used_labels_str: list of 3 labels as str
    :return: a score calculated using the following validation methods

    (1) Search for 'Aufzählung' with phrases
    (2) Check verb binding between the phrases
    (3) Replace labels with other labels and check the logic

    """
    global results
    global pool
    label_words = []
    if len(sentence_scheme.origin_field) != 0:
        sentence: str = input_sentence
        for of in reversed(sentence_scheme.origin_field):
            for origin in of:
                val = ""
                for elements in origin.origin:
                    val += elements.word + " "
                sentence = sentence.replace(origin.replace[0].word + " ", val)
        input_sentence = sentence
        sentence_scheme = SentenceScheme(sentence, space=spacy)
    print("input:" + str(input_sentence))
    suspect_l = 0
    root_way_x = []
    for word in sentence_scheme.words:
        if used_labels_str.__contains__(word.word):
            label_words.append(word)
    print(label_words)
    for label in label_words:

        root_back = []
        suspect_e = []

        def analyze(sy, v):
            for word in sentence_scheme.words:
                if word.id == sy.head:
                    if used_labels_str.__contains__(word.word) and v > 0:
                        if root_back[v - 1].dep == "cj" or root_back[v - 1].dep == "cd" \
                                or root_back[v - 1].dep == "cp":
                            suspect_e.append(1)
                    root_back.append(word)
                    if word.dep == "ROOT":
                        break
                    analyze(word, v + 1)

        analyze(label, 0)
        if len(suspect_e) != 0:
            suspect_l += 1
        print("root_back:" + str(root_back))
        root_way_x.append(root_back)
    if suspect_l > 0:
        print("sus:" + str(suspect_l))

    root_way_y = [[], [], []]
    print(root_way_x)
    try:
        for rq in root_way_x[0]:
            if root_way_x[1].__contains__(rq):
                root_way_y[0].append(rq)
                break
            else:
                root_way_y[0].append(rq)
    except Exception as e:
        print(e)
    try:
        for rq in root_way_x[1]:
            if root_way_x[2].__contains__(rq):
                root_way_y[1].append(rq)
                break
            else:
                root_way_y[1].append(rq)
    except Exception as e:
        print(e)
    try:
        for rq in root_way_x[0]:
            if root_way_x[2].__contains__(rq):
                root_way_y[2].append(rq)
                break
            else:
                root_way_y[2].append(rq)
    except Exception as e:
        print(e)
    verb_contain = 0
    print("root ways")
    print(root_way_y)
    for rwy in root_way_y:
        for rwy0 in rwy:
            if used_labels_str.__contains__(rwy0.word):
                break
            if rwy0.type == "VERB" or rwy0.type == "AUX":
                verb_contain += 1

    # logic change, use multithreading

    results = []
    for i in range(0, 3):
        results.append(
            pool.apply_async(func=run_logic_experiment_with_parse, args=(i, input_sentence, used_labels_str, winners, spacy)))

    results = [r.get() for r in results]

    false = 0

    for r in results:
        print(r)
        if not r:
            false += 1

    print("output")
    print(false)
    print(verb_contain)
    print(suspect_l)

    var0 = false / 3  # best: 3, worst: 0
    var1 = verb_contain / 3  # best: 1, worst: 0
    var2 = 1 / (math.pow(suspect_l + 1, 3))  # best: 1, worst: 1/9

    # total best = 1 * (3 + 1) = 4
    # total worst = (1/9) * (0 + 0) = 0

    var3 = var2 * (var0 + var1) / 4
    return var3, (false, verb_contain, suspect_l)


def run_logic_experiment_with_parse(parse_id: int, input_sentence: str, labels: list, winners: dict, space) -> bool:
    """
    threading, logic replace
    :param parse_id: the n of parce label
    :param input_sentence: the input sentence
    :param labels: the 3 labels
    :param winners: the most non fitting words for each label (from test a)
    :return: true/false (logical_algo)
    """
    current_label = labels[parse_id]
    current_winner = winners[current_label]
    try:
        print("running for " + input_sentence.replace(current_label, current_winner))
        result = run(input_sentence.replace(current_label, current_winner), space)
        print("#" + str(parse_id) + ":" + result.__str__())
    except LogicException:
        return False
    return result.score == 1


def test_c0(input_str: str, winners: dict, space) -> tuple:
    """

    :param input_str: the input sentence
    :param winners: the smallest semantic distance pair for each label in test_a
    :return: a tuple containing:
    an int:
    -1 -> no usage
    -2 -> grammar error or sentence structure error
    0...1 output of test (final_score)
    list:
        list of all scores used to calc the final score... only if int 0 >= and <= 1
    """

    labels_used = list(winners.keys())

    data = start_test_c(input_sentence=input_str, space=space)
    if isinstance(data[0], bool):
        usage = check_usage_of_labels(data[1], labels_used)
        if usage[0]:

            if large_logic_control(data[1], space):
                return score_validation(input_sentence=input_str, sentence_scheme=data[1], winners=winners,
                                        used_labels_str=labels_used, spacy=space)
            else:
                x, scores = score_validation(input_sentence=input_str, sentence_scheme=data[1], winners=winners,
                                             used_labels_str=labels_used, spacy=space)
                scores += (-0.5,)
                x = - 0.5
                if x < 0:
                    x = 0
                return x, scores
        else:
            return -1, None
    else:
        return -2, data


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
    input_str1 = "Für den Auftragskiller ist die Relativitätstheorie keine Philosophie."
    labels_used0 = ["Tapete", "Wand", "Farbe"]
    zzz = 0
    for labels00 in labels_used0:
        for labels1 in labels_used0:
            wr = WordRelation(labels1, labels00, germanet.get_synsets_by_orthform(labels1)[0], germanet.get_synsets_by_orthform(labels00)[0], spacy=space)
            zzz += wr.calculate_relation(useG=True)
    winners2 = {"Auftragskiller": "Madeira", "Philosophie": "Schatzmeister", "Relativitätstheorie": "Schatzmeister"}
    print(test_c0(input_str1, winners2, space))
    print((1 - (zzz - 3)/ 3))
#