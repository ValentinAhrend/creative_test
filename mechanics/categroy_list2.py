from multiprocessing.pool import ThreadPool

import requests
import json
from urllib.parse import quote

result = []
pool = ThreadPool(100)


def run_list():
    global result, pool
    file0 = open("/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
                 "Quellen/project/application/test/word_relatedness/generic_terms_y.json", "r")
    data = file0.read()
    l = json.loads(data)
    file0.close()
    result = []

    # 1 step: get random wiktionary page
    # 2 step: search header on wikipedia
    # 3 step: get category of article
    # 4 step: get category of category of category

    for _ in range(0, 100):
        result.append(pool.apply_async(func=a_b, args=()))

    result = [r.get() for r in result]

    for r in result:
        l.extend(r)
    lx = []
    for ll in l:
        if not lx.__contains__(ll):
            lx.append(ll)

    file0 = open("/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
                 "Quellen/project/application/test/word_relatedness/generic_terms_y.json", "w")
    file0.write(json.dumps(lx))
    file0.close()

    print("task completed")


def a_b() -> list:
    cats_complete = []
    random_wiktionary_link = "https://de.m.wiktionary.org/wiki/Spezial:Zuf%C3%A4llig_in_Kategorie/Substantiv_(Deutsch)"

    session = requests.session()
    for _ in range(0, 10):
        response_url = session.get(random_wiktionary_link).url

        response_header = response_url[response_url.rindex("/") + 1:]

        broke = False

        for ii in range(0, 3):

            wikipedia_page_link = "https://de.wikipedia.org/wiki/" + response_header.replace(" ", "_")

            data = session.get(wikipedia_page_link).content.decode(encoding="utf-8")

            cats = []
            while data.__contains__('"Kategorie:'):
                index0 = data.index('"Kategorie:')
                cat0: str = data[index0 + 1: data.index('"', index0 + 1)]
                cats.append(cat0)
                data = data[index0 + 1:]
            if len(cats) == 0:
                broke = True
                break
            dd = []

            for c in cats:
                if not c.__contains__("Wikipedia") and not c.__contains__("Begriffsklärung") and not c.__contains__(
                        "("):
                    dd.append(c)
            if len(dd) > 0:

                response_header = lensort(dd)[0][1]

                if ii == 1:
                    response_header_x = response_header
                    if response_header_x.startswith("Kategorie:"):
                        response_header_x = response_header[response_header.index(":") + 1:]
                    cats_complete.append(response_header_x)
        if not broke:
            if response_header.startswith("Kategorie:"):
                response_header = response_header[response_header.index(":") + 1:]
            cats_complete.append(response_header)

    return cats_complete


def lensort(x):
    list1 = []
    for i in x:
        list1.append([len(i), i])
    return sorted(list1)


if __name__ == '__main__':
    for i in range(0, 1000):
        run_list()
        print(i)