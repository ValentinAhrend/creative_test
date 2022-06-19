import json
import time
from multiprocessing.pool import ThreadPool

import requests
import spacy
from germanetpy.germanet import Germanet

def load_result(url, w, topic: bool):
    o = requests.get(url=url)
    s = o.content.decode("utf-8")
    if o.status_code >= 300:
        url = 'https://de.wiktionary.org/w/index.php?search=' + w + '&ns0=1'
        o1 = requests.get(url)
        s = o1.content.decode("utf-8")
        h0 = '<div class="mw-search-result-heading"><a href="/wiki/'
        if s.__contains__(h0):
            index = s.index(h0) + len(h0)
            index2 = s.index('"', index)
            result = s[index:index2]
            return load_result('https://de.wiktionary.org/wiki/' + result, result, topic)
        else:
            return ""
    topics = []
    if topic:
        se = '<a href="/wiki/'
        if s.__contains__('title="Hyperonyme"'):
            index0 = s.index('title="Hyperonyme"')
            last_index = 0
            s0 = s[index0: s.index("</dd></dl>", index0 + 1)]
            while True:
                try:
                    if s0.__contains__(se):
                        index1 = s0.index(se, last_index)
                        sx = s0[index1 + len(se): s0.index('"', index1 + len(se))]
                        last_index = index1 + 1
                        topics.append(sx)
                    else:
                        break
                except ValueError:
                    break

    if not s.__contains__(
            '<div id="mw-content-text" class="mw-body-content mw-content-ltr" lang="de" dir="ltr">'):
        s = s
    elif not s.__contains__('<span class="mw-headline" id="Übersetzungen">'):
        s = s[s.index('<div id="mw-content-text" class="mw-body-content mw-content-ltr" lang="de" dir="ltr">'):]
    else:
        s = s[s.index('<div id="mw-content-text" class="mw-body-content mw-content-ltr" lang="de" dir="ltr">'):
              s.index('<span class="mw-headline" id="Übersetzungen">')]
    if not w.__contains__("Aussprache"):
        s = s.replace("Aussprache", "")
    if not w.__contains__("Wortart"):
        s = s.replace("Wortart", "")
    if not w.__contains__("Genus"):
        s = s.replace("Genus", "")
    if not w.__contains__("Etymologie"):
        s = s.replace("Etymologie", "")
    if not w.__contains__("Abschnitt"):
        s = s.replace("Abschnitt", "")
    if not w.__contains__("Semantik"):
        s = s.replace("Semantik", "")
    if not w.__contains__("Phonetik"):
        s = s.replace("Phonetik", "")
    if not w.__contains__("Quell"):
        s = s.replace("Quell", "")
    if not w.__contains__("Wort"):
        s = s.replace("Wort", "")
    if not w.__contains__("Rede"):
        s = s.replace("Rede", "")
    if not w.__contains__("Reim"):
        s = s.replace("Reim", "")
    if not w.__contains__("Hyperon"):
        s = s.replace("Hyperon", "")
    if topic:
        return s, topics
    else:
        return s

threadp = ThreadPool(10)
results = []

def get_rtr(lst):

    sbx: dict = {}
    for ix in range(len(lst)):
        print(ix)
        res = load_result("https://en.wiktionary.org/wiki/Special:Random", "", False)
        for g in g_terms:
            if res.__contains__(g):
                if sbx.keys().__contains__(g):
                    sbx[g] += 1
                else:
                    sbx[g] = 1

    return sbx

if __name__ == '__main__':
    """
    ex1:
    before = (time.time_ns() + 500000) // 1000000
    germanet = Germanet(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
        "Quellen/project/application/creativity_test/germanet_data/germanet/GN_V160/GN_V160_XML")
    print("difference: " + str(((time.time_ns() + 500000) // 1000000 - before)))
    """
    space = spacy.load(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität Quellen/project/application/creativity_test/spacy_data/de_core_news_md/de_core_news_md-3.2.0")
    germanet = Germanet(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
        "Quellen/project/application/creativity_test/germanet_data/germanet/GN_V160/GN_V160_XML")

    lst = ["Haus", "Maus", "Schrank", "Tafel", "Wohnung", "Baum", "Wald", "Schule", "Zimmer", "Boden"]
    syn = []
    for l in lst:
        syn.append(germanet.get_synsets_by_orthform(l)[0])
    before = (time.time_ns() + 500000) // 1000000

    # optimize generic_terms_y_copy.json (less elements)
    g_terms = json.load(open("/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
                             "Quellen/project/application/word_relatedness_dart/word_relatedness_dart"
                             "/generic_terms_y_copy.json"
                             "", "r"))
    for i in range(len(g_terms)):
        results.append(threadp.apply_async(func=get_rtr, args=[g_terms[100 * i:100 * (i + 1)]]))

    results = [r.get() for r in results]

    sbx_fixed = {}
    for result in results:
        for key, item in result.items():
            if sbx_fixed.keys().__contains__(key):
                sbx_fixed[key] += item
            else:
                sbx_fixed[key] = item

    sorted_sbx = []
    max_list = []
    for key, item in sbx_fixed.items():
        max_list.append(item)
    max_list.sort(
        reverse=True)
    for i in max_list:
        key = [key0 for key0 in sbx_fixed if (sbx_fixed[key0] == i)][0]
        sorted_sbx.append(key)
        print(key)
        sbx_fixed.pop(key)

    print(json.dumps(sorted_sbx))

    open("/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
                             "Quellen/project/application/word_relatedness_dart/word_relatedness_dart"
                             "/generic_terms_y_new.json", "w").write(json.dumps(sorted_sbx))