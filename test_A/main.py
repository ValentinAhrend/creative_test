from json import JSONEncoder

from germanetpy.germanet import Germanet
from germanetpy.path_based_relatedness_measures import PathBasedRelatedness
from germanetpy.synset import Synset, WordCategory
import time
import test_a_optimized


def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default


def run_test_opt():
    list_of_words = ["Schrank", "Zeit", "Raum", "Religion", "Start", "Schule", "Radio"]

    germanet = Germanet(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
        "Quellen/project/application/creativity_test/germanet_data/germanet/GN_V160/GN_V160_XML")
    h: Synset = germanet.get_synset_by_id("s49774")
    o: Synset = germanet.get_synset_by_id("s83979")
    rn = PathBasedRelatedness(germanet=germanet, category=WordCategory.nomen, max_len=35, max_depth=20,
                              synset_pair=(h, o))

    time0 = time.time()

    synset_list, list_of_words = test_a_optimized.start_test_a(list_of_words, germanet=germanet)
    s0 = []
    for ryn in synset_list:
        s0.append(ryn[0])
    matrix, score = test_a_optimized.finish_test_a(s0, list_of_words)
    print((time.time()-time0))
    matrix.print()
    print(score)


if __name__ == '__main__':
    run_test_opt()
