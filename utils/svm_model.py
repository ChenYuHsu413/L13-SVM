"""SVM training utilities (thin wrapper around sklearn.svm.SVC)."""

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


def train_svm(X, y, kernel="rbf", C=1.0, gamma="scale", degree=3):
    """Train an SVC on (X, y) and return (model, training_accuracy).

    Parameters
    ----------
    X, y : arrays
        Features and labels.
    kernel : str
        "linear", "rbf", or "poly".
    C : float
        Regularization strength. Larger C -> less tolerance for misclassification.
    gamma : float or {"scale", "auto"}
        Kernel coefficient for "rbf" and "poly".
    degree : int
        Polynomial degree (only used by the "poly" kernel).

    Returns
    -------
    model : fitted SVC
    accuracy : float
        Training accuracy in [0, 1].
    """
    model = SVC(
        kernel=kernel,
        C=C,
        gamma=gamma,
        degree=degree,
    )
    model.fit(X, y)
    accuracy = accuracy_score(y, model.predict(X))
    return model, accuracy
