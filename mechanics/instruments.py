# -*- coding:utf-8 -*-

import json
import os.path
import time
from enum import Enum

import requests
import spacy
from germanetpy.germanet import Germanet
from germanetpy.path_based_relatedness_measures import PathBasedRelatedness
from germanetpy.synset import Synset
from germanetpy.synset import WordCategory

import app
import test_F
from test_A import test_a_optimized
from test_B import test_b
from test_C.test_c import test_c0
from test_D.test_d import start_test_d_1
from test_E.test_e import form_test_e
from test_F.test_f import Scheme, run_test_f


class Value:

    def __init__(self, name):
        self.name = name
        self.session_start = time.time()
        self.value = 0.0

    def __str__(self):
        return "(" + self.name + str(self.session_start) + ") - Value Object, presenting " + str(self.value)

    def send_exception(self, exception_title, exception_message):
        print("exit, caused by " + exception_title)
        print("-- " + exception_message)


class NRV:

    def __init__(self):
        self.types_map = {}
        self.FINISHED.value = 0
        self.stop = False
        """f = open('/Users/valentinahrend/Documents/data_f1.txt', 'w')
        f.write("0,0")
        f.close()

        f = open('/Users/valentinahrend/Documents/data_f2.txt', 'w')
        f.write("0,0")
        f.close()

        f = open('/Users/valentinahrend/Documents/data_f3.txt', 'w')
        f.write("0,0")
        f.close()"""

    #     f = open('//Users/valentinahrend/Documents/types_cc.json', "w")
    #        f.write("{}")

    def start(self):

        if open('/stop.txt').read() == 'stop':
            self.stop = True

        if self.stop:
            print("-----")

            print(self.FINISHED.value)

            return

        url = 'https://gedichte.ws/zufall'
        # url = 'https://www.gedichte.ws/kindergedichte/626'
        content = requests.get(url)
        print(content.url)
        print("47273492387429742938")

        self.FINISHED.value += 1
        index0 = content.text.index("<p>")
        index1 = content.text.index("</p>", index0)
        piut = content.text[index0 + 3:index1]

        errr = piut.split("<br />")

        e2 = []
        for e in errr:
            if e.__contains__('&quot;'):
                e = e.replace('&quot;', '')
            if e.__contains__("\n"):
                e = e.replace("\r\n", "")
            e2.append(e)

        piut = "".join(e2)

        while piut.endswith(""):
            piut = piut[:-1]

        if piut.__contains__("©"):
            piut = piut[0:piut.index("©")]
        gedicht = piut.strip()

        lines = gedicht.split(sep="")
        paragraphs = [""]
        for line in lines:
            if line != "" and line != "":
                paragraphs[len(paragraphs) - 1] += line + ""

        # wir haben nun das paragraphen array geschaffen

        # Fehlerüberprüfung

        # jede Strophe wird analysiert...

        schemes_total = []
        z_length = 0
        for paragraph in paragraphs:
            if paragraph.endswith(""):
                paragraph = paragraph[:-1]
            result = test_F.test_f.reimschema_typus(paragraph)
            print("-->" + str(result['schema']))
            schemes_total.append(Scheme(result['schema']))
            z_length += result['z_anzahl']
        words_used_in_rhymes = []
        rhyme_groups = []
        rhyme_types = {}

        f1, f2, f4, f3 = test_F.test_f.valid0(schemes_total, z_length)
        f1_ = open('/Users/valentinahrend/Documents/data_f1.txt', "r")
        xf1 = f1_.read()
        if xf1 is not None:
            n = float(xf1[0:xf1.index(",")])
            z = float(xf1[xf1.index(",") + 1:])
            n = (n * z + f1) / (z + 1)
            z += 1
            xf1 = str(n) + "," + str(z)
            f1_w = open('/Users/valentinahrend/Documents/data_f1.txt', "w")
            f1_w.write(xf1)
            f1_w.close()

        f2_ = open('/Users/valentinahrend/Documents/data_f2.txt', "r")
        xf2 = f2_.read()
        if xf2 is not None:
            n = float(xf2[0:xf2.index(",")])
            z = float(xf2[xf2.index(",") + 1:])
            n = (n * z + f2) / (z + 1)
            z += 1
            xf2 = str(n) + "," + str(z)
            f2_w = open('/Users/valentinahrend/Documents/data_f2.txt', "w")
            f2_w.write(xf2)
            f2_w.close()

        f3_ = open('/Users/valentinahrend/Documents/data_f3.txt', "r")
        xf3 = f3_.read()
        if xf3 is not None:
            n = float(xf3[0:xf3.index(",")])
            z = float(xf3[xf3.index(",") + 1:])
            n = (n * z + f3) / (z + 1)
            z += 1
            xf3 = str(n) + "," + str(z)
            f3_w = open('/Users/valentinahrend/Documents/data_f3.txt', "w")
            f3_w.write(xf3)
            f3_w.close()

        self.start()


'''
        for schema in schemes_total:
            for rhyme in schema.single:

                if not rhyme_groups.__contains__(rhyme.rhyme_group):
                    if isinstance(rhyme.rhyme_group, tuple):
                        for g in rhyme.rhyme_group:
                            if not rhyme_groups.__contains__(g):
                                rhyme_groups.__contains__(g)
                    else:
                        rhyme_groups.append(rhyme.rhyme_group)

                if not rhyme_types.__contains__(rhyme.type):
                    rhyme_types[rhyme.type] = 1
                else:
                    rhyme_types[rhyme.type] = rhyme_types[rhyme.type] + 1

                _FINISHED.value = 0
                for word in rhyme.words:
                    def __r_w_(word0) -> int:
                        if not words_used_in_rhymes.__contains__(word0):
                            words_used_in_rhymes.append(word0)
                            return 1
                        return 0

                    if isinstance(word, tuple):
                        for ww in word:
                            _FINISHED.value += __r_w_(ww)
                    else:
                        _FINISHED.value += __r_w_(word)
                if rhyme.element_count - _FINISHED.value > 1:
                    words_used_in_rhymes = words_used_in_rhymes[0:len(words_used_in_rhymes) - _FINISHED.value]
                    rhyme_groups = rhyme_groups[0:-1]
                    rhyme_types[rhyme.type] = rhyme_types[rhyme.type] - 1

        f = open('/Users/valentinahrend/Documents/types_cc.json', "r")

        print(rhyme_types.__str__())
        ele = f.read()
        print(ele)
        types_map0 = json.loads(ele)
        for key0 in rhyme_types.keys():
            if types_map0.keys().__contains__(key0):
                types_map0[key0] += rhyme_types[key0]
            else:
                types_map0[key0] = rhyme_types[key0]

        f = open('/Users/valentinahrend/Documents/types_cc.json', "w")

        f.write(json.dumps(types_map0))
        f.close()

        print(types_map0)
'''


class TestInformationData:
    def __init__(self, test_id, test_name, test_description):
        self.test_id = test_id
        self.test_name = test_name
        self.test_description = test_description

    def json_obj(self):
        return [self.test_id, self.test_name, self.test_description]


