class VectorizerTFIDF:
    """
    A container object that store vectorizer with TFIDF objects which can be used for
    text document feature extraction by the scikit-learn library.
    Vectorizers are fitted TfidfVectorizer objects from sklearn.feature_extraction.text module.
    Attribute:
        version: version of the VectorizerTFIDF object.
        title_vectorizer: TFIDF vectorizer for job title.
        desc_vectorizer: TFIDF vectorizer for job description.
        title_para: parameters of job title vectorizer - {"max_df":max_df, "min_df":min_df}.
        desc_para: parameters of job description vectorizer - {"max_df":max_df, "min_df":min_df}.
        filename: Path of the file into which VectorizerTFIDF is saved.
    """

    def __init__(self, title_vectorizer, desc_vectorizer, date):
        """
        Init VectorizerTFIDF class object.
        :param title_vectorizer: TfidfVectorizer from sklearn.feature_extraction.text module,
                                    fitted by job title data.
        :param desc_vectorizer: TfidfVectorizer from sklearn.feature_extraction.text module,
                                    fitted by job description data.
        :param filename: Path of the file into which VectorizerTFIDF is saved.
        """
        self.version = '0.001'
        self.date_created = date
        self.title_vectorizer = title_vectorizer
        self.title_para = {'max_df': title_vectorizer.max_df,
                           'min_df': title_vectorizer.min_df}
        self.desc_vectorizer = desc_vectorizer
        self.desc_para = {'max_df': desc_vectorizer.max_df,
                          'min_df': desc_vectorizer.min_df}

    @staticmethod
    def load(filename):
        """Load VectorizerTFIDF object from saved pickle file."""
        import pickle
        with open(filename, 'rb') as file_in:
            loaded_vect = pickle.load(file_in)
        return loaded_vect


def fit_tfidf_vectorizer(tokenized_docs, doc_field, max_df=None, min_df=None):
    """
    Fit scikit-learn TfidfVectorizer object.
    :param tokenized_docs: Text documents of which each word-tokens are separated by '|'.
    :param doc_field: Data field of document to be vectorized.
    :param max_df: Maximum count of features that will be embedded into the vectorizer.
                    Providing (int)/(float) will specify maximum count in term of
                    (absolute number)/(fraction of total available features).
                    default: max_df=1.0 (use all features).
    :param min_df: Minimum count of features that will be embedded into the vectorizer.
                    Providing (int)/(float) will specify minimum count in term of
                    (absolute number)/(fraction of total available features).
                    default: min_df=1 (at least 1 feature).
    :return: Fitted scikit-learn TfidfVectorizer object.
    """

    def simple_split(doc_segmented):
        """Return a list of word-tokens by splitting doc_segmented whereby word-tokens are separated by '|'."""
        return doc_segmented.split('|')

    from sklearn.feature_extraction.text import TfidfVectorizer

    # select document field to be tokenized.
    tokenized_docs = [doc[doc_field] for doc in tokenized_docs]

    # instantiate TfidfVectorizer object.
    tfidf_vectorize = TfidfVectorizer(tokenizer=simple_split, max_df=max_df, min_df=min_df)
    tfidf_vectorize.fit(tokenized_docs)  # fit vectorizer.
    return tfidf_vectorize


def create_vectorizer(documents: dict, tokenize_func=None,
                      title_max_df=0.95, title_min_df=0.005,
                      desc_max_df=0.95, desc_min_df=0.005,
                      dump=False):
    """
    Create a fitted VectorizerTFIDF object to be used for document feature extraction
    required for text classification by scikit-learn library.


    :param documents: A list of documents in json format.
    :param tokenize_func: Tokenizer function. If provided, the function will tokenize documents.
                        Leave 'tokenize_func' if the documents are already tokenized.
    :param title_max_df: Maximum count of features that will be embedded into the vectorizer
                        intended for job title data.
                        Providing (int)/(float) will specify maximum count in term of
                        (absolute number)/(fraction of total available features).
                        default: max_df=1.0 (use all features).
    :param title_min_df: Minimum count of features that will be embedded into the vectorizer
                        intended for job title data.
                        Providing (int)/(float) will specify minimum count in term of
                        (absolute number)/(fraction of total available features).
    :param desc_max_df: Maximum count of features that will be embedded into the vectorizer
                        intended for job description data.
                        Providing (int)/(float) will specify maximum count in term of
                        (absolute number)/(fraction of total available features).
    :param desc_min_df: Minimum count of features that will be embedded into the vectorizer
                        intended for job description data.
                        Providing (int)/(float) will specify minimum count in term of
                        (absolute number)/(fraction of total available features).
    :param dump: True will store VectorizerTFIDF object into a file.
    :return: Fitted VectorizerTFIDF object.
    """

    from copy import deepcopy
    from datetime import date
    import dill

    documents = deepcopy(documents)
    today = date.today()

    # create filename
    filename = './Resource/Classifier/' + 'TFIDF_' + str(today) + '_' + \
               str(int(len(documents) / 1000)) + '.vec'

    # if tokenizer function is provided - implying that the documents are not tokenized
    # or that one wants to re-tokenize the documents.
    if tokenize_func:
        documents = tokenize_func(documents)
    # create vectorizer for job title data.
    title_vectorizer = fit_tfidf_vectorizer(documents, 'title', title_max_df, title_min_df)
    # create vectorizer for job description data.
    desc_vectorizer = fit_tfidf_vectorizer(documents, 'desc', desc_max_df, desc_min_df)
    # create VectorizerTFIDF object.
    document_vectorizer = VectorizerTFIDF(title_vectorizer, desc_vectorizer, today)

    if dump:  # if user wants to save the fitted vectorizer.
        dill.dump(document_vectorizer, open(filename, 'wb'))

    return document_vectorizer
