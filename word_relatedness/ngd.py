import math
import time
from multiprocessing.pool import ThreadPool

import numpy as np
import requests
from bs4 import BeautifulSoup

""" 
NGD = Normalized Google Distance 

article: https://aclanthology.org/C12-2049.pdf

defines the similarity between words via comparing the search results on google for the word A, B and the combination 
of A and B
"""


def NGD(w1, w2):
    if w1 != w2:
        results = total_numbers(w1, w2)
        global result
        result = []
        n = 25270000001.0
        # 25.270.000.000 maximum amount of google results
        n = math.log(n, 2)
        # logarithm with base 2

        if results[0] == n or results[1] == n:
            n = n + 100

        f_w1 = math.log(int(results[0]) + 1, 2)
        f_w2 = math.log(int(results[1]) + 1, 2)
        f_w1_w2 = math.log(int(results[2]) + 1, 2)
        random_method([n, f_w1, f_w2, f_w1_w2])
        out = ((max(f_w1, f_w2) - f_w1_w2) / (n - min(f_w1, f_w2)))
        return out
    else:
        return 0


def random_method(value):
    print(value)


def get_ngd(w1, w2, tries=10):
    # tries are important because it is a very important value.

    for i in range(tries):
        try:
            return NGD(w1, w2)
        except Exception as e:
            print(str(tries) + str(e))
    return np.NaN


result = []
pool = ThreadPool(4)


def total_numbers(w1, w2) -> list:
    global pool, result
    result.append(pool.apply_async(func=num_results, args=(w1, 0)))
    time.sleep(0.1)
    result.append(pool.apply_async(func=num_results, args=(w2, 0)))
    time.sleep(0.1)
    result.append(pool.apply_async(func=num_results, args=(w1 + "+" + w2, 0)))

    result = [r.get() for r in result]
    return result


def kill_complete_session():
    pool.close()
    pool.join()


def num_results(text, tr):
    try:
        """Returns the number of Google results for a given query."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '
                          'Safari/537.36'}
        # sleep(5, 10)
        no_optionals = "&sxsrf=AOaemvKg0HaQuzLMmzeFfjF6evLPOsYpZg:1639153973774&source=lnt&tbs=li:1&sa=X&ved" \
                       "=2ahUKEwjA9dmy1Nn0AhXGgP0HHSoYAiAQpwV6BAgBEDE&biw=2560&bih=1329&dpr=2 "
        r = requests.get("https://www.google.com/search?hl=de&q={}".format(text) + no_optionals, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")  # Get text response
        res = soup.find('div', {'id': 'result-stats'})  # Find result string
        if res.text.replace(".", "").split()[0].isnumeric():
            return int(res.text.replace(".", "").split()[0])
        return int(res.text.replace(".", "").split()[1])  # Return result int
    except AttributeError as e:
        if tr == 0:
            time.sleep(0.3)
            return num_results(text, tr + 1)
        return 1000000  # returning one million as default


if __name__ == '__main__':
    print(NGD("Freundschaft", "Taschenrechner"))
    # [838000000, 82100000, 3910000, 35300, 135000]