class TestInformation(Enum):
    TEST_A = TestInformationData(test_id=496575095, test_name="Kreuzverhör", test_description="Beim Kreuzverhör "
                                                                                              "müssen 10 "
                                                                                              "möglichst verschiedene "
                                                                                              "Wörter "
                                                                                              "eingegeben werden. "
                                                                                              "Die Wörter sollten "
                                                                                              "Nomen, "
                                                                                              "aber keine Namen oder "
                                                                                              "umgangssprachlichen "
                                                                                              "Ausdrücke sein. "
                                                                                              "Das zeitliche Limit "
                                                                                              "beträgt 2 Minuten.")
    INIT = TestInformationData(test_id=-6126037, test_name="Laden von Modulen", test_description="Vor dem Test muss "
                                                                                                 "der Test kurz "
                                                                                                 "geladen werden. "
                                                                                                 "Dies dauert wenige "
                                                                                                 "Sekunden.")
    TEST_B = TestInformationData(test_id=967950466, test_name="Buchstabenkette", test_description="Für drei der in der "
                                                                                                  "1. Aufgabe "
                                                                                                  "eingegeben "
                                                                                                  "Wörter müssen nun "
                                                                                                  "möglichst ähnliche "
                                                                                                  "Wörter gefunden "
                                                                                                  "werden. "
                                                                                                  "Du kannst die Reihe "
                                                                                                  "unbegrenzt "
                                                                                                  "fortführen, "
                                                                                                  "allerdings gibt es "
                                                                                                  "ein zeitliches "
                                                                                                  "Limit "
                                                                                                  "von 5 Minuten.")
    TEST_C = TestInformationData(test_id=392452174, test_name="Satz-Kombination", test_description="Die Aufgabe "
                                                                                                   "'Satz-Kombination' "
                                                                                                   "besteht darin, aus "
                                                                                                   "mindestens 3 der "
                                                                                                   "Wörter "
                                                                                                   "aus Aufgabe 1 "
                                                                                                   "einen Satz "
                                                                                                   "zu bilden. "
                                                                                                   "Innerhalb "
                                                                                                   "von 3 Minuten "
                                                                                                   "sollte "
                                                                                                   "ein logischer, "
                                                                                                   "sinnvoller "
                                                                                                   "Satz entstehen. "
                                                                                                   "Der "
                                                                                                   "Satz sollte "
                                                                                                   "gleichzeitig "
                                                                                                   "ein Hauptsatz "
                                                                                                   "sein.")
    TEST_D = TestInformationData(test_id=527072652, test_name="Problemzauber", test_description="Hier müssen 3 "
                                                                                                "Probleme "
                                                                                                "gelöst werden. Die "
                                                                                                "Lösungsmethode und "
                                                                                                "das "
                                                                                                "Problem wird in jeder "
                                                                                                "Teilaufgabe "
                                                                                                "erläutert.")
    TEST_E = TestInformationData(test_id=151887809, test_name="Schlangenlinie", test_description="Nenne das erste "
                                                                                                 "Wort, "
                                                                                                 "das dir zu einem "
                                                                                                 "bestimmten Begriff "
                                                                                                 "einfällt.Anschlie"
                                                                                                 "ßend nennt "
                                                                                                 "man das erste Wort, "
                                                                                                 "was "
                                                                                                 "einem zu dem "
                                                                                                 "eingebenen Wort "
                                                                                                 "einfällt und so "
                                                                                                 "weiter... "
                                                                                                 "Eine solche Liste "
                                                                                                 "an Begriffen "
                                                                                                 "sollen 3 mal "
                                                                                                 "erstellt werden. "
                                                                                                 "Es gibt kein "
                                                                                                 "zeitliches Limit, "
                                                                                                 "die Zeit spielt "
                                                                                                 "aber eine "
                                                                                                 "wichtige Rolle.")
    TEST_F = TestInformationData(test_id=202637939, test_name="Reimspiel", test_description="Im Reimspiel muss ein "
                                                                                            "Gedicht verfasst werden. "
                                                                                            "Die Wörter in dem Gedicht "
                                                                                            "sollen sich reimen. "
                                                                                            "Versuche "
                                                                                            "einen guten Ausdruck zu "
                                                                                            "verwenden.")


class TestStatus(Enum):
    OPENED = 0,
    STARTED = 1,
    FINISHED = 2,
    TASK_1 = 3,
    TASK_2 = 4,
    TASK_3 = 5,
    ERR = 6

    """
    add alternative values, which show the process in the specific validation
    """


class TestError(Enum):
    WRONG_METHOD_ID = "Diese Methode exisitiert nicht."
    NO_USAGE = "Die angegebenen Wörter konnten nicht in dem Satz gefunden werden."


class TestOutput(Enum):
    FINISHED = "Erfolgreich abgeschlossen."


def test_data_from_str(json_str):
    lst = json.loads(json_str)
    return TestData(lst[0], lst[1], lst[2], lst[3])


