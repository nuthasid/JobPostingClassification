
class FuzzyMatch:
    """FuzzyMatch object contain a word list in which each word is associated with
    a keyword with minimum Levenshtein distance."""

    def __init__(self, leven_func=None, cosine_cut=0.25):
        """
        Init object.
        :param leven_func: Levenshtein distance function. If 'none' the object will
        use Levenshtein implementation from python-Levenshtein.
        :param cosine_cut: Cosine similarity cut-off considered too dissimilar.
        """
        if not leven_func:
            self.leven_dis = leven_func
        else:
            from Levenshtein import distance
            self.leven_dis = distance
        self.cosine_cut = cosine_cut
        self.lexicon = {}
        self.keywords = set()

    def set_keyword(self, keywords):
        """
        Set object keyword.
        :param keywords: (list) keywords.
        :return:
        """
        self.keywords = set(keywords)
        self.keywords.add('')

    def _add_word(self, word):
        """
        Add a word to the lexicon and calculate cloest match.
        :param word: (str) word.
        :return: None
        """
        if word in self.lexicon:
            return
        self.lexicon[word] = {'keyword': '_',
                              'cosine': 1.0,
                              'leven': 10**3}
        for keyword in sorted(list(self.keywords)):
            cosine = self.cosine_dis(word, keyword)
            if cosine > self.cosine_cut:
                leven = len(word) + len(keyword)
            else:
                leven = self.leven_dis(word, keyword)
            distance = {'keyword': keyword,
                        'leven': leven,
                        'cosine': cosine}
            if self.lexicon[word]['leven'] < distance['leven']:
                self.lexicon[word] = distance
            elif self.lexicon[word]['leven'] == distance['leven'] and \
                    self.lexicon[word]['cosine'] < distance['cosine']:
                self.lexicon[word] = distance
            else:
                pass
        return

    def add_word_list(self, word_list):
        """
        Add a list of words to the lexicon and calculate their closest
        keyword match.
        :param word_list: (list) a list of words.
        :return: None
        """
        for word in word_list:
            self._add_word(word)

    def _add_keyword(self, keyword):
        """
        Add a word to the keyword list and recalculate closest match
        for all words in the lexicon.
        :param keyword: (str) keyword.
        :return: None
        """

        self.keywords.add(keyword)

        for word in self.lexicon.keys():
            cosine = self.cosine_dis(word, keyword)
            if cosine > self.cosine_cut:
                leven = len(word) + len(keyword)
            else:
                leven = self.leven_dis(word, keyword)
            distance = {'keyword': keyword,
                        'leven': leven,
                        'cosine': cosine}
            self.lexicon[word][keyword] = distance
            if self.lexicon[word]['leven'] > distance['leven']:
                self.lexicon[word] = distance
            elif self.lexicon[word]['leven'] == distance['leven'] and \
                    self.lexicon[word]['cosine'] > distance['cosine']:
                self.lexicon[word] = distance
            else:
                pass

    def add_keyword_list(self, keyword_list):
        """
        Add a list of words to the keyword list and recalculate their closest
        match for each word in the lexicon.
        :param keyword_list: (list) a list of keywords.
        :return: None
        """
        for keyword in keyword_list:
            self._add_keyword(keyword)

    def fuzzy_match(self, word, leven_weight=0.1):
        """
        Find the keyword with closest match for a given word.
        :param word: (str) word
        :param leven_weight: (float, default=0.1) Edit intensity (number of edit divided
        by the length of the word) above which the word is considered to be too dissimilar
        to the keyword.
        :return: (dict) {keyword, leven_dis, cosine_dis} or None
        """
        if word not in self.lexicon:
            self._add_word(word)
        edits = self.lexicon[word]['leven'] / len(word)
        if edits < leven_weight:
            return self.lexicon[word]
        else:
            return None

    @staticmethod
    def cosine_dis(word1, word2):
        """
        Calculate cosine similarity between two words.
        :param word1: (str) First word.
        :param word2: (str) Second word.
        :return: (float) cosine similarity.
        """
        from scipy.sparse import csc_matrix
        from scipy.spatial.distance import cosine
        from sklearn.feature_extraction.text import CountVectorizer

        vectorizer = CountVectorizer(analyzer='char')
        word_vec = vectorizer.fit_transform([word1, word2])
        word_vec = csc_matrix.todense(word_vec)
        word_dis = cosine(word_vec[0], word_vec[1])

        return word_dis
