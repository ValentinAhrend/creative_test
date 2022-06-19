import requests

from logical_algo.lingual_analysis import Sentence
from logical_algo.lingual_analysis import SentenceScheme, lingual_logic_parse, Word, Origin
from test_A import ssession
from test_A.test_a import __get_synsets, __get_relation_for_synset, Relation


def generate_logical_binding(scheme: SentenceScheme, space) -> bool:
    sentence: Sentence = scheme.sentences[0]
    """generating pairs for lookup process"""
    pairs = []
    """
    all objects combined with their source verb
    verb combined with subject
    subject combined with subject
    object combined with object
    """

    """example:

    Der Apfel ist sauer

    sauer - ist
    sauer -Apfel

    """

    main_subject = None
    for block in sentence.blocks:
        if block.t == 1:
            for w2 in block.data:
                if w2.dep == "sb" or w2.dep == "ep":
                    main_subject = w2
                    break
    pairs.append([main_subject, scheme.words[int(scheme.root_id)]])
    for block in sentence.blocks:
        if block.t == 0 or block.t == 3 or block.t == 4:
            for w2 in block.data:
                if (w2.dep == "nk" or
                        w2.dep == "oa" or w2.dep == "mo" or w2.dep == "og" or w2.dep == "og" or w2.dep == "op" or w2.dep == "da" or
                        w2.dep == "op" or (w2.dep == "pd" and w2.morph.keys().__contains__("Case"))) \
                        and w2.type == "NOUN":
                    pairs.append([w2, main_subject])
    """print(sentence.blocks)
    for block in sentence.blocks:
        if block.t == 0:
            main_object_w = None
            for w2 in block.data:
                if (
                        w2.dep == "oa" or w2.dep == "mo" or w2.dep == "og" or w2.dep == "og" or w2.dep == "op" or w2.dep == "da" or
                        w2.dep == "op" or (w2.dep == "pd" and w2.morph.keys().__contains__("Case"))) \
                        and w2.type != "VERB" and w2.type != "AUX":
                    main_object_w = w2
                    break
            root = sentence.words[int(main_object_w.head)]
            pairs.append((main_object_w, root))
        elif block.t == 1:
            main_subject = None
            for w2 in block.data:
                if w2.dep == "sb" or w2.dep == "ep":
                    main_subject = w2
                    break
            root = sentence.words[int(main_subject.head)]
            pairs.append((main_subject, root))"""
    """ elif block.t == 3:
            print(block.name)
            main_object_w = None
            for w2 in block.data:
                if (
                        w2.dep == "nk" or w2.dep == "oa" or w2.dep == "mo" or w2.dep == "og" or w2.dep == "og" or w2.dep == "op" or w2.dep == "da" or
                        w2.dep == "op" or (w2.dep == "pd" and w2.morph.keys().__contains__("Case"))) \
                        and w2.type != "VERB" and w2.type != "AUX" and w2.type != "ADP":
                    main_object_w = w2
                    break
            if main_object_w is not None:
                root = sentence.words[int(main_object_w.head)]
                pairs.append((main_object_w, root))"""

    print("pairs" + str(pairs))

    """TAsk: Create web scraper that loads sentences from: 
    https://corpora.uni-leipzig.de/de/res?corpusId=deu_wikipedia_2021&word=Haus and searches for the paired with 
    word. If it is found, the pair is logical. If it is not found several steps have to be done before it can be 
    declared not logical The top-word of the pair word needs to be generated. (Wolkenkratzer = Haus) and the lookup 
    starts again. If the word is in direct binding there is nothing to do, to make it not logical... 

    Attention: If the pair word is found, the sentence has to be load into a sentence scheme, where it will be checked,
    whether the word has the same label (like "AccusativeObject") as the pair word

    """

    target_ulr = ["https://corpora.uni-leipzig.de/de/webservice/index?limit=50&offset=",
                  "&corpusId=deu_typical-mixed_2018&action=loadExamples&word="]

    success_h = True
    for pair in pairs:

        if not success_h:
            break
        good_sentences = []
        sentences = []
        success0 = False

        for obj in pair:

            found = 0
            n = 0
            while True:
                if n == 1000 or found > 9:
                    break
                n += 50
                pair_w = pair[(pair.index(obj) + 1) % 2]

                url = target_ulr[0] + str(n) + target_ulr[1] + obj.word
                out = requests.get(url)
                h1 = "<li><span>"
                h2 = '<span class="highlight">'
                h3 = "</span>"
                h4 = "</span> ("

                # create sentences
                x = str(out.content.decode('utf-8'))
                while x.__contains__(h1):
                    index = x.index(h1)
                    index2 = x.index(h4, index)
                    sub = x[index + len(h1): index2]
                    try:
                        s = sub[0:sub.index(h2)] + obj.word + sub[sub.index(h3) + len(h3):]
                    except ValueError as ee:
                        print(ee)
                        break
                    if not s.endswith("."):
                        s = s[:-1]
                    sentences.append(s)
                    x = x[index2:]

                    if s.__contains__(pair_w.word) or ((pair_w.type == "VERB" or pair_w.type == "AUX")
                                                       and s.__contains__(pair_w.lemma)):
                        good_sentences.append(s)
                        found += 1
        print(len(good_sentences))
        print(good_sentences)
        if len(good_sentences) == 0:
            print("none")
            """pair_x = pair
            hyper_form1 = get_hyper_form(pair[0])
            hyper_form2 = get_hyper_form(pair[1])
            pair = (hyper_form1, hyper_form2)
            complete_sentence = ""
            for w in scheme.sentences[0].words:
                if w.word == pair_x[0]:
                    complete_sentence += " " + hyper_form1
                elif w.word == pair_x[1]:
                    complete_sentence += " " + hyper_form2
                else:
                    complete_sentence += " " + w.word
            scheme_y = None
            try:
                scheme_y = SentenceScheme(complete_sentence)
            except logical_algo.exception.LogicException as e:
                print(e)
            finally:
                if not scheme_y:
                    continue
                for obj in pair:
                    found = 0
                    n = 0
                    while True:
                        if n == 1000 or found > 3:
                            break
                        n += 50
                        pair_w = pair[(pair.index(obj) + 1) % 2]
                        url = target_ulr[0] + str(n) + target_ulr[1] + obj.word
                        out = requests.get(url)
                        h1 = "<li><span>"
                        h2 = '<span class="highlight">'
                        h3 = "</span>"
                        h4 = "</span> ("
                        # create sentences
                        x = str(out.content.decode('utf-8'))
                        while x.__contains__(h1):
                            index = x.index(h1)
                            index2 = x.index(h4, index)
                            sub = x[index + len(h1): index2]
                            print(sub)
                            s = sub[0:sub.index(h2)] + obj.word + sub[sub.index(h3) + len(h3):]
                            if not s.endswith("."):
                                s = s[:-1]
                            sentences.append(s)
                            x = x[index2:]
                            if s.__contains__(pair_w.word) or ((pair_w.type == "VERB" or pair_w.type == "AUX")
                                                               and s.__contains__(pair_w.lemma)):
                                good_sentences.append(s)
                                found += 1
                if len(good_sentences) != 0:
                    for good_sentence in good_sentences:
                        try:
                            scheme_x = lingual_logic_parse(SentenceScheme(good_sentence), None)
                            success = __compare_schemes(scheme_y, scheme_x, pair[0], pair[1])
                            if success:
                                success0 = True
                        except logical_algo.exception.LogicException as eee:
                            print(eee)"""
        else:
            for good_sentence in good_sentences:
                try:
                    scheme_x = lingual_logic_parse(SentenceScheme(good_sentence, space), None)
                    success = __compare_schemes(scheme, scheme_x, pair[0], pair[1])
                    print(success)
                    if success:
                        success0 = True
                        break
                except Exception as e:
                    print(e)
        if not success0:
            success_h = False
            break

    return success_h


def __compare_schemes(scheme0: SentenceScheme, new_scheme: SentenceScheme, match_word: Word, target_word: Word) -> bool:
    """This method tries to compare two sentences by their schemes """
    """displacy.serve(new_scheme.doc, port=5002)
    displacy.serve(scheme0.doc, port=5002)
    """
    new_match_word = None

    # search for match word in new_scheme
    for w in new_scheme.words:
        if w.word == match_word.word or w.lemma == match_word.lemma or \
                (w.type == "VERB" and match_word.type == "VERB" and
                 (w.lemma.__contains__(match_word.lemma) or match_word.lemma.__contains__(w.lemma))):
            new_match_word = w
            break
    # compare both objects

    new_target_word = None

    for w in new_scheme.words:
        if w.word == target_word.word or w.lemma == target_word.lemma or \
                (w.type == "VERB" and target_word.type == "VERB" and
                 (w.lemma.__contains__(target_word.lemma) or target_word.lemma.__contains__(w.lemma))):
            new_target_word = w
            break

    if not new_target_word or not new_match_word:
        if new_scheme.origin_field.__len__() > 0 and new_scheme.origin_field[-1]:
            origins = new_scheme.origin_field
            for origin in origins[-1]:
                origin: Origin = origin
                for w in origin.origin:
                    if w.word == match_word.word or w.lemma == match_word.lemma or \
                            (w.type == "VERB" and match_word.type == "VERB" and
                             (w.lemma.__contains__(match_word.lemma) or match_word.lemma.__contains__(w.lemma))):
                        new_match_word = w
                    elif w.word == target_word.word or w.lemma == target_word.lemma or \
                            (w.type == "VERB" and target_word.type == "VERB" and
                             (w.lemma.__contains__(target_word.lemma) or target_word.lemma.__contains__(w.lemma))):
                        new_target_word = w
                    new_scheme.words.extend(origins)

            if not new_match_word:
                return False
        else:
            return False

    # check binding to target word

    # old

    root_way_a = []  #
    root_way_b = []  # 7,1,2,4,6,5

    root_way_a_2 = []
    root_way_b_2 = []

    def check(current, a):
        if current and not (current.dep == "ROOT" or current.head == current.id):

            if a == 0:
                root_way_a.append(int(current.id))
            elif a == 1:
                root_way_b.append(int(current.id))
            elif a == 2:
                root_way_a_2.append(int(current.id))
            elif a == 3:
                root_way_b_2.append(int(current.id))

            if a < 2:
                next2 = scheme0.sentences[0].words[int(current.head)]
            else:
                next2 = new_scheme.sentences[0].words[int(current.head)]
            check(next2, a)

    check(match_word, 0)
    check(target_word, 1)

    check(new_match_word, 2)
    check(new_target_word, 3)

    root_way_c = []
    root_way_c_2 = []

    for rq in root_way_a:
        if root_way_b.__contains__(rq):
            break
        else:
            root_way_c.append(scheme0.sentences[0].words[rq].dep)

    for rq in root_way_a_2:
        if root_way_b_2.__contains__(rq):
            break
        else:
            root_way_c_2.append(new_scheme.sentences[0].words[rq].dep)

    return root_way_c[0] == root_way_c_2[0]


def get_hyper_form(word: Word):
    credentials = ssession.get_credits()
    id0 = ssession.generate_cookie_id(credentials=credentials, force=False)
    sy = __get_synsets(word, id0, credentials)[0]
    sz = __get_relation_for_synset(sy, id0, credentials)
    relation: Relation = sz.relations[0]
    return relation.next_headers[0]







