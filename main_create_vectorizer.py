""""
    Create an object of fitted tfidf vectorizer and dump into a pickle file.
    :argument
    documents:          A file containing documents, each of which is stored in json format
                        with the following keys: (1) "title", (2) "desc", (3) "tag"
    output:             File name for the output.
    pool=<int>:         Number of pool processes.
    ntitle=<int>:       Length of n-gram for title tokenizer - default = 5.
    ndesc=<int>:        Length of n-gram for description tokenizer - default = 3.
    chunksize=<int>:    Number of jobs assigned to a given queue in each process.
"""

if __name__ == '__main__':

    import sys
    from src.tokenizer import tokenize_documents
    from src.vectorizer import create_vectorizer
    import warnings
    import json
    warnings.filterwarnings('ignore')

    # ========== parsing arguments ==========
    argvs = sys.argv[1:]
    doc_filename = argvs.pop(0)
    out_filename = argvs.pop(0)
    kwargs = {'pool': 16, 'ntitle': 5, 'ndesc': 3, 'chunksize': 100}

    for arg in argvs:
        for key in list(kwargs):
            if arg.find(key) != -1:
                kwargs[key] = int(arg.split('=')[1])
    # ========================================

    # Read documents from json file.
    print('Loading data from ' + doc_filename)
    with open(doc_filename, 'rt', encoding='utf-8') as f_in:
        documents = json.load(f_in)

    # Tokenize documents
    print(kwargs)
    documents = tokenize_documents(documents, pool_process=kwargs['pool'],
                                   chunksize=kwargs['chunksize'])
    print('Completed tokenizing documents ' + doc_filename)

    json.dump(documents,
              open(out_filename, 'wt', encoding='utf-8'),
              ensure_ascii=False)

    # create vectorizers
    vectorizers = create_vectorizer(documents, dump=True)
    print('Completed fitting vectorizers from documents ' + doc_filename)
