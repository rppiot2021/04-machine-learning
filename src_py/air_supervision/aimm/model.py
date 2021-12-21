from sklearn import multioutput, svm, exceptions
import aimm.plugins
import numpy
import pickle


@aimm.plugins.model
class MultiOutputSVR(aimm.plugins.Model):

    def __init__(self):
        self._model = multioutput.MultiOutputRegressor(
            svm.SVR(C=2000))

    def fit(self, x, y):
        self._model.fit(x, y)
        return self

    def predict(self, x):
        try:
            x = numpy.array(x).reshape(1, -1)
            return self._model.predict(x).reshape(-1).tolist()
        except exceptions.NotFittedError:
            return []

    def serialize(self):
        return pickle.dumps(self)

    @classmethod
    def deserialize(self, b):
        return pickle.loads(b)