class TestData:
    """
    the TestData represents the current status of the current running test
    the connection between the flutter python framework and the python files receives messages created by the print-
    method. This means that the str() method must contain each value in a certain format
    """

    LOG = "test-data"

    def __init__(self, test_information, status, error, output):
        self.test_information: TestInformationData = test_information
        self.status: int = status
        self.error: list = error
        self.output: list = output
        if isinstance(self.test_information, list):
            self.test_information = TestInformationData(test_id=self.test_information[0],
                                                        test_name=self.test_information[1],
                                                        test_description=self.test_information[2])

    def send_data(self):
        print(json.dumps({self.LOG: self.data()}))

    def get_data(self):
        return json.dumps(self.data())

    def data(self):
        return [self.test_information.json_obj(), self.status, self.error, self.output]


def test_from_str():
    # impl needed!!!!!!!!!!!!!!!!!!
    return Test()


def test_exists() -> bool:
    return os.path.isfile("current-test-info.json")


class Test:
    """
    the Test manager class that is called by the app framework
    controlling all input and output calls and manage stability and data transportation
    """

    def __init__(self):
        self.test_data: list = []
        self.start_time = time.time_ns()

    def save(self):
        obj = []
        for test_info in self.test_data:
            test_info: TestData = test_info
            obj.append(test_info.data())
        if os.path.isfile("current-test-info.json"):
            json.dump({'start_time': self.start_time,
                       'test_data': obj}, open("current-test-info.json", "w"))
        else:
            json.dump({'start_time': self.start_time,
                       'test_data': obj}, open("current-test-info.json", "x"))

    def put(self, test_id, method, input_data) -> str:
        """
        the put method handles all methods for each test and organizes the process
        it is the adaption to each test frame
        :param test_id: the test id [0-5]
        :param method: the method you want to execute (depends on the test)
        :param input_data: the data the test requires
        :return: a str in json format representation of the TestData

        test_id book:

        -1 -> init the models
        [0...5] for tests
        6 get all results (including time)

        """

        data = None
        try:
            if test_id == -1:
                # germanet
                germanet_file = str(__file__)[
                                0:str(__file__).rindex("mechanics")] + "germanet_data/germanet/GN_V160/GN_V160_XML"
                app.germanet = Germanet(germanet_file)
                """h: Synset = test.germanet.get_synset_by_id("s49774")
                o: Synset = test.germanet.get_synset_by_id("s83979")"""
                """test.relatedness = PathBasedRelatedness(germanet=test.germanet, category=WordCategory.nomen, max_len=35,
                                                        max_depth=20,
                                                        synset_pair=(h, o))"""
                # spacy
                app.spacy = spacy.load(str(__file__)[
                                       0:str(__file__).rindex(
                                           "mechanics")] + "spacy_data/de_core_news_md/de_core_news_md-3.2.0")

                data = TestData(test_information=TestInformation.INIT.value, status=TestStatus.FINISHED.value, error=[],
                                output=TestOutput.FINISHED.value)
            elif test_id == 0:
                print("hello")
                if method == -1:
                    """check single word"""
                    data = TestData(test_information=TestInformation.TEST_A.value, status=TestStatus.STARTED.value,
                                    error=[],
                                    output=[len(app.germanet.get_synsets_by_orthform(input_data[0])) > 0])
                elif method == 0:
                    """
                    sending complete synsets back and receive synset ids then

                    list_of_words == input_data

                    :return synset_list, list_of_words

                    :receiving list_of_words
                    """
                    synset_list, list_of_words = test_a_optimized.start_test_a(input_data, germanet=app.germanet)
                    sl = []
                    for synset in synset_list:
                        sx = []
                        for sy in synset:
                            sq = []
                            for lex in sy.lexunits:
                                sq.append(lex.orthform)
                            sz = []
                            for hy in sy.direct_hyponyms:
                                szz = []
                                for lex in hy.lexunits:
                                    szz.append(lex.orthform)
                                sz.append(szz)
                            sx.append((sy.id, sq, sz))
                        sl.append(sx)
                    data = TestData(test_information=TestInformation.TEST_A.value, status=TestStatus.STARTED.value,
                                    error=[],
                                    output=tuple((sl, list_of_words)))
                elif method == 1:

                    """
                    :receiving synset_list, list_of_words
                    input_data = list
                    """
                    synset_list = []
                    for synset_id in input_data[0]:
                        print(synset_id)
                        synset_list.append(app.germanet.get_synset_by_id(synset_id[0]))

                    matrix, score = test_a_optimized.finish_test_a(synset_list, input_data[1], spacy=app.spacy)
                    data = TestData(test_information=TestInformation.TEST_A.value, status=TestStatus.FINISHED.value,
                                    error=[],
                                    output=(matrix, score))
                else:

                    data = TestData(test_information=TestInformation.TEST_A.value, status=TestStatus.FINISHED.value,
                                    error=[TestError.WRONG_METHOD_ID.value], output=[])
            elif test_id == 1:

                if method == 0:
                    """
                    receive: list_of_words from test_a
                    return: 3 random words form the list
                    """
                    test_words = test_b.define_test_words(input_data)[0:3]
                    data = TestData(test_information=TestInformation.TEST_B.value, status=TestStatus.STARTED.value,
                                    error=[], output=test_words)
                elif method == 1:
                    """
                    receive: dictionary (map)...
                    {
                    k: v - list(words)
                    }
                    return tuple of average and output_dict
                    """
                    output = test_b.start_test_b(input_data, app.germanet, app.spacy)
                    data = TestData(test_information=TestInformation.TEST_B.value, status=TestStatus.FINISHED.value,
                                    error=[], output=output)
                else:
                    data = TestData(test_information=TestInformation.TEST_B.value, status=TestStatus.FINISHED.value,
                                    error=[TestError.WRONG_METHOD_ID.value], output=[])
            elif test_id == 2:
                if method != 0:
                    data = TestData(test_information=TestInformation.TEST_C.value, status=TestStatus.FINISHED.value,
                                    error=[TestError.WRONG_METHOD_ID.value], output=[])
                else:
                    """
                    receive: winners[1], input_sentence[0]
                    return: tuple score and sentence scores
                    """
                    output = test_c0(input_data[0], input_data[1], app.spacy)

                    if output[0] == -1:
                        data = TestData(test_information=TestInformation.TEST_C.value, status=TestStatus.FINISHED.value,
                                        error=[TestError.NO_USAGE.value], output=[])
                    elif output[0] == -2:
                        data = TestData(test_information=TestInformation.TEST_C.value, status=TestStatus.FINISHED.value,
                                        error=str(output[1]), output=[])
                    else:
                        data = TestData(test_information=TestInformation.TEST_C.value, status=TestStatus.FINISHED.value,
                                        error=[], output=output)
            elif test_id == 3:
                if 0 <= method < 4:
                    """
                    receive: list of sentences
                    """
                    output = start_test_d_1(input_data, app.germanet, method, app.spacy)
                    data = TestData(test_information=TestInformation.TEST_D.value, status=3 + method,
                                    error=[], output=output)
                else:
                    data = TestData(test_information=TestInformation.TEST_D.value, status=TestStatus.FINISHED.value,
                                    error=[TestError.WRONG_METHOD_ID.value], output=[])
            elif test_id == 4:
                if method == 0:
                    """
                    receive: list of lists out of word and time to enter
                    """
                    data = TestData(test_information=TestInformation.TEST_E.value, status=TestStatus.FINISHED.value,
                                    error=[], output=form_test_e(input_data, (app.germanet, app.spacy)))
                else:
                    data = TestData(test_information=TestInformation.TEST_E.value, status=TestStatus.FINISHED.value,
                                    error=[TestError.WRONG_METHOD_ID.value], output=[])
            elif test_id == 5:
                if method == 0:
                    """
                    receive: poetry
                    return: score and example rhyme scheme
                    """
                    data = TestData(test_information=TestInformation.TEST_F.value, status=TestStatus.FINISHED.value,
                                    error=[], output=run_test_f(input_data))
                else:
                    data = TestData(test_information=TestInformation.TEST_F.value, status=TestStatus.FINISHED.value,
                                    error=[TestError.WRONG_METHOD_ID.value], output=[])
            elif test_id == 6:
                if method == 0:
                    """
                    send data from each task
                    add total score
                    """
                    print(self.test_data)
            self.test_data.append(data)
        except Exception as e:
            return TestData(test_information=TestInformation.INIT.value, status=TestStatus.ERR.value,
                            error=[e.args], output=[]).get_data()
        return data.get_data()
