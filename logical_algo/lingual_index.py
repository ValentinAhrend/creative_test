from logical_algo.lingual_analysis import SentenceScheme, lingual_logic_parse
from logical_algo.logical_analysis import generate_logical_binding
import json
from logical_algo.exception import LogicException


class LogicResult:
    """The LogicResult is the output of the logic ai. It contains a final 'logic' score and mutliple properties,
    like the SentenceScheme """

    def __init__(self):
        self.sentence_scheme = SentenceScheme(None, None)
        self.score = -1
        self.logic_exception: LogicException = LogicException(ex_type=-2, json_data_str="")

    def add_sentence_scheme(self, sentence_scheme):
        self.sentence_scheme = sentence_scheme

    def add_score(self, score):
        self.score = score

    def add_err(self, logic_exception: LogicException):
        self.logic_exception: LogicException = logic_exception

    def __str__(self):
        return json.dumps({
            'logic_score': str(self.score),
            'sentence_scheme': self.sentence_scheme.__str__(),
            "exception": self.logic_exception.__str__()
        })


def run(input_sentence, space) -> LogicResult:
    """This method executes the logic ai text algorithm. It returns the LogicResult class."""
    logic_result = LogicResult()
    try:
        scheme = SentenceScheme(input_sentence, space=space)
        logic_result.add_sentence_scheme(scheme)

        scheme_updated = lingual_logic_parse(scheme, None)

        out = generate_logical_binding(scheme_updated, space=space)
        if out:
            logic_result.score = 1
        else:
            logic_result.score = 0

        return logic_result

    except LogicException as logic_ex:
        logic_result.add_err(logic_ex)
        return logic_result
