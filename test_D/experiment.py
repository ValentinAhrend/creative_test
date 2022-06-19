from multiprocessing.pool import ThreadPool

import spacy
from gensim.models import Doc2Vec
from germanetpy.germanet import Germanet

from test_D.test_d import start_test_d_1


def run_x( sent):
    print("?")
    return start_test_d_1([sent], germanet, 3, space, model=model)


pool = ThreadPool(50)

if __name__ == '__main__':
    """
    200 sentences, check if randomly correct
    """

    space = spacy.load(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität Quellen/project/application/creativity_test/spacy_data/de_core_news_md/de_core_news_md-3.2.0")
    germanet = Germanet(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
        "Quellen/project/application/creativity_test/germanet_data/germanet/GN_V160/GN_V160_XML")

    sentences_a = open("sentences10k.txt").read()
    model = Doc2Vec.load(str(__file__)[
                         0:str(__file__).rindex("test_D")] + "test_D/d2v-" + str(3) + ".model")
    n = 2000
    max_iter = 170
    sentences_list = []
    for i in range(max_iter):
        sentence = sentences_a[sentences_a.index(str(i + n)+"	") + len((str(i + n) + "	")):sentences_a.index(str(i + n + 1) + "	")]
        sentences_list.append(sentence)
    pool = ThreadPool(50)
    results = []
    for sent in sentences_list:
        print(sent)
        results.append(pool.apply_async(func=run_x, args=[sent]))
    results = [r.get() for r in results]
    print(results)

"""
output:

experiment-output.json

169/170
161/170
160/170


"""