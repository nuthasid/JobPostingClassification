from sklearn.naive_bayes import MultinomialNB


class MultiNB(MultinomialNB):
    """
    Modified implementation of scikit-learn MultinomialNB by replacing predict method
    with the one where cut-off probability can be specified.
    """

    def __init__(self, cutoff):
        """
        init MultiNB class.

        :param cutoff: The cut-off probability at which classes are separated.
        """
        super(MultiNB, self).__init__()
        self.cutoff = cutoff
        # cutoff = {'label':cutoff,...}

    def predict(self, datavec):
        """Modified implementation of the vanilla .predict method."""
        predict_proba = self.predict_proba(datavec)
        predicted = []
        for index in range(len(predict_proba)):
            item_predict = None
            for class_index, class_ in enumerate(self.classes_):
                if predict_proba[index][class_index] > self.cutoff[class_]:
                    item_predict = class_
            predicted.append(item_predict)
        return predicted
