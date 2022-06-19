import json as js
from http.client import HTTPResponse
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import urllib.parse
import time
import requests
from pathlib import Path
from multiprocessing.pool import ThreadPool
from test_A.matrix import Matrix
from hyphen import Hyphenator
import test_A.ssession as ssession


class Synset:
    def __init__(self, json):
        self.relations = []
        if isinstance(json, str):
            json = js.loads(json)

        self.json = json
        self.id = json['id']
        self.headers = list(json['orthForms'])
        self.category = json['wordCategory']
        self.word_class = json['wordClass']
        self.paraphrase = json['paraphrase']
        self.definitions = list(json['wiktionaryParaphrases'])

    def add_relations(self, relation_list):
        self.relations = relation_list
        json_object_list = []
        for relation in relation_list:
            json_object_list.append(relation.to_json())
        self.json['relations'] = json_object_list
        print(self.json)

    def __str__(self):
        return js.dumps(self.json)


class Relation:
    def __init__(self, json_element):
        self.next_headers_split = []
        self.json = json_element
        self.base = json_element['fromSynsetId']
        self.next = json_element['toSynsetId']
        self.type = json_element['relType']
        self.next_headers = list(json_element['toOrthForms'])

    def to_json(self):
        return self.json

    def add(self, l):
        self.json['toOrthForms_split'] = l
        self.next_headers_split = l


def __get_synsets(word, id0, credentials) -> list:
    url = "https://weblicht.sfs.uni-tuebingen.de/rover/api/synsets?word=" + urllib.parse.quote(word, safe='')
    print(url)

    req = Request(url)

    req.add_header("Cookie", id0['name'] + "=" + id0['value'])
    req.add_header("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                                 "like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36")
    req.add_header("Host", "weblicht.sfs.uni-tuebingen.de")
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                             "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
    req.add_header("Connection", "keep-alive")
    # req.add_header("Accept-Encoding", "gzip, deflate, br")

    try:
        response: HTTPResponse = urlopen(req)
        json_text = response.read().decode()
        obj = js.loads(json_text)
        synset_list = []

        for element in obj['data']:
            synset_list.append(Synset(element))

        len(synset_list)

        return synset_list
    except Exception as e:
        print(e)
        if isinstance(e, HTTPError):
            e0: HTTPError = e
            print(e0.code)
            if e0.code == 401:
                id0 = ssession.generate_cookie_id(credentials=credentials, force=True)
                print(id0)
                time.sleep(1)
                return __get_synsets(word, id0, credentials)
        return []


"""
:return liste mit unterschiedlichen Bedeutungen 
 
 für Haus:
 - (1) Dynastie
 - (2) Sternzeichen
 - (3) Gebäude
 - (n) ...
 
 der komplette Sysnet muss mitgeliefert werden, wichtig ist die Erklärung,
 oder die Umschreibeung.
 
 Der Nutzer wird aufgerufen den Begriff mit einem anderen Begriff zu Verdeutlichen, Begriffe oben.
 
 Falls ihm kein Wort einfällt wird das Default-Synset übernommen.
 
"""

hyphenator : Hyphenator = None


def test_a_start(word_list, credentials) -> list:

    # check internet connection
    global hyphenator
    hyphenator = Hyphenator('de_DE')

    url_check = 'https://example.com'
    try:
        requests.get(url_check)
    except Exception as e:
        raise BaseException("No Internet Connection!")

    id0 = ssession.generate_cookie_id(credentials=credentials, force=False)
    sy1 = []
    for w in word_list:
        sy1.append(__get_synsets(w, id0, credentials))

    if len(sy1) != len(word_list):
        raise BaseException("cannot work with different lists")

    return sy1


def __get_relation_for_synset(synset: Synset, id0, credentials):
    if Path(__asset_path() + "synset_cache/synset" + synset.id).exists():
        return Synset(open(__asset_path() + "synset_cache/synset" + synset.id, "r").read())

    url = "https://weblicht.sfs.uni-tuebingen.de/rover/api/conrels?synsetId=" + synset.id

    req = Request(url)

    req.add_header("Cookie", id0['name'] + '=' + id0['value'])
    req.add_header("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                                 "like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36")
    req.add_header("Host", "weblicht.sfs.uni-tuebingen.de")
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                             "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
    req.add_header("Connection", "keep-alive")

    try:
        response: HTTPResponse = urlopen(req)
        json_text = response.read().decode()
        obj = dict(js.loads(json_text))
        relations = []
        for obj_ in obj['data']:
            relations.append(Relation(obj_))
        synset.add_relations(__load_each_relation_word(synset.headers, relations))
        add_to_cache(synset)
        return synset
    except HTTPError as e:
        if isinstance(e, HTTPError):
            e0: HTTPError = e
            print(e0.code)
            if e0.code == 401:
                id0 = ssession.generate_cookie_id(credentials=credentials, force=True)
                print(id0)
                time.sleep(2)
                return __get_relation_for_synset(synset, id0, credentials)
        return synset


global_relation_load = {}
pool = ThreadPool(10)
machine_boundary = []


def __load_each_relation_word(headers, relations: list) -> list:
    global global_relation_load

    relations0 = []
    for relation in relations:
        header_split = []
        nh_ = relation.next_headers
        for header in headers:
            nh_.append(header)
        for header in nh_:

            if global_relation_load.__contains__(header):
                header_split.append(global_relation_load[header])
            elif str(header)[0].isupper():

                print("load header:"+header)

                v = (__separate_word(header))

                header_split.append(v)
                global_relation_load[header] = v
                relation.add(v)
        relations0.append(relation)
    return relations0


def __separate_word(header) -> list:

    global hyphenator
    if hyphenator is not None:
        return hyphenator.pairs(header)
    else:
        return []


"""url = "https://www.dwds.de/wb/" + header

    try:

        response = requests.get(url)

    except requests.exceptions.ConnectionError as e0:
        print(e0)
        return []

    html = response.text

    if not html.__contains__('<span class="dwdswb-ft-blocklabel serif italic">Wortzerlegung'):
        return [header]

    index = html.index('<span class="dwdswb-ft-blocklabel serif italic">Wortzerlegung')

    #<span class="dwdswb-ft-blocklabel serif italic">Wortzerlegung </span><span class="dwdswb-ft-blocktext"> <i class=
    "bi bi-arrow-up-right dwds-aur"></i><a href="/wb/Fu%C3%9F">Fuß</a> <i class="bi bi-arrow-up-right dwds-aur"></i>
    <a href="/wb/Ball#1">Ball<sup>1</sup></a></span></div>

    html = html[index:html.index("</div>", index)]

    t = []

    while html.__contains__("</a>"):
        index = html.index("</a>")

            # <span class="dwdswb-ft-blocklabel serif italic">Wortzerlegung </span><span class="dwdswb-ft-blocktext"> 
            <i class="bi bi-arrow-up-right dwds-aur"></i> <i class="bi bi-arrow-up-right dwds-aur"></i><a href="/wb/Ball
            #1"
            >Ball<sup>1</sup></a></span></div>

        sub = html[0:index]

        if sub.endswith("sup>"):
            sub = sub[0:sub.rfind('<sup>')]

        sub = sub[sub.rfind(">") + 1:]

        t.append(sub)

        html = html[index + 4:]

    if len(t[0]) == 1:
        return header

    return t"""


def test_a_continue(option_list, credentials):
    id0 = ssession.generate_cookie_id(credentials=credentials, force=False)
    data = []

    global pool

    for s_id in option_list:
        data.append(pool.apply_async(__get_relation_for_synset, (s_id, id0, credentials)).get())
    matrix = Matrix(len(option_list))

    a0 = 0
    a1 = 0

    for i in range(0, len(option_list)):
        for j in range(0 + i, len(option_list)):
            v = __distance(j, i, data[i], data[j], id0, credentials)
            matrix.add(v, j, i)
            a0 += v
            a1 += 1

    ssession.close_web_driver()

    matrix.print()
    print(">>"+((a0 - len(option_list)) / (a1-len(option_list))).__str__())


def __works(s,h) -> bool:

    w = "".join(s)
    if not w.__contains__(h):
        return False

    index0 = w.index(h)
    v0 = 0
    for ss in s:
        if v0 == index0:
            v0 = -2
            break
        elif v0 > index0:
            break
        v0 += len(ss)

    if v0 != -2:
        return False

    v1 = 0
    index1 = index0 + len(h)
    for ss in s:
        if v1 == index1:
            return True
        elif v1 > index1 or v1 == len(w):
            return False
        v1 += len(ss)


def __distance(j, i, s0: Synset, s1: Synset, id0, credentials) -> float:
    if s0.id == s1.id:
        return 1.0

    print("compare relations of "+s0.headers[0]+" and "+s1.headers[0])
    for s in s0.relations:
        print(s.next_headers_split)
    print("---------")
    for o in s1.relations:
        print(o.next_headers_split)

    # relation between relation header and top header
    for relation in s0.relations:
        for s1_header in s1.headers:
            for n_header in relation.next_headers:
                if n_header == s1_header:
                    print("r0 found")
                    return 1 - 0.02857
            for o_header in relation.next_headers_split:
                if __works(o_header, s1_header):
                    return 1 - 0.02857 * 1.5

    # relation between relation header and top header
    for relation in s1.relations:
        for s0_header in s0.headers:
            for n_header in relation.next_headers:
                if n_header == s0_header:
                    print("r1 found")
                    return 1 - 0.02857
            for o_header in relation.next_headers_split:
                if __works(o_header, s0_header):
                    return 1 - 0.02857 * 1.5

    # semantic distance

    # check cache before

    p = Path(__asset_path() + "synset_cache/from" + s0.id+ "to" + s1.id)
    p1 = Path(__asset_path() + "synset_cache/from" + s1.id+ "to" + s0.id)
    if p.exists():
        v = float(p.read_text())
        print(v)
        return v
    elif p1.exists():
        v = float(p1.read_text())
        print(v)
        return v

    url = "https://weblicht.sfs.uni-tuebingen.de/rover/api/semrels?measures=SimplePath&synset1Id=" + s0.id + \
          "&synset2Id=" + s1.id + "&normMax=1"

    print(url)

    req = Request(url)

    req.add_header("Cookie", id0['name'] + "=" + id0['value'])
    req.add_header("User-Agent", "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                                 "like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36")
    req.add_header("Host", "weblicht.sfs.uni-tuebingen.de")
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                             "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
    req.add_header("Connection", "keep-alive")

    try:
        response: HTTPResponse = urlopen(req)
        json_text = response.read().decode()
        obj = dict(js.loads(json_text))

        print("success for value " + j.__str__() + "/" + i.__str__())

        add_data_to_cache(s0.id,s1.id,str(obj['data'][0]['score']))

        v = obj['data'][0]['score']
        print(v)
        return v

    except HTTPError as e:
        print(e)
        if isinstance(e, HTTPError):
            e0: HTTPError = e
            print(e0.code)
            if e0.code == 401 or e0.code == 500:
                id0 = ssession.generate_cookie_id(credentials=credentials, force=True)
                print(id0)
                if e0.code == 500:
                    time.sleep(2)
                else:
                    time.sleep(2)
                return __distance(j, i, s0, s1, id0, credentials)
        return -1


def __assets(name, mode):
    top = __file__
    top = top[0:top.rfind("/")]
    return open(top + "/assets/" + name, mode)


def __asset_path() -> str:
    top = __file__
    top = top[0:top.rfind("/")]
    return top + "/assets/"


def add_to_cache(synset: Synset):
    p = Path(__asset_path() + "synset_cache/synset" + synset.id)
    if not p.exists():
        p0 = Path(__asset_path() + "synset_cache")
        if not p0.exists():
            p0.mkdir()
        file = open(__asset_path() + "synset_cache/synset" + str(synset.id), "w+")
        file.write("")
        js.dump(synset.json, fp=file)
        print(file)


def add_data_to_cache(id0, id1,val):
    p = Path(__asset_path() + "synset_cache/from" + id0 + "to" + id1)
    if not p.exists():
        p0 = Path(__asset_path() + "synset_cache")
        if not p0.exists():
            p0.mkdir()
        file = open(__asset_path() + "synset_cache/from" + id0 + "to" + id1, "w+")
        file.write(val)
