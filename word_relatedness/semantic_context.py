import json
import math
from multiprocessing.pool import ThreadPool
import time

import requests

results = []
pool = ThreadPool(2)


def semantic_context(w1, w2, include_topics: bool = False, zap: int = 0):
    global results
    global pool
    session = requests.session()
    results = []
    pool = ThreadPool(2)
    request_link_a = "https://de.wiktionary.org/wiki/" + w1
    request_link_b = "https://de.wiktionary.org/wiki/" + w2
    results.append(pool.apply_async(func=load_result, args=(request_link_a, w1, session, include_topics)))
    results.append(pool.apply_async(func=load_result, args=(request_link_b, w2, session, include_topics)))

    results = [r.get() for r in results]

    # new against bug: semantic dead
    if results.__len__ == 0 and zap == 0:
        time.sleep(0.1)
        return semantic_context(w1, w2, zap=1)
    elif results.__len__ == 0:
        return -2

    if include_topics:
        topics = [r[1] for r in results]
        results = [r[0] for r in results]

        topic_results_a = []
        topic_results_b = []

        for topic in topics:
            for t in topic:
                rl = "https://de.wiktionary.org/wiki/" + t
                if topics.index(topic) == 0:
                    topic_results_a.append(pool.apply_async(func=load_result, args=(rl, t, session, False)))
                else:
                    topic_results_b.append(pool.apply_async(func=load_result, args=(rl, t, session, False)))
        topic_results_a = [r.get() for r in topic_results_a]
        topic_results_b = [r.get() for r in topic_results_b]

    generic_terms = json.load(open("/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
                                   "Quellen/project/application/test/word_relatedness/generic_terms_y.json"))

    w1_headers = []
    w2_headers = []

    generic_terms.append(w1)
    generic_terms.append(w2)

    for gt in generic_terms:

        if results[0].__contains__(gt):
            w1_headers.append(gt)
        if results[1].__contains__(gt):
            w2_headers.append(gt)

    appears_in_both = []
    for w1 in w1_headers:
        if w2_headers.__contains__(w1):
            appears_in_both.append(w1)

    if include_topics:
        wx_header_headers = []
        wy_header_headers = []
        xc = 0
        for gt in generic_terms:
            wx_header_headers.append([])
            wy_header_headers.append([])
            for tr in topic_results_a:
                if tr.__contains__(gt):
                    wx_header_headers[xc].append(gt)
            for tz in topic_results_b:
                if tz.__contains__(gt):
                    wy_header_headers[xc].append(gt)
            xc += 1
        while wx_header_headers.__contains__([]):
            wx_header_headers.remove([])
        while wy_header_headers.__contains__([]):
            wy_header_headers.remove([])

        total_comp_x = 1
        x_max = 2
        for header_list in wx_header_headers:
            x_max += len(header_list)
            for header in header_list:
                if w2_headers.__contains__(header):
                    total_comp_x += 1
        total_comp_y = 1
        y_max = 2
        for header_list in wy_header_headers:
            y_max += len(header_list)
            for header in header_list:
                if w1_headers.__contains__(header):
                    total_comp_y += 1
        var0_x = math.log(2 * total_comp_x, 2) / math.log(x_max, 2)
        var0_y = math.log(2 * total_comp_y, 2) / math.log(y_max, 2)
        var_e = (var0_y + var0_x) / 2

    # print(w1_headers, w2_headers, appears_in_both)

    if len(appears_in_both) > 0 and len(w2_headers) > 0 and len(w1_headers) > 0:

        w1_ = len(w1_headers) + 1
        w2_ = len(w2_headers) + 1
        w0_ = len(appears_in_both) + 1

        """

        Calculate the highest point:

        w1_ = 2500 + 1# len(w1_headers) + 1
        w2_ = 2500 + 1# len(w2_headers) + 1
        w0_ = 1 + 1 # len(appears_in_both) + 1

        >20.739335268643753

        """

        print(appears_in_both)
        print(w1_headers)
        print(w2_headers)

        w0_short = w1_
        w0_long = w2_
        if w0_short > w0_long:
            w0_short = w2_
            w0_long = w1_
        # factor 1 depends from the relative possibility to have same headers
        var0 = math.log(w0_ * 2, 2) / math.log(w1_ + w2_, 2)
        # factor 2 depends from the length of the appears_in_both and the shortest cat abb
        # var1 = math.log(w0_short, 2) / math.log(w0_, 2)
        # factor 3 depends from the length of the appears_in_both and the longest cat abb
        # var2 = math.log(w0_long, 2) / math.log(w0_, 2)
        # factor 4 is a multiplication of all factors
        # var3 = var1 * var0 * var2

        # max(var1, var2) - var0 /

        var3 = var0
        # print(var3)
        return var3
    else:
        return 0


def load_result(url, w, session, topic: bool):
    o = session.get(url=url)
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
            return load_result('https://de.wiktionary.org/wiki/' + result, result, session, topic)
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

    if not s.__contains__('<div id="mw-content-text" class="mw-body-content mw-content-ltr" lang="de" dir="ltr">'):
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


if __name__ == '__main__':
    print(semantic_context("Himmel", "Wolkenkratzer"))

