import time
from multiprocessing.pool import ThreadPool
import random

import spacy as spacy
from germanetpy.germanet import Germanet
from germanetpy.path_based_relatedness_measures import PathBasedRelatedness
from germanetpy.synset import Synset, WordCategory

from word_relatedness.ngd import NGD
from word_relatedness.semantic_context import semantic_context


class WordRelation:

    # sim: PathBasedRelatedness will be removed because of the fast that the raster method is now used

    def __init__(self, w1: str, w2: str, s1: Synset, s2: Synset, spacy):
        if w1 and w2:
            self.w1 = w1
            self.w2 = w2
            self.s1 = s1
            self.s2 = s2
            self.results = []
            self.spacy = spacy
        else:
            raise Exception("Synset cannot be null!")

    def calculate_relation(self, useG) -> float:
        pool = ThreadPool(4)
        self.results = []
        self.results.append(pool.apply_async(func=self.semantic_distance_with_raster))  # 0
        if useG:
            self.results.append(pool.apply_async(func=self.calculate_ngd))  # 1
        else:
            self.results.append(pool.apply_async(func=self.single_return))
        self.results.append(pool.apply_async(func=self.calculate_semantic_context))  # 2
        self.results.append(pool.apply_async(func=self.vector_cosine_similarity))  # 3
        time.sleep(random.uniform(0, 0.5))
        self.results = [r.get() for r in self.results]
        filling = [0, 0, 0, 0]
        if self.results[3] > 1.0 and self.results[2] == 1:
            filling[3] = 68.75
            filling[2] = 5.8035714
            if useG:
                filling[1] = 4.9107143
            filling[0] = 20.5357143
        elif self.results[3] - self.results[1] > self.results[0] and self.results[2] != 1 and self.results[3] > \
                self.results[0] and useG:
            print("current topic")
            filling[3] = 18.75
            filling[2] = 5.8035714
            filling[1] = 50
            filling[0] = 20.5357143
        else:
            filling[0] = 41.0714286
            filling[1] = 9.8214286
            if useG:
                filling[2] = 11.6071429
            filling[3] = 37.5
        if self.results[2] == 3:
            filling[2] = 0
        # fill all equally until 100
        while sum(filling) < 100:
            filling[0] += 1
            filling[1] += 1
            if self.results[2] != 3 and useG:
                filling[2] += 1
            filling[3] += 1
        if useG:
            return (self.results[0] * filling[0] + self.results[1] * filling[1] + self.results[2] * filling[2] +
                    self.results[3] * filling[3]) / sum(filling)
        else:
            return (self.results[0] * filling[0] + self.results[1] * filling[1] +
                    self.results[3] * filling[3]) / sum(filling)

    def vector_cosine_similarity(self):
        return 1 - self.spacy(self.w1).similarity(self.spacy(self.w2))

    """def calculate_semantic_relatedness(self) -> float:
        return self.sim.simple_path(synset1=self.s1, synset2=self.s2)"""

    def semantic_distance_with_raster(self):
        path_len = self.s1.shortest_path_distance(self.s2)
        raster: list = [
            1.0,
            0.987708,
            0.974733,
            0.954862,
            0.925482,
            0.882317,
            0.824512,
            0.755922,
            0.680006,
            0.602665,
            0.531854,
            0.470320,
            0.414220,
            0.365897,
            0.324850,
            0.286456,
            0.249496,
            0.213358,
            0.177132,
            0.141854,
            0.110697,
            0.083603,
            0.060573,
            0.041605,
            0.026676,
            0.015687,
            0.008311,
            0.003894,
            0.001606,
            0.000596,
            0.000194,
            0.000049,
            0.000011,
            0.000003,
            0.000001,
            0.000000,
            0.000000,
            0.000000,
            0.000000
        ]
        return 1 - raster[path_len]

    def calculate_ngd(self) -> int:
        return 1 - NGD(self.w1, self.w2)

    def single_return(self) -> int:
        return 0

    def calculate_semantic_context(self) -> int:
        return 1 - semantic_context(self.w1, self.w2)


if __name__ == '__main__':
    before = (time.time_ns() + 500000) // 1000000
    space = spacy.load(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität Quellen/project/application/creativity_test/spacy_data/de_core_news_md/de_core_news_md-3.2.0")
    germanet = Germanet(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
        "Quellen/project/application/creativity_test/germanet_data/germanet/GN_V160/GN_V160_XML")
    h: Synset = germanet.get_synset_by_id("s33819")
    o: Synset = germanet.get_synset_by_id("s29209")
    rn = PathBasedRelatedness(germanet=germanet, category=WordCategory.nomen, max_len=35, max_depth=20,
                              synset_pair=(h, o))

    wr = WordRelation(h.lexunits[0].orthform, o.lexunits[0].orthform, h, o, space)

    print(wr.calculate_relation(useG=True))

    print("difference: " + str(((time.time_ns() + 500000) // 1000000 - before)))
