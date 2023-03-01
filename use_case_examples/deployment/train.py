import platform
import sys
import time
from shutil import copyfile
from tempfile import TemporaryDirectory

import numpy
from sklearn.datasets import load_breast_cancer

from concrete.ml.deployment import FHEModelClient, FHEModelDev, FHEModelServer
from concrete.ml.sklearn import XGBClassifier

if __name__ == "__main__":
    # Let's first get some data and train a model.
    X, y = load_breast_cancer(return_X_y=True)

    assert isinstance(X, numpy.ndarray)
    assert isinstance(y, numpy.ndarray)

    # Split X into X_model_owner and X_client
    X_train = X[:-10]
    y_train = y[:-10]

    # Train the model and compile it
    model = XGBClassifier(n_bits=2, n_estimators=8, max_depth=3)
    model.fit(X_train, y_train)

    # Until we have proper model serialization we need to compile and create client/server here
    # FIXME: https://github.com/zama-ai/concrete-ml-internal/issues/735
    model.compile(X_train)
    dev = FHEModelDev("./dev", model)
    dev.save()