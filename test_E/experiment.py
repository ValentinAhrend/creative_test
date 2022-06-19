import json

import spacy
from germanetpy.germanet import Germanet

from word_relatedness.word_relation import WordRelation

if __name__ == '__main__':
    space = spacy.load(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität Quellen/project/application/creativity_test/spacy_data/de_core_news_md/de_core_news_md-3.2.0")
    germanet = Germanet(
        "/Users/valentinahrend/OneDrive/! Valentin/Kreativität "
        "Quellen/project/application/creativity_test/germanet_data/germanet/GN_V160/GN_V160_XML")
    result = json.load(open("test_experiment_0.json"))
    print(result["test1"])
    z = []
    for k, v in result.items():
        if str(k).startswith("chain"):
            ls: list = v
            prev = None
            lo = []
            for lss in ls:
                if prev:
                    print(prev)
                    print(lss)
                    wr = WordRelation(lss, prev, germanet.get_synsets_by_orthform(lss)[0], germanet.get_synsets_by_orthform(prev)[0], space)
                    lo.append(wr.calculate_relation(useG=True))
                prev = lss
            print(lo)
            print(sum(lo) / len(lo))
            print(len(v))
            print(len(v) / (sum(lo) / len(lo)))
            z.append((len(v) - 16.7777777 / 2) / (sum(lo) / len(lo)))
            # 16, 17, 20, 15, 15, 14, 18, 17, 19
            print((16 + 17 + 20 + 15 + 15 + 14 + 18 + 17 + 19) / 9)
            print("__________-")
    print(z)
