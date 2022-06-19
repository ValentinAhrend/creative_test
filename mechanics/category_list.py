from multiprocessing.pool import ThreadPool
from time import sleep
import requests
import json

result = []
pool = ThreadPool(100)


def run_cat_list():
    global result
    """
    #1 load https://alex-riedel.de/randV2.php?anz=10
        it is a open php site that returns 100 german words...
    #2 load the wikipedia page of each word
    #3 get the wikipedia categories add to list
    :return: file with list (generic_terms)
    """

    ''' src_file = open("/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
                    "Quellen/project/application/test/word_relatedness/generic_terms_x.json", "r")
    data = src_file.read()
    big_list: list = json.loads(data)'''
    big_list = []
    # src_file.close()

    target_file = open("/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
                       "Quellen/project/application/test/word_relatedness/generic_terms_x.json", "w")

    for i in range(0, 100):
        print(i)
        result.append(pool.apply_async(func=run_word_generation, args=()))
        sleep(1 / (i+1))

    result = [r.get() for r in result]

    for rx in result:
        print(rx)
        big_list.extend(rx)
    big_list = remove_duplicates(big_list)
    print(big_list)

    target_file.write(json.dumps(big_list))
    target_file.close()

def remove_duplicates(item_list):
    singles_list = []
    for element in item_list:
        if element not in singles_list:
            singles_list.append(element)
    return singles_list


def run_word_generation() -> list:
    print("load")
    session = requests.sessions.session()
    url = "https://alex-riedel.de/randV2.php?anz=200"
    json_str = session.get(url).content.decode(encoding="utf-8")
    tag_list: list = json.loads(json_str)
    url0 = "https://de.wikipedia.org/wiki/"

    complete_list = []

    for tag in tag_list:
        data = session.get(url0 + tag).content.decode(encoding="utf-8")
        if data.__contains__('"Kategorie:'):
            index = data.index('"Kategorie:')
            cat0 = data[index:data.index('"', index + 3)]
            cat0 = cat0.replace("Wikipedia", "")

            if cat0.__contains__("("):
                continue
            cat0 = cat0[cat0.index(":") + 1:]
            complete_list.append(cat0)
    complete_list = remove_duplicates(complete_list)
    return complete_list


if __name__ == '__main__':
    run_cat_list()
