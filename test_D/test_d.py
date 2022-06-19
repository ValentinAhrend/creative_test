import time

import language_tool_python
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from germanetpy.germanet import Germanet
from germanetpy.path_based_relatedness_measures import PathBasedRelatedness
from germanetpy.synset import Synset, WordCategory
from nltk.tokenize import word_tokenize
import json
import spacy
from logical_algo.lingual_analysis import get_site_packages_dir, SentenceScheme, Word
from test_C.test_c import validate_input_sentence_on_grammar
from word_relatedness.word_relation import WordRelation


def high_sim(w1, w2, max0: int):
    others = 0
    others2 = 0
    for w0 in w1:
        if not w2.__contains__(w0):
            others += 1
    for w0 in w2:
        if not w1.__contains__(w0):
            others2 += 1
    return max(others, others2) <= max(len(w1), len(w2)) / max0


def start_test_d_1(list_of_sentences: list, germanet: Germanet, task_id, space):
    # validate sentences on grammar
    id0 = 0
    tool = language_tool_python.LanguageTool('de-DE')
    for sentence in list_of_sentences:
        print(sentence)
        problems = validate_input_sentence_on_grammar(sentence, tool)
        if len(problems) != 0:
            return 0, id0, problems
        id0 += 1

    clipped_task = []
    file = open(str(__file__)[
                            0:str(__file__).rindex("test_D")]+"test_D/test4-" + str(task_id) + "-methods.json", "r")
    # file = open("test4-3-methods.json", "r")
    data: list = json.load(file)['methods']
    defined = []
    print("..")
    """if task_id == 1:
    focus: list = json.load(open("test4-"+str(task_id)+"-methods-focus.json", "r"))['focus']"""
    model = Doc2Vec.load(str(__file__)[
                            0:str(__file__).rindex("test_D")]+"test_D/d2v-" + str(task_id) + ".model")
    print(".")
    for is0 in list_of_sentences:

        """max2 = use_model['#']
        data_c = []
        for data0 in test_data:
            cx = 0
            if use_model.keys().__contains__(data0.lower()):
                cx = use_model[data0.lower()]
            if cx / max2 < 0.05:
                data_c.append(data0)"""

        """data_c = []
        content = open("deu_mixed-typical_2011_100K-words.txt", "r").read()

        for word in test_data:
            try:
                indec = content.index(word)
                if indec != -1:
                    ds = content[indec-5:indec-1]
                    if ds.__contains__("\n"):
                        ds = ds[ds.index("\n")+1:]
                    print(ds)
                    if int(ds) > 200:
                        data_c.append(word)
            except Exception as e:
                print(e)

        print(data_c)"""
        print(is0)
        """x = check_algo(is0, str(__file__)[
                            0:str(__file__).rindex("test_D")]+"test_D/test4-"+str(task_id)+".json", space)
        if x[0]:
            print("found with spacy")
            defined.append((True, is0, x[1]))
            continue
        """
        def iter_0(input_sentence, ixx):
            print("iter:000")
            # to find the vector of a document which is not in training data
            test_data = word_tokenize(is0)
            v1 = model.infer_vector(test_data, epochs=100)

            # print("V1_infer", v1)

            # to find most similar doc using tags

            similar_doc = model.dv.most_similar(v1, topn=50)[ixx:]

            print(similar_doc)

            most_similar = similar_doc[0]
            print(most_similar)

            if task_id == 2:
                if int(most_similar[0]) > 343:
                    for w in similar_doc:
                        if not int(w[0]) > 343:
                            most_similar = w
                            break

                if int(most_similar[0]) > 343:
                    defined.append((False, input_sentence, 0))
                    return
            elif task_id == 3:
                if int(most_similar[0]) > 43:
                    for w in similar_doc:
                        if not int(w[0]) > 43:
                            most_similar = w
                            break

                if int(most_similar[0]) > 43:
                    defined.append((False, input_sentence, 0))
                    return
            elif task_id == 1:
                if int(most_similar[0]) > 128:
                    for w in similar_doc:
                        if not int(w[0]) > 128:
                            most_similar = w
                            break

                if int(most_similar[0]) > 128:
                    defined.append((False, input_sentence, 0))
                    return

            match = data[int(most_similar[0])]

            print(match)

            if clipped_task.__contains__(most_similar[0]):
                ms = most_similar
                for next0 in similar_doc:
                    print("check:" + str(next0))
                    if not clipped_task.__contains__(next0[0]):
                        if task_id == 2:
                            if int(next0[0]) > 344:
                                for w in similar_doc:
                                    if not int(w[0]) > 344 and not clipped_task.__contains__(w[0]):
                                        most_similar = w
                                        break

                            if int(next0[0]) > 344:
                                continue
                        elif task_id == 3:
                            if int(next0[0]) > 42:
                                for w in similar_doc:
                                    if not int(w[0]) > 42 and not clipped_task.__contains__(w[0]):
                                        most_similar = w
                                        break
                            if int(next0[0]) > 42:
                                continue
                        elif task_id == 1:
                            if int(most_similar[0]) > 128:
                                for w in similar_doc:
                                    if not int(w[0]) > 128 and not clipped_task.__contains__(w[0]):
                                        most_similar = w
                                        break
                            if int(most_similar[0]) > 128:
                                continue
                if ms != most_similar:
                    match = data[int(most_similar[0])]
                else:
                    defined.append((False, input_sentence, match))
                    return

            clipped_task.append(most_similar[0])

            match_tokens = word_tokenize(match)

            if data.__contains__(input_sentence):
                defined.append((True, input_sentence, input_sentence))
                return

            """
            check how the words of test_data are in match
            """

            matched_words = []
            matched_words_b = []
            un_matched_words = []

            """ if task_id == 1:
                focus_in_match = match_tokens[focus[int(most_similar[0])]]"""

            for token in match_tokens:
                contain = False
                for t in test_data:
                    if t.lower() == token.lower() or t.capitalize() == token.capitalize() or high_sim(t, token, 5):
                        matched_words.append(token)
                        matched_words_b.append(t)
                        contain = True
                        break
                if not contain:
                    un_matched_words.append(token)
            print(matched_words)
            if len(matched_words) > 0:
                doc = space(" ".join(matched_words))

                registered_words_in_checked = []
                for element in doc.to_json()['tokens']:
                    print(element['pos'])
                    if (element['pos'] == "VERB" or element['pos'] == "NOUN" or element['pos'] == "AUX"
                        or element['pos'] == "ADJ" or element['pos'] == "ADV") and \
                            (task_id != 3 or (element['lemma'] != "werden" and element['lemma'] != "Freund"
                                              and element['lemma'] != "Idee")):
                        print(element)
                        registered_words_in_checked.append(element)
                if len(registered_words_in_checked) == 0:
                    noun = None
                    for rn2 in registered_words_in_checked:
                        if rn2['pos'] == "NOUN":
                            noun = rn2
                            break
                    if noun:
                        doc2 = space(" ".join(test_data))

                        last_noun = None
                        for element in doc2.to_json()['tokens']:
                            print(element['pos'])
                            if element['pos'] == "NOUN":
                                last_noun = element

                        wr = WordRelation(last_noun['lemma'], noun['lemma'],
                                          germanet.get_synsets_by_orthform(last_noun['lemma'])[0],
                                          germanet.get_synsets_by_orthform(noun['lemma'])[0], space)
                        x = wr.calculate_relation(useG=True)
                        print(x)
                        if x < 0.8:
                            if ixx != 3:
                                iter_0(input_sentence, ixx + 1)
                            else:
                                defined.append((False, input_sentence, match))
                            return
                    else:
                        if ixx != 3:
                            iter_0(input_sentence, ixx + 1)
                        else:
                            defined.append((False, input_sentence, match))
                        return

                vx = float(most_similar[1])
                defined.append((vx > 0.6, input_sentence, match, vx))
            else:
                defined.append((False, input_sentence, match))

        iter_0(is0, 0)
    s = "".join([str(f[0]) for f in defined]).count("True")

    return s, defined


def check_algo(sentence: str, solution_file, spcy) -> tuple:
    solution = json.load(open(solution_file))['methods']
    dst = []
    sentence_d = spcy(sentence)

    for s in solution:
        time.sleep(0.01)
        dst.append(sentence_d.similarity(spcy(s)))
    m = max(dst)
    print(m)
    return m > 0.7, solution[dst.index(m)]


def compare_sentence_schemes(scheme_a: SentenceScheme, scheme_b: SentenceScheme) -> bool:
    """
    compare the both sentence schemes
    this method tries to find same elements and checks whether the elements have the same or similar dependency tree
    :param scheme_a: the first SentenceScheme value
    :param scheme_b: the second SentenceScheme value
    :return: a boolean whether there are similarities or not
    """
    similar = []
    for w_a in scheme_a.words:
        w_a: Word = w_a
        for w_b in scheme_b.words:
            if w_a.word == w_b.word or w_a.lemma == w_b.lemma:
                similar.append((w_a, w_b))
    if len(similar) == 0:
        return False


def train_data(task_id):
    file = open(str(__file__)[
                            0:str(__file__).rindex("test_D")]+"test_D/test4-" + str(task_id) + ".json", "r")
    data = json.load(file)['base']

    """adding external 10.000 random other sentences"""
    f12 = open("sentences10k.txt")
    for row in f12.read().split(sep="\n")[2000:7000]:
        ic = 0
        for e in row:
            ic += 1
            if not e.isnumeric():
                break
        data.append(row[ic:])

    f02 = open("test4-1-methods.json", "w")
    f02.write("")
    json.dump(data, f02)

    # exit(0)

    tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]
    max_epochs = 100
    vec_size = 100
    alpha = 0.025

    model = Doc2Vec(alpha=alpha,
                    vector_size=vec_size,
                    min_alpha=0.00025,
                    min_count=1,
                    dm=2)

    model.build_vocab(tagged_data)

    for epoch in range(max_epochs):
        print('iteration {0}'.format(epoch))
        model.train(tagged_data,
                    total_examples=model.corpus_count,
                    epochs=max_epochs)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha

    model.save("d2v-" + str(task_id) + ".model")

    """
    now generating most used words in the model dataset
    """

    """word_dict: dict = {}
    for sentence in data:
        for w in word_tokenize(sentence):
            if word_dict.keys().__contains__(w.lower()):
                word_dict[w.lower()] += 1
            else:
                word_dict[w.lower()] = 1
    word_dict["#"] = len(data)
    fil0 = open("use.json", "x")
    json.dump(word_dict, fil0)"""

    print("Model Saved")


if __name__ == '__main__':
    space = spacy.load("/Users/valentinahrend/OneDrive/! Valentin/Kreativität Quellen/project/application/creativity_test/spacy_data/de_core_news_md/de_core_news_md-3.2.0")

    """list_of_sentences_ = [
        "Man blutet",
        "Man hat Schmerzen",
        "Du bekommst eine Wunde",
        "Man muss es bandagieren",
        "Ich habe Schmerzen",
        "Ich kippe um",
        "Ich verblute",
        "Ich sterbe",
        "Mir wird schwarz vor Augen"
    ]"""
    """list_of_sentences_ = [
        "Ich übersetze das Wort",
        "Ich nutze mein Handy",
        "Ich male es",
        "Ich zeichne es.",
        "Ich mache Pantomime",
        "Ich versuche es zu erklären",
        "Ich gucke nach der Definition",
        "Ich definiere das Wort",
        "Ich schaue in einem Wörterbuch nach",
        "Ich beschreibe das Wort"
    ]"""
    list_of_sentences_ = [
        "Ich nutze mein Handy"
    ]
    """
    9   
    6
    5
    """
    germanet = Germanet(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
        "Quellen/project/application/creativity_test/germanet_data/germanet/GN_V160/GN_V160_XML")
    h: Synset = germanet.get_synset_by_id("s49774")
    o: Synset = germanet.get_synset_by_id("s83979")
    rn = PathBasedRelatedness(germanet=germanet, category=WordCategory.nomen, max_len=35, max_depth=20,
                              synset_pair=(h, o))
    print(start_test_d_1(list_of_sentences_, germanet, 1, space))

