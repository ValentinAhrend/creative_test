import lingual_index
import spacy

if __name__ == '__main__':
    spacyy = spacy.load(str(__file__)[
                        0:str(__file__).rindex(
                            "logical_algo")] + "spacy_data/de_core_news_md/de_core_news_md-3.2.0")
    print(lingual_index.run("Im Wald ist eine Schule mit vielen Waldn.", spacyy))
