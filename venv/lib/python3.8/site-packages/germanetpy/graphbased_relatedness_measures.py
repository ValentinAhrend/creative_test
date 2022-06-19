import numpy as np
from germanetpy import longest_shortest_path


class Graphbased_relatedness:
    def __init__(self, germanet, category):
        self._germanet = germanet
        self._max_len = longest_shortest_path.get_overall_longest_shortest_distance(germanet, category)
        self._max_depth = longest_shortest_path.get_greatest_depth(germanet, category)

    def path(self, synset1, synset2):
        assert synset1.word_category == synset2.word_category, "only synsets of the same Wordcategory can be " \
                                                               "compared"
        pathlen = synset1.shortest_path_distance(synset2)
        path = (self.max_len - pathlen) / self.max_len
        return np.round(path, decimals=3)

    def wup(self, synset1, synset2):
        assert synset1.word_category == synset2.word_category, "only synsets of the same Wordcategory can be " \
                                                               "compared"
        root_node = self.germanet.root()
        lcs_nodes = synset1.lowest_common_subsumer(synset2)
        depth = 0
        for n in lcs_nodes:
            dist = n.shortest_path_distance(root_node)
            if dist > depth:
                depth = dist
        pathlen = synset2.shortest_path_distance(synset1)
        wup = (2 * depth) / (pathlen + 2 * depth)
        return np.round(wup, decimals=3)

    def lch(self, synset1, synset2):
        assert synset1.word_category == synset2.word_category, "only synsets of the same Wordcategory can be " \
                                                               "compared"
        pathlen = synset1.shortest_path_distance(synset2)
        lch_sim = -np.log(pathlen / (2 * self.max_depth))
        return np.round(lch_sim, decimals=3)

    def normalize(self, raw_value,normalized_max):
        return (raw_value / max_value) * normalized_max


    @property
    def germanet(self):
        return self._germanet

    @property
    def max_len(self):
        return self._max_len

    @property
    def max_depth(self):
        return self._max_depth
