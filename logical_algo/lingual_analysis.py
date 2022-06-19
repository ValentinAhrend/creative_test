import json
import site
import uuid
import spacy
import time
from spacy import displacy

from logical_algo.exception import LogicException

start_time = 0


def get_site_packages_dir():
    return [p for p in site.getsitepackages()
            if "site-packages" in p][0]


class SentenceScheme:
    def __init__(self, input_sentence, space):
        if not input_sentence:
            return
        global start_time
        if start_time == 0:
            start_time = int(time.time_ns().__str__())
        # print("SentenceScheme via " + input_sentence)
        '''as a next step, we have to split the sentence into words in different Blocks'''

        self.spacy = space

        self.root_2_wrappers = None

        self.doc = self.spacy(input_sentence)

        self.origin_field = []

        """words = tokenize(doc)
        words = a_lemma(words, doc)
        words = b_pos(words, doc)"""

        """
        Next step is the generation or inclusion of the dep-tree of spacy.
        With this tree, the logical combination-sources should be set.    
        """

        """noun_chunk_wrapper = []

        for ncv in doc.noun_chunks:
            wrapper = WordWrapper()
            for nvcc in ncv:

                target = None

                for wx in words:
                    wx: Word = wx
                    if wx.word == str(nvcc):
                        target = wx

                if not target:
                    print(words)
                    raise Exception("!")

                wrapper.merge_single_word(target)
                words = words[words.index(target) + 1:]
            noun_chunk_wrapper.append(wrapper)"""

        """for token in doc:
            print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                  token.shape_, token.is_alpha, token.is_stop)"""
        tokens = self.doc.to_json()['tokens']
        self.words = []

        root = None

        nc: list = list(self.doc.noun_chunks)
        nc1 = []
        for n in nc:
            nc1.append(str(n))
        nc = nc1

        self.noun_chunks = []

        for token in tokens:
            original_word = input_sentence[int(token['start']):int(token['end'])]

            w = Word(token, original_word)
            if w.dep == "ROOT":
                root = w
            self.words.append(w)
        problem_solver = ProblemSolver()
        c = problem_solver.check(self.words)
        if c != 0:
            sent = problem_solver.handle_problem(c)
            sentence = ""
            for w9 in self.words:
                sentence += w9.word
                sentence += " "
            if sent != sentence:
                self.__init__(sent)
                return
        # words generated

        """The sentence generation:
        1. split the words by ',' 
        2. now check whether the split part is a real sentence"""

        sentence_parts = []
        curr_part = []
        sb_count = 0
        c0 = 0
        for w99 in self.words:
            curr_part.append(w99)
            if w99.dep == "sb":
                sb_count += 1
            if w99.word == "," or w99.word == "." or w99.type == "SCONJ":
                if not (w99.word == "," and not self.words[c0 + 1].type.__contains__("CONJ")):
                    sentence_parts.append(curr_part)
                    curr_part = []
            c0 += 1

        if sb_count > 1:
            raise LogicException(ex_type=4)

        if len(sentence_parts) == 0:
            sentence_parts.append(self.words)

        self.sentences = []

        # print(len(sentence_parts))

        main_words = []

        for cp in sentence_parts:
            # check the conjunction
            if cp[0].type == "SCONJ":
                sent = Sentence(words=cp, type_=1, name="UnknownSub")
                self.sentences.append(sent)
            else:
                '''get pos of verb'''
                last = cp[-1]
                if last.tag.startswith("$"):
                    last = cp[-2]
                if last.type == "VERB" or last.type == "AUX":
                    if last.type == "VVIZU" or (
                            len(cp) > int(last.id) + 1 and cp[int(last.id) - 1].type == "PTKZU"):
                        sent = Sentence(words=cp, type_=1, name="InfinitiveSub")
                        self.sentences.append(sent)
                        continue
                    elif last.dep == "rc":
                        sent = Sentence(words=cp, type_=1, name="RelativeSub")
                        self.sentences.append(sent)
                        continue

                if main_words.__len__() > 0 and int(main_words[-1].id) + 2 >= int(cp[0].id):
                    sent = Sentence(words=cp, type_=1, name="IrregularSub")
                    self.sentences.append(sent)
                    continue

                if cp[-1].word == ",":
                    cp = cp[0:-1]
                main_words.extend(cp)

        self.sentences.append(Sentence(words=main_words, type_=0, name="Main"))
        if len(self.sentences) > 1:
            """Due to the problem of uncontrollable context issues the logic analysis will be only possible for one 
            main sentence """
            raise LogicException(ex_type=4)

        if not root or (root.type != "AUX" and root.type != "VERB"):
            root_n = None
            for w00 in self.words:
                if w00.dep == "sb":
                    root_n = self.words[int(w00.head)]
            if root_n:
                root = root_n
            else:
                raise LogicException(ex_type=1, json_data_str=json.dumps(self.doc.to_json()))
        # the next step is to get all words headed (head) with root
        """self.root_2_wrappers = []"""
        self.root_id = root.id
        """ for w in self.words:
            if w.head == self.root_id and not w.tag.startswith("$"):
                wrapper = WordWrapper()
                if w.id == self.root_id:
                    wrapper.merge_single_word(root, root.dep)
                else:
                    wrapper.merge_words(w, root, w.dep)

                    def iter_(wrapper_) -> WordWrapper:
                        wrapper3 = []
                        for w0 in self.words:
                            if w0.head == wrapper_.id and w0.id != wrapper_.id:
                                wrapper2 = WordWrapper()
                                wrapper2.merge_words(w0, self.words[int(wrapper_.id)], w0.dep)
                                wrapper2 = iter_(wrapper2)

                                if isinstance(wrapper2.src[0], Word) and isinstance(wrapper2.src[1], Word):
                                    if nc.__contains__(wrapper2.src[0].word):
                                        self.noun_chunks.append(wrapper2.src[0])
                                    elif nc.__contains__(wrapper2.src[1].word):
                                        self.noun_chunks.append(wrapper2.src[1])
                                    elif nc.__contains__(wrapper2.src[0].word + " " + wrapper2.src[1].word):
                                        self.noun_chunks.append(wrapper2)

                                wrapper3.append(wrapper2)
                        if wrapper3.__len__() > 0:
                            wrapper_.include_wrapper(wrapper3)
                        return wrapper_

                    wrapper = iter_(wrapper)
                self.root_2_wrappers.append(wrapper)
        print(self.words)"""

        """There is a logical syntax exception found in the doc generation process. Any personal pronoun is used in a 
        nk combination to a real noun. This causes that the personal pronoun will be used like a DET pronoun (e.g. 
        possessive). To solve this problem we need to build a ProblemSolver that handles the error and solves it. It 
        has to generate a json list, where every operated sentence is listed, to check its validity """

        if 22 == 2:
            displacy.serve(self.doc, port=5002)

    def rebuild_using_list_only(self):

        root = None

        nc: list = list(self.doc.noun_chunks)
        nc1 = []
        for n in nc:
            nc1.append(str(n))
        nc = nc1
        self.noun_chunks = []
        problem_solver = ProblemSolver()
        c = problem_solver.check(self.words)
        if c != 0:
            sent = problem_solver.handle_problem(c)
            self.__init__(sent)
            return
        # words generated

        """The sentence generation:
        1. split the words by ',' 
        2. now check whether the split part is a real sentence"""

        sentence_parts = []
        curr_part = []
        sb_count = 0
        for w99 in self.words:
            curr_part.append(w99)
            if w99.dep == "sb":
                sb_count += 1
            if w99.word == "," or w99.word == "." or w99.type == "SCONJ":
                sentence_parts.append(curr_part)
                curr_part = []

        if sb_count > 1:
            raise LogicException(ex_type=4)

        if len(sentence_parts) == 0:
            sentence_parts.append(self.words)

        self.sentences = []

        # print(len(sentence_parts))

        main_words = []

        for cp in sentence_parts:
            # check the conjunction
            if cp[0].type == "SCONJ":
                sent = Sentence(words=cp, type_=1, name="UnknownSub")
                self.sentences.append(sent)
            else:
                '''get pos of verb'''
                last = cp[-1]
                if last.tag.startswith("$"):
                    last = cp[-2]
                if last.type == "VERB" or last.type == "AUX":
                    if last.type == "VVIZU" or (
                            len(cp) > int(last.id) + 1 and cp[int(last.id) - 1].type == "PTKZU"):
                        sent = Sentence(words=cp, type_=1, name="InfinitiveSub")
                        self.sentences.append(sent)
                        continue
                    elif last.dep == "rc":
                        sent = Sentence(words=cp, type_=1, name="RelativeSub")
                        self.sentences.append(sent)
                        continue

                if main_words.__len__() > 0 and int(main_words[-1].id) + 2 >= int(cp[0].id):
                    sent = Sentence(words=cp, type_=1, name="IrregularSub")
                    self.sentences.append(sent)
                    continue

                if cp[-1].word == ",":
                    cp = cp[0:-1]
                main_words.extend(cp)

        self.sentences.append(Sentence(words=main_words, type_=0, name="Main"))

        if len(self.sentences) > 1:
            """Due to the problem of uncontrollable context issues the logic analysis will be only possible for one 
            main sentence """
            raise LogicException(ex_type=4)

        if not root or (root.type != "AUX" and root.type != "VERB"):
            root_n = None
            for w00 in self.words:
                if w00.dep == "sb":
                    root_n = self.words[int(w00.head)]
            if root_n:
                root = root_n
            else:
                raise LogicException(ex_type=1, json_data_str=json.dumps(self.doc.to_json()))
        # the next step is to get all words headed (head) with root
        """self.root_2_wrappers = []"""
        self.root_id = root.id

    def __str__(self):
        try:
            return json.dumps({
                'words': str(self.words),
                "constellation_root_id": self.root_id
            })
        except AttributeError:
            return "{}"


'''The 1. Definition for a single Word'''


class Word:

    def __init__(self, token, original_word):
        if not original_word:
            return
        self.word: str = original_word
        self.id = str(token['id'])
        self.lemma = str(token['lemma'])
        self.position = (int(token['start']), int(token['end']))
        self.tag: str = token['tag']
        self.type: str = token['pos']
        self.morph = str(token['morph'])
        morph = {}
        for split in self.morph.split("|"):
            if not split:
                continue
            value: str = split[split.index('=') + 1:-1]
            if value.isnumeric():
                value: int = int(value)
            morph[split[0:split.index("=")]] = value
        self.morph = morph
        self.dep = token['dep']
        self.head = str(token['head'])
        self.parameters = Parameters()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if 2 % 3 == 0:
            return self.word
        else:
            return "[word: '" + self.word + "', id: '" + self.id.__str__() + "', " + self.lemma + ", " + \
                   self.position.__str__() + ", " + self.tag + ", " + self.type + ", " + self.morph.__str__() + ", " + \
                   self.dep + ", " + self.head.__str__() + ", " + self.parameters.__str__() + "] "

    """
    Word Parameter List:
    
    - "relation_to_other_word" -> id of the other word this word is related to.
    
    
    
    """

    def set_parameter(self, key, value):
        self.set_specific_parameter(group_name=None, key=key, value=value)

    def set_specific_parameter(self, group_name, key, value):
        self.parameters.add_param(group=group_name, key=key, value=value)


'''Parameter Class is a simple group-sorted mapping'''


class WordWrapper:

    def __init__(self):
        self.id = -1
        self.src = []
        self.type = 0
        self.dep = "?"

    """
        When merging please note that the dep parameter should be the dep of w1 to w2
    """

    def merge_words(self, word1, word2, dep):
        """if self.type < 0:
            return"""
        self.merge_single_word(word1, None)
        self.merge_single_word(word2, dep)

    def merge_single_word(self, word, dep):
        """if self.type < 0:
            return"""
        if len(self.src) > 1:
            return
        if dep:
            self.dep = dep
        self.type = 1
        self.src.append(word)
        self.id = self.src[0].id

    def merge_wrap(self, wapper1, wapper2, dep):
        """if self.type > 0:
            return"""
        self.dep = dep
        self.merge_single_wrapper(wapper1, None)
        self.merge_single_wrapper(wapper2, dep)

    def merge_single_wrapper(self, wrapper, dep):
        """if self.type > 0:
            return"""
        if len(self.src) > 1:
            src_x = []
            for s in self.src:
                if s.id == wrapper.src[-1].id:
                    '''replace element'''
                    src_x.append(wrapper)
                else:
                    src_x.append(s)
            if len(src_x) != len(self.src):
                self.src = src_x
            else:
                return
        self.type = -1
        if dep:
            self.dep = dep
        self.src.append(wrapper)
        self.id = self.src[0].id

    def include_wrapper(self, wrapper):
        self.type = -1
        self.src[0] = wrapper
        if isinstance(wrapper, list):
            self.id = wrapper[0].id
        else:
            self.id = wrapper.id

    def __repr__(self):
        if 2 % 2 == 0:
            return str(self.src)
        else:
            return "[id: '" + str(self.id) + "', src: " + str(self.src) + ", type: '" + str(self.type) + "'"

    def __str__(self):
        return self.__repr__()


class Parameters:

    def __init__(self):
        self.groups = {}

    def __str__(self):
        return json.dumps(self.groups)

    def add_group(self, key) -> bool:
        if self.groups.keys().__contains__(key):
            return False
        self.groups[key] = []
        return True

    def check_group0(self):
        if len(self.groups.keys()) == 0:
            self.add_group("0")

    def add_param(self, group, key, value):
        self.check_group0()
        if group is None:
            group = "0"
        l0 = list(self.groups[group])

        r0 = []

        for l1 in l0:
            if l1['k'] != key:
                r0.append(l1)

        r0.append({'k': key, 'v': value})
        self.groups[group] = r0

    def get_param(self, group, key):
        if group is None:
            group = "0"
        if self.groups.keys().__contains__(group):
            l0: list = self.groups[group]
            for l1 in l0:
                if l1['k'] == key:
                    return l1['v']
        return None


'''Block is a part of a sentence'''


class Block:
    block_q = [
        "Object",
        "Subject",
        "Predicate",
        "Adverb",
        "Modifier",
        "Particle",
        "Addition",
    ]

    def __init__(self, type_: int, name: str, word: list):
        self.title = self.block_q[type_]
        self.t = type_
        self.data = word
        self.name = name
        self.context = -1

    def add_context(self, context: int):
        self.context = context

    def __str__(self):
        return "....BLOCK/" + self.title + "/" + self.name + "/" + str(self.data) + "....0"

    def __repr__(self):
        return self.__str__()


'''The ProblemSolver handles Syntax exeptions in the dependency tree'''


class ProblemSolver:
    """EX#001: Usage of personal pronoun in nk binding to NN as a DET, example:
        -> Morgen essen meine Mutter und ich Kuchen...
        Subject: Morgen (WRONG)
        dependency:

        essen -> oa Mutter -> nk meine -> cd und -> cj Kuchen -> nk ich (is PRON but as DET, like 'meine')
    """

    """EX#002: Incorrect Verb binding and subject generation."""

    def __init__(self):

        self.problem = None
        self.words = []
        self.subject = None

    def check(self, words) -> int:
        """checking for EX#001"""

        # print("check")
        for w in words:
            w: Word = w
            if w.dep == "nk":
                if w.type == "PRON" and w.tag == "PPER" and int(w.head) > int(w.id):
                    self.problem = w
                    self.words = words
                    return 1
        """checking for EX#002"""
        return 0

    def check2(self, words, subject):
        if len(subject) == 1:
            self.subject = subject
            root_id = int(subject[0].head)
            for w9 in words:
                if int(words[root_id].head) == int(w9.id) and root_id != int(w9.id):
                    if w9.type == "CCONJ":
                        for w10 in words:
                            if int(w10.id) == int(w10.head):
                                if w10.type != words[root_id].type:
                                    self.words = words
                                    self.problem = w10
                                    print("problem : " + str(self.problem))
                                    return 2
        return 0

    def handle_problem(self, n) -> str:
        if self.problem:
            if n == 1:
                return self.handle_problem_ex001()
            elif n == 2:
                return self.handle_problem_ex002()
        else:
            return ""

    def handle_problem_ex001(self) -> str:
        # print("solve:")
        """1. get the problem and define the dependency tree back. The output should be somthing like [None, None, meine, Mutter, und, ich, Kuchen].
        2. the next step is to eliminate the 'Kuchen' so the nk binding reference.
        3. then the type will be turned, using the conjunctions.
        4. the list will be returned as a sentence.
        5. the document needs to be rebuild via the list"""
        try:
            word_list_empty: list = [None] * len(self.words)

            word_list_empty[int(self.problem.id)] = self.problem

            def get_back(current_w, ct, before):
                current_w: Word = current_w

                for wx in self.words:
                    wx: Word = wx
                    if (int(wx.id) == int(current_w.head) or (ct > 1 and int(wx.head) == int(current_w.id))) and int(
                            wx.head) != int(wx.id) and before != wx:
                        word_list_empty[int(wx.id)] = wx
                        # print(wx.word)
                        get_back(wx, ct + 1, current_w)

            get_back(self.problem, 0, None)

            # print(word_list_empty)

            # 1 step complete

            word_list_empty[int(self.problem.head)] = None

            w02 = []
            for wxx in word_list_empty:
                if wxx:
                    w02.append(wxx)

            start = w02[0].position[0]
            end = w02[-1].position[1]

            # 2 step complete

            # print(word_list_empty)

            if word_list_empty[int(self.problem.id) - 1].type == "CCONJ":
                # print("the list is able to change")

                # getting the first part

                first_element = []

                for xx in w02:
                    if xx.dep == 'cd':
                        break
                    else:
                        first_element.append(xx)

                for ssf in first_element:
                    word_list_empty[int(ssf.id)] = None

                word_list_empty[int(first_element[0].id)] = self.problem

                word_list_empty[int(self.problem.id)] = first_element[0]

                if len(first_element) > 1:
                    v0 = 1
                    for f0 in first_element[1:]:
                        word_list_empty.append(None)
                        word_list_empty[int(self.problem.id) + v0] = f0
                        v0 += 1
            else:
                raise Exception("Problem EX#001")

            w01 = []
            for wxx in word_list_empty:
                if wxx:
                    w01.append(wxx)
            word_list_empty = w01

            # 3 step complete

            sentence = ""
            for w9 in self.words:
                sentence += w9.word
                sentence += " "

            new_sentence = ""
            for w8 in word_list_empty:
                new_sentence += w8.word
                new_sentence += " "

            out = sentence[0:start] + new_sentence + sentence[1 + end:]
            return out
        except AttributeError as e:
            print(e)
            sentence = ""
            for w9 in self.words:
                sentence += w9.word
                sentence += " "
            return sentence

    def handle_problem_ex002(self) -> str:
        # print("need help")
        """1. add the conjunction binding to the subject instead of the informal or formal ROOT verb
        2. return new word list"""

        words_str = []
        for ww in self.words:
            words_str.append(ww.word)

        new_sentence = " ".join(words_str[0:int(self.subject[-1].id) + 1]) + " und sie " + " ".join(
            words_str[int(self.subject[-1].id) + 1:])

        return new_sentence


