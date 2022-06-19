class Path:

    def __init__(self, from_synset, to_synset, lcs, start_to_lcs_path, end_to_lcs_path):
        self._from_synset = from_synset
        self._to_synset = to_synset
        self._lcs = lcs
        self._start_to_lcs_path = start_to_lcs_path
        self._end_to_lcs_path = end_to_lcs_path
        self._pathlen = len(start_to_lcs_path) + len(end_to_lcs_path) - 1

    def __repr__(self):
        return f'Path (from start to LCS={self.start_to_lcs_path}, from end to LCS={self.end_to_lcs_path})'

    @property
    def from_synset(self):
        return self._from_synset

    @property
    def to_synset(self):
        return self._to_synset

    @property
    def lcs(self):
        return self._lcs

    @property
    def start_to_lcs_path(self):
        return self._start_to_lcs_path

    @property
    def end_to_lcs_path(self):
        return self._end_to_lcs_path

    @property
    def pathlen(self):
        return self._pathlen
