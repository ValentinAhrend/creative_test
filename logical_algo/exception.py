
class LogicException(Exception):
    """This Exception is called as a result of the algorithm. If there is an unlogical element, but no access to a
    great return bridge, the exception with the error data will be thrown. """

    def __init__(self, ex_type=0, json_data_str=None):
        message = "Unlogical Exception"
        if ex_type == 0:
            message = "An unlogical element was detected: "
        elif ex_type == 1:
            message = "No ROOT Verb was found in the sentence: "
        elif ex_type == -2:
            message = "This is a dummy exception. There are no logical exceptions."
        elif ex_type == 2:
            message = "No Subject was found in the sentence: "
        elif ex_type == 3:
            message = "The Subject contains to identical personal identifiers. (Ex: *Ich* und *Ich* sind toll.)"
        elif ex_type == 4:
            message = "There exist too many sub sentences (max. = 1)."
        message += str(json_data_str)
        super().__init__(message)
