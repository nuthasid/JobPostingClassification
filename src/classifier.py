class Classifier:

    def __init__(self, vectorizer):
        """
        Init Classifier


        :param vectorizer: A vectorizier object wth 'transform' method.
        """

        from copy import deepcopy
        from datetime import date

        self.version = '0.001'
        self.date = date.today()
        self.classifiers = []
        self.classes_ = []
        self.vectorizer = vectorizer
        self.copy = deepcopy

    def predict_documents(self, documents, thres=0.5):
        """
        Predict the label of the document(s).

        :param documents: Documents in json format with keys: 'title_seg' and 'desc_seg'.
        :param thres: probability threshold over which the document will be assigned a class.
        :return: JSON documents - each of which contain addition key 'predicted'
                    of which value is a dict with {'class': float<prob>} pair.
        """

        documents = self.copy(documents)
        if not type(documents) in (list, tuple):
            documents = [documents]

        for document in documents:
            document.update(self.predict_document(document, thres))

        return documents

    def predict_document(self, document, thres=0.5):
        """
        Predict the class of the document using a set of classifier (class attribute).


        :param document: The document in dict format to be classified.
        :param thres: probability threshold over which the document will be assigned a class.
        :return: (predicted class, <dict>{class, probability}).
        """

        document = self.copy(document)

        # extract features into numpy array.
        data_vec = self._extract_features(document)

        doc_class = {'None': thres}  # set default class to 'None'
        # for each classifier, classify the document.
        for clf in self.classifiers:
            # store prediction result in doc_class.
            # only store positive class from the result from .predict_proba method.
            # since the name of positive class must begins with [A-Za-z], the location of class
            # in .predict_proba method return will be at location 1.
            doc_class[clf.classess_[1]] = clf.predict_proba(data_vec)[0, 1]

        # Find the class with max predicted probability - including the default class
        # whose probability equals thres.
        predicted = 'None'
        for key in list(doc_class):
            if doc_class[key] > doc_class[predicted]:
                predicted = key

        return predicted, doc_class

    def _extract_features(self, documents):
        """
        Extract features from documents using specified vectorizer into numpy array.


        :param documents: The documents in dict format with keys 'title_seg' and 'desc_seg'.
        :return: numpy array
        """

        from scipy.sparse import hstack

        documents = self.copy(documents)

        title_data = [doc['title_seg'] for doc in documents]  # create a list of title data from documents.
        desc_data = [doc['desc_seg'] for doc in documents]  # create a list of desc data from documents.

        # transform-vectorize
        title_vec = self.vectorizer.vectorize_title.transform(title_data)
        desc_vec = self.vectorizer.vectorize_desc.transform(desc_data)
        # stack title onto desc
        data_vec = hstack([title_vec, desc_vec])

        return data_vec

    @staticmethod
    def _sample(dataset, size):
        """Return a random sample of size=size from a list dataset."""

        import random

        return [dataset[i] for i in sorted(random.sample(len(dataset), size))]

    def train_classifier(self, documents, pos_label, classifier):
        """
        Train the classifier.


        :param documents: The documents in dict format with keys 'title_seg', 'desc_seg' and 'label'.
                            by mean of which the classifier is to be trained.
        :param pos_label: Positive label on which classifier is to be trained.
        :param classifier: A classifier object with method fit, predict and predict_proba.
                            If not specified MultinomialNB from scikit-learn will be used.
        :return: Trained classifier object.
        """

        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report

        documents = self.copy(documents)
        if not classifier:
            from sklearn.naive_bayes import MultinomialNB
            classifier = MultinomialNB()

        # ========== separate classes of documents ==========
        pos_doc = []
        neg_doc = []
        for doc in documents:
            if doc['label'] == pos_doc:
                pos_doc.append(doc)
            else:
                neg_doc.append(doc)
        # ====================================================

        # =========== balancing between two classes ==========
        if len(pos_doc) > len(neg_doc):
            pos_doc = self._sample(pos_doc, len(neg_doc))
        elif len(pos_doc) < len(neg_doc):
            neg_doc = self._sample(neg_doc, len(pos_doc))
        # ====================================================

        # rename all negative labels.
        for index, _ in enumerate(neg_doc):
            neg_doc[index]['label'] = '!' + pos_label
        documents = pos_doc + neg_doc  # rejoin two classes.

        data_vec = self._extract_features(documents)  # extract feature from the documents.
        label_vec = [doc['label'] for doc in documents]  # create a table of document labels/classes.

        # === fit and show accuracy using train-test split. ===
        # split sample into train_set and test_set.
        desc_train, desc_test, label_train, label_test = train_test_split(data_vec, label_vec, test_size=0.3)
        model_split = classifier
        model_split.fit(desc_train, label_train)  # fit using training split.
        label_predict = model_split.predict(desc_test)  # predict the label of test set.
        print('============== Classification accuracy report for the Test Set. ==============')
        print(classification_report(label_vec, label_predict))  # print accuracy report for the test set.
        print('==============================================================================')

        # fit the model using the whole labeled data.
        model_full = classifier
        model_full.fit(data_vec, label_vec)

        return model_full

    def append(self, classifier):
        """
        Append classifier object to Classifier object.


        :param classifier: A classifier object with 'predict_proba' method.
        :return: None
        """

        self.classifiers.append(classifier)
        self.classes_.append(classifier.classes_[1])
        self.classes_.sort()

    def pop(self, classifier_name):
        """
        Remove classifier object from the Classifier object by specifying class name.


        :param classifier_name: The name of class of the classifier to remove.
        :return: None
        """

        # check if classifier_name exists
        if classifier_name not in self.classes_:
            return None

        for index, clf in enumerate(self.classifiers):
            if clf.classess_[1] == classifier_name:
                self.classifiers.pop(index)
        self.classes_.remove(classifier_name)

    def save_file(self, filename, filepath='./Resource/Classifier/'):
        """
        Write classifier object to a file.


        :param filename: Classifier object filename.
        :param filepath: Path to the directory where in the file is to be written.
        :return: None
        """

        import dill

        if filename.find('.') == -1:
            filename += '.clfs'
        filename = filepath + filename
        with open(filename, 'rb') as f_out:
            dill.dump(self, f_out)

    @staticmethod
    def read_pickle(filename):
        """
        Load Classifier object from a file


        :param filename: path to the file containing Classifier object.
        :return: Classifier object
        """

        import dill

        with open(filename, 'rb') as f_in:
            ret = dill.load(f_in)
        return ret