def lingual_logic_parse(sentence_scheme, origin_subject):
    # print("LLP")
    sentence_scheme: SentenceScheme = sentence_scheme
    """Reformatting the sentence_scheme into a block scheme
    the root verb becomes just a member of the block scheme as the sb or oa..
    the goal is to include mulitple roots dependent and independent
    """

    """the first step is to load the direct realtions via binding phrases (like CCONJ) of the ROOT"""

    r_id = int(sentence_scheme.root_id)

    root = sentence_scheme.words[r_id]

    root_field = [root]

    i = 1
    j = 0
    while int(sentence_scheme.words[r_id + i].head) == (i + r_id - 1 - j) \
            and (sentence_scheme.words[r_id + i].dep == "cj" or sentence_scheme.words[r_id + i].dep == "cd"
                 or sentence_scheme.words[r_id + i].dep == "punct"):
        root_field.append(sentence_scheme.words[r_id + i])
        if sentence_scheme.words[r_id + i].dep == "punct":
            j += 1
        else:
            j = 0
        i += 1

    # print(root_field)

    """We have now the root_field list, that displays the real verb root."""

    """We need a subject rooted system, because if there are two separated verbs, it can be an enumeration or 
    multiple sentence blocks. If there are two separated subjects, there are always two main sentences. """

    'NEW: Generate subject... for each sub and main sentence'

    sentences_x = []

    for sentence in sentence_scheme.sentences:

        subject = None

        for w in sentence.words:
            if w.dep == "sb":
                subject = w
                break

        if not subject:
            for w in sentence.words:
                if w.dep == "ep":
                    """Undefined Passive Phrase using 'es'"""
                    subject = w
                    break

        if not subject:
            # print("no subject")
            # displacy.serve(sentence_scheme.doc, port=5002)
            raise LogicException(ex_type=2, json_data_str={})

        s_id = int(subject.id)
        sub = [None] * len(sentence_scheme.words)

        # 1. search for head = s_id in total sentence

        exception_bool = False

        for w9 in sentence.words:
            if int(sentence_scheme.words[r_id].head) == int(w9.id) and r_id != int(w9.id):
                if w9.type == "CCONJ":
                    for w10 in sentence_scheme.words:
                        if int(w10.id) == int(w10.head):
                            if w10.type != sentence_scheme.words[r_id].type:
                                exception_bool = True

        def analyse(wo: Word, last_type: str):
            for w0 in sentence_scheme.words:
                if int(w0.head) == int(wo.id) or int(w0.id) == int(wo.head) or (
                        exception_bool and not last_type and int(root.head) == int(w0.id) and int(
                    w0.id) != r_id and w0.type == "CCONJ"):
                    if w0.dep == "cd" or w0.dep == "cj" or w0.dep == "nk" or w0.dep == "mo" or w0.dep == "ag" or w0.dep == "ROOT":
                        if w0.type != last_type and (
                                w0.type == "CCONJ" or w0.type == "PRON" or w0.type == "NOUN" or w0.type == "DET"
                                or w0.type == "ADJ" or w0.type == "ADV"):
                            if not sub[int(w0.id)]:
                                sub[int(w0.id)] = w0
                                analyse(w0, w0.type)
                            # print(sub)
                        else:
                            if w0.type == "VERB":
                                # print("-" + w0.head)
                                # bug fix EX#002 sub[int(w0.head)] = None
                                sub[int(w0.id)] = None

        analyse(subject, None)
        sub[s_id] = subject
        subject = []
        for s in sub:
            if s:
                subject.append(s)

        if subject[-1].type == "CCONJ":
            subject = subject[0:-1]

        # print("subject: " + str(subject))
        if origin_subject:
            if len(sentence_scheme.origin_field) == 0:
                sentence_scheme.origin_field.append([])

            o = Origin()
            o.origin = origin_subject
            o.replace = subject
            sentence_scheme.origin_field[-1].append(o)

        """the next step is to find the verbs connected to the subject. The first connected verb is always the ROOT dep 
        verb. But there could be more like in this example: >> 'Ich gehe an die frische Luft und trinke ein Tee.' this 
        sentence contains the subject >> 'Ich' and the predicates 'gehe' and 'trinke'. These two predicates (verbs) must 
        be used as an own method. 

        [] <--- gehe --- Ich --- trinke ---> Tee

        """

        'subject -> simple pronoun'

        """'the following code gets for input a general personal pronoun, but somehow this does not work for all sentences.'
        'the correctness is independent from the continuing result of the next doc generation. That is the reason for ' \
        'this still being used'"""

        """ print(sentence_scheme.root_2_wrappers)

        prn_count = {
            'ichSin': (1, 1),
            'duSin': (2, 1),
            "erSin": (3, 1),
            "sieSin": (3, 1),
            "esSin": (3, 1),
            "wirPlu": (1, 2),
            "ihrPlu": (2, 2),
            "siePlu": (3, 2)
        }

        numerus = 0
        p0_list = []
        gender = ""

        for se in subject:
            se: Word = se
            if se.type == "NOUN" or se.type == "PRON":
                numerus += 1
                b0 = se.morph['Number'] == "Sin"
                if not b0:
                    numerus += 2
                else:
                    numerus += 1

                # get person
                if se.type == "PRON":

                    # wir bug fix
                    if se.tag == "PPER" and se.word != "sie":
                        if prn_count.keys().__contains__(se.word.lower()+"Sin"):
                            p0_list.append(prn_count[se.word.lower() + "Sin"][0])
                        else:
                            p0_list.append(prn_count[se.word.lower() + "Plu"][0])
                    else:
                        use = se.lemma
                        if se.lemma.lower() != se.word.lower():
                            use = se.word

                        p0_list.append(prn_count[use.lower() + se.morph['Number']][0])
                else:
                    if b0:
                        if se.morph['Gender'] == "Neu":
                            gender = "es"
                        elif se.morph['Gender'] == "Fem":
                            gender = "sie"
                        else:
                            gender = "er"

                    p0_list.append(3)
        p0_list = sorted(p0_list)
        dupes = list(set(p0_list[::2]) & set(p0_list[1::2]))
        if len(dupes) > 0:
            raise LogicException(ex_type=3)

        replacing_attr = ""

        print(subject)"""

        'if verb ends with en -> sie bzw. wir'
        'if not -> ihr'

        n = 0
        we = []

        for w3 in subject:
            if w3.type == "NOUN" or w3.type == "PRON" or w3.type == "PROPN" or (w3.type == "X" and w3.tag == "NE") or (
                    w3.tag == "PRELS" and w3.type == "DET"):
                n += 1

                if w3.type == "NOUN":
                    if w3.morph['Number'] == "Sin":
                        if w3.morph['Gender'] == "Neu":
                            we.append("es")
                        elif w3.morph['Gender'] == "Fe":
                            we.append("sie")
                        else:
                            we.append("er")
                    else:
                        we.append("sie")
                elif w3.type != "PRON":
                    we.append(w3.word.lower())
                else:
                    we.append(w3.word.lower())

        if n == 1:

            reference = we[0]
        else:
            if root.morph['Number'] == "Sin":
                reference = we[0]
            else:
                if root.word.endswith("en"):
                    reference = "sie"
                else:
                    reference = "ihr"

        problem_solver = ProblemSolver()
        c = problem_solver.check2(words=sentence_scheme.words, subject=subject)
        """if c != 0:
            new_sent = problem_solver.handle_problem(c)
            # print(new_sent + "!!!")
            sentence_scheme0 = SentenceScheme(new_sent)
            sentence_scheme0.origin_field = sentence_scheme.origin_field
            lingual_logic_parse(sentence_scheme0, subject)
            return
            experiment#1
            """
        if reference.lower() != subject[0].word.lower() and False:

            """ b1: bool = False
            wards = []
            for wx in sentence_scheme.words:
                if int(wx.id) >= int(subject[0].id) and int(wx.id) <= int(subject[-1].id):
                    if not b1:
                        wards.append(reference)

                    b1 = True
                else:
                    wards.append(wx.word)
            new_sentence = " ".join(wards)

            if new_sentence[0:1].islower():
                new_sentence = new_sentence[0:1].upper() + new_sentence[1:]

            sentence_scheme0 = SentenceScheme(new_sentence)
            sentence_scheme0.origin_field = sentence_scheme.origin_field
            # print("reload track completely")

            return lingual_logic_parse(sentence_scheme0, subject)
            
            experiment#1
            """
        else:
            # print("ready to continue...")

            # setting up time interval check

            # print("CURRENT TIME IN IS: " + str((int(time.time_ns().__str__()) - start_time) / pow(10, 9)) + " (in s)")

            """The next step is to build a field for every type in this sentence. The following type (glossary.pg) are possible:
            "ADJ": "adjective",
        "ADP": "adposition",
        "ADV": "adverb",
        "AUX": "auxiliary",
        "CONJ": "conjunction",
        "CCONJ": "coordinating conjunction",
        "DET": "determiner",
        "INTJ": "interjection",
        "NOUN": "noun",
        "NUM": "numeral",
        "PART": "particle",
        "PRON": "pronoun",
        "PROPN": "proper noun",
        "PUNCT": "punctuation",
        "SCONJ": "subordinating conjunction",
        "SYM": "symbol",
        "VERB": "verb",
        "X": "other",
            """

            """
            BLOCKS:

            ----- Object ------
            -> NOUN/PROPN + additional config, including o in dep

            ----- Subject -----
            already exists

            ----- Predicate -----
            -> AUX/VERB (bound with oc)

            ----- Modifiers ------
            -> ADV + additional config

            ----- Addition ------
            -> ADP + additional config

            ----- Extra -----
            ???

            """

            # Object

            blocks = []
            sentence_words = sentence.words.copy()
            pending_sentence_words = sentence_words.copy()

            # the object detection is similar to the subject detection

            object_base = []

            # print("---- Object ----")

            for w2 in sentence_words:
                if (
                        w2.dep == "oa" or w2.dep == "og" or w2.dep == "og" or w2.dep == "op" or w2.dep == "da" or w2.dep == "op" or (
                        w2.dep == "pd" and w2.morph.keys().__contains__(
                    "Case"))) and w2.type != "VERB" and w2.type != "AUX":
                    object_base.append(w2)
            # Note: The dep of obj is not always true, for example: a dative object is represented by ao (accusative)


            for ob in object_base:
                ob2 = [None] * len(sentence_scheme.words)
                ob2[int(ob.id)] = ob
                for w3 in pending_sentence_words:
                    if int(w3.head) == int(ob.id):
                        ob2[int(w3.id)] = w3

                        def analyse(wo: Word, last_type: str):
                            for w0 in pending_sentence_words:
                                if (int(w0.head) == int(wo.id) or int(w0.id) == int(wo.head)) and w0 != ob:
                                    if w0.dep == "cd" or w0.dep == "cj" or w0.dep == "nk" or w0.dep == "mo" \
                                            or w0.dep == "cc" or w0.dep == "cm" or w0.dep == "ROOT":
                                        if (w0.type != last_type or w0.type == "ADV" or w0.type == "ADJ") and (
                                                w0.type == "CCONJ" or w0.type == "PRON" or w0.type == "NOUN"
                                                or w0.type == "DET" or w0.type == "ADP" or w0.type == "NUM"
                                                or w0.type == "ADJ" or w0.type == "ADV"):

                                            if not ob2[int(w0.id)]:
                                                ob2[int(w0.id)] = w0
                                                analyse(w0)
                                        else:
                                            if w0.type == "VERB":
                                                # bug fix EX#002 sub[int(w0.head)] = None
                                                ob2[int(w0.id)] = None

                        analyse(w3, None)
                ob3 = []
                for ob20 in ob2:
                    if ob20:
                        ob3.append(ob20)
                ob2 = ob3
                del ob3
                # get object form
                name = None
                if ob.dep == "op":
                    name = "PrepositionalObject"
                else:
                    if not ob.morph.keys().__contains__("Case"):
                        if ob.dep == "oa":
                            name = "AccusativeObject"
                        elif ob.dep == "da":
                            name = "DativeObject"
                        elif ob.dep == "og":
                            name = "GenitiveObject"
                    else:
                        case = ob.morph['Case']
                        if case == "Ac":
                            name = "AccusativeObject"
                        elif case == "Da":
                            name = "DativeObject"
                        elif case == "Ge":
                            name = "GenitiveObject"
                        elif case == "No":
                            name = "NominativeObject"
                if name:
                    for ob22 in ob2:
                        sentence_words.remove(ob22)
                    block = Block(type_=0, name=name, word=ob2)
                    blocks.append(block)
            # print(blocks)
            # Subject Nominative Object
            for sl in subject:
                sentence_words.remove(sl)
            subject_block = Block(type_=1, name="MainSubject", word=subject)
            # print(subject_block)
            blocks.append(subject_block)
            pending_sentence_words = sentence_words.copy()
            # Predicate

            # print("---- Predicate ----")
            print(sentence_words)
            first = None
            predicate = []

            for wx in pending_sentence_words:

                p0 = [None] * len(sentence_scheme.words)
                predicates = []
                p_id = []
                filled = []

                def analyse(wo: Word, structure: list):
                    for w0 in pending_sentence_words:
                        if (int(w0.head) == int(wo.id) or int(w0.id) == int(wo.head)) and w0 != first:
                            if w0.dep == "cd" or w0.dep == "cj" or w0.dep == "oa" or w0.dep == "mo" or w0.dep == "oc" or w0.dep == "svp":
                                if (w0.type == "ADP" and w0.tag != "APPRART") or w0.type == "AUX" or w0.type == "VERB":
                                    if not p0[int(w0.id)]:
                                        # print("##"+str(w0))
                                        p0[int(w0.id)] = w0
                                        sentence_words.remove(w0)
                                        if w0.type == "AUX" or w0.type == "VERB":
                                            p_id.append(int(w0.id))
                                            if structure[-1].type == w0.type and w0.type != "AUX" and structure[
                                                -1].type != "AUX" and structure[-1].morph['VerbForm'] != "In" and \
                                                    w0.morph['VerbForm'] != "In":
                                                # print("CASE")
                                                structure[-1] = w0
                                            else:
                                                structure.append(w0)
                                            predicates.append(structure.copy())
                                        else:
                                            if w0.dep == "svp":
                                                doc = sentence_scheme.spacy(w0.word + structure[-1].word)
                                                t = doc.to_json()['tokens'][0]
                                                filled.append(structure[-1])
                                                structure[-1] = Word(t, w0.word + structure[-1].word)
                                                if sentence_words.__contains__(w0):
                                                    sentence_words.remove(w0)
                                                predicates.append(structure.copy())
                                        analyse(w0, structure)

                if first is None and (wx.type == "AUX" or wx.type == "VERB") and ((int(wx.head) > int(
                        sentence.words[-1].id) or int(wx.head) < int(sentence.words[0].id)) or sentence.name == "Main"):
                    first = wx
                    # print(wx)
                    p0[int(wx.id)] = wx
                    sentence_words.remove(wx)
                    predicates.append([wx])
                    analyse(wx, [wx])
                    standard_tree = []
                    for predicate1 in reversed(predicates):
                        standard_tree_x = predicate1[:-1]
                        if len(standard_tree) == 0:
                            standard_tree = standard_tree_x
                        if predicate1 != standard_tree or predicate1 == first:

                            if not filled.__contains__(predicate1[-1]):
                                predicate.append(predicate1)
                                filled.append(predicate1[0])  # ADD 15.11.21 - check required
                    break
                """    continue
                if first and int(wx.head) == int(first.id) and wx.dep == "oc" and (wx.type == "VERB" or wx.type == "AUX"):
                    predicate.append(wx)
                    analyse(wx, None)"""

            for p in predicate:
                blocks.append(Block(word=p, type_=2, name="BaseVerbs"))

            pending_sentence_words = sentence_words.copy()
            """Modifiers"""

            # print("--- Adverbs and Modifiers and Particles ---")

            # collecting adverbs
            already_in_block = []
            print(pending_sentence_words)
            print(blocks)
            for w in pending_sentence_words:
                if (
                        w.dep == "mo" or w.dep == "pd" or w.dep == "ng" or w.dep == "mnr") and \
                        not already_in_block.__contains__(w) and not w.type.__contains__("CONJ"):

                    # go under the rhythm

                    if w.type == "PART":
                        """particle found!!!"""
                        sentence_words.remove(w)
                        block = Block(type_=5, name="Particle", word=[w])
                        block.add_context(int(sentence.words[int(w.head) - int(sentence.words[0].id)].id))
                        blocks.append(block)
                        continue

                    running_area = [None] * len(sentence_scheme.words)

                    running_area[int(w.id)] = w
                    sentence_words.remove(w)
                    print("101")

                    def analyse0(wy, stack_size):
                        for ww in pending_sentence_words:
                            if int(ww.head) == int(wy.id):
                                stack_size += 1
                                if already_in_block.__contains__(ww):
                                    """compare stack size"""

                                    # get block

                                    bad_block = None

                                    for bs in reversed(blocks):
                                        if bs.data.__contains__(ww):
                                            bad_block = bs
                                            break

                                    v_stack_size = len(bad_block.data)
                                    if stack_size >= v_stack_size:
                                        """remove block form blocks"""
                                        blocks.remove(bad_block)
                                    else:
                                        raise Exception("Hello?")
                                running_area[int(ww.id)] = ww
                                if sentence_words.__contains__(ww):
                                    sentence_words.remove(ww)

                                analyse0(ww, stack_size + 1)
                                break

                    analyse0(w, 0)
                    print(w)
                    words4 = []
                    for wzz in running_area:
                        if wzz:
                            already_in_block.append(wzz)
                            words4.append(wzz)
                    if w.type == "ADV" and sentence.words[int(w.head) - int(sentence.words[0].id)].type == "VERB" or \
                            sentence.words[int(w.head) - int(sentence.words[0].id)].type == "AUX" \
                            or sentence.words[int(w.head) - int(sentence.words[0].id)].type == "ADV":
                        b = Block(type_=3, name="VerbModifier", word=words4)
                        b.add_context(int(sentence.words[int(w.head) - int(sentence.words[0].id)].id))
                        blocks.append(b)
                    else:
                        blocks.append(Block(type_=4, name="ObjectSubjectModifier", word=words4))
            # print(blocks)

            pending_sentence_words = sentence_words.copy()

            # print("--- Removing Garbage and Additional Stuff ---")

            for w in pending_sentence_words:
                if w.tag.startswith("$"):
                    sentence_words.remove(w)
                    # trash
                else:
                    if w.type.__contains__("CONJ"):
                        sentence_words.remove(w)
                        block = Block(type_=6, name=w.type, word=[w])
                        blocks.append(block)

            pending_sentence_words = sentence_words.copy()
            sentence.add_blocks(blocks)
            print(blocks)
            print("???")
            sentences_x.append(sentence)
    sentence_scheme.sentences = sentences_x
    print(sentence.blocks)
    return sentence_scheme


"""The sentence class is a part of a sentence"""


class Sentence:
    type0 = [
        "HS",
        "NS"
    ]

    def __init__(self, words, type_, name):
        self.words: list = words
        self.type = self.type0[type_]
        self.name = name
        self.blocks = []

    def __str__(self):
        return "..../Sentence: " + self.name + "/type=" + str(self.type) + "/&" + str(self.words) + ".......0"

    def __repr__(self):
        return self.__str__()

    def qq(self) -> str:
        s = ""
        for w in self.words:
            s += w.word + " "
        return s

    def add_blocks(self, blocks: list):
        self.blocks = blocks


"""The SyntaxBinding class is a class to enter the original words for a replacement"""


class Origin:
    def __init__(self):
        self.replace: list = []
        self.origin: list = []

    def __str__(self):
        return str(self.origin) + " -> " + str(self.replace)

    def __repr__(self):
        return self.__str__()


"""Attention: For the LogicTable Accessories we need to configure values as str lists, because of the fact, 
that it is possible to add multiple start nouns or method verbs (ex.) """


class Quant:
    """The Quant class is a 2 frame paralysed sync object"""

    def __init__(self, **sync_values):
        self.sync_values = sync_values
        self.iter = 0
        self.val = None
        self.lock = uuid.uuid4().int

    def __add_value(self, value):
        self.val = value

    def __lock(self, uid):
        self.lock = uid

    def to_quant_iter(self):
        if self.iter + 1 < len(self.sync_values):
            self.iter += 1
            q0 = Quant()
            q0.__add_value(self.sync_values.values()[self.iter])
            q0.__lock(self.lock)
            return q0

    def __same(self, q):
        return q.lock == self.lock

    def __str__(self):
        return self.val


class Method:
    """The method class includes the Process-Verb and the additional adverbs"""

    def __init__(self, method_quant_list, modifiers_quant_list):
        self.method: list = method_quant_list
        self.modifiers: list = modifiers_quant_list


class ProcessBar:
    """The object representing the MPB"""

    def __init__(self, w0, method_used, w1):
        self.start: list = w0
        self.method: Method = method_used
        self.end: list = w1

    def __str__(self):
        return str(self.start) + " ------" + str(self.method) + "-------> " + str(self.end)


class LogicTable:
    """This class is called LogicTable because of it's functionality as an overview and workspace. An LogicTable
    contains a main process board (MPB). See example below. The LogicQuestion construction also takes place in the
    LogicTable kit """
    """Example of MPB for 'Ich esse gerne Eis':
    
    (NS) Subject [ICH] -------e-s-s-e------> [EIS] Object (AO)
                      |                     |                   
                      --------[GERNE]--------
    
    """

    def __init__(self, process):
        print(process)
