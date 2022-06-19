
"""
THE String Control Interface SCI
--------------------------------

by Valentin Ahrend

Operating a string with pre-set methods

-> giving the input string to the constructor

method-tree: {

    words (separator)
    phrase (separator)
    compare (comparator)

}

"""


class SCI:

    """self.values:
        ops (operating_string, str, final)

    """

    def __init__(self, operating_string):
        self.ops = operating_string

    def words(self):
        words = self.ops.split()
        words_ = []
        for word in words:
            word_ = ""
            if word.__contains__('\uf8ff'):
                inc = word.index('\uf8ff')
                w_sep, w_sep_ = word[0:inc], ""
                for c in w_sep:
                    if c.isalpha() and not c.isnumeric():
                        w_sep_ += c
                word = word[inc:].replace('\uf8ff', '', -1)
                if len(w_sep_) > 0:
                    words_.append(w_sep_)
            for c in word:
                if c.isalpha() and not c.isnumeric():
                    word_ += c
            if len(word_) > 0:
                words_.append(word_)
        return words

    def phrase(self):
        return str(self.ops).splitlines(keepends=False)

    def each(self, array, function) -> list:

        results = []

        for element in array:
            results.append(function(element))

        return results

    def compare(self, elements):
        finished = []
        selection = []
        for element in elements:
            ct = True
            for finish in finished:
                if finish == element:
                    ct = False
                    j = -1
                    for i in range(len(selection)):
                        if selection[i][0] == finish:
                            j = i
                            break
                    if j != -1:
                        selection[j] = tuple(selection[j]).__add__((finish,))
                    else:
                        selection.append((finish, finish))
                    break
            if ct:
                finished.append(element)
        return selection




class SCOM(SCI):

    """the sci commands"""

    def __init__(self, operating_string):
        super().__init__(operating_string)

    def run_commands(self) -> int:
        pass


"""
class SCOM_A(SCOM):
    
    def run_commands(self) -> bool:
        actions... 
"""

class SCOM_Alliteration(SCOM):
     def run_commands(self) -> int:
         """
         check if there is an alliteration in text
         :returns size of found alliterations (words in alliteration * amount of alliteration)
         info: an alliteration is found in one phrase only (not multiple)
         """
         # self.each(self.phrase(), lambda : self.each(self.words(), lambda: self.compare())
