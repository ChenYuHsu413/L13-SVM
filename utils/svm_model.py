"""SVM training utilities (thin wrapper around sklearn.svm.SVC)."""

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


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


def train_svm_with_split(
    X, y, kernel="rbf", C=1.0, gamma="scale", degree=3, test_size=0.3, random_state=42
):
    """Fit on a training split and report both training and test accuracy.

    Showing a held-out *test* accuracy makes overfitting visible: when C / gamma
    are too large the training accuracy stays high while the test accuracy drops.

    Returns
    -------
    model : SVC fitted on the training split
    train_acc, test_acc : float
    splits : tuple (X_train, y_train, X_test, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )
    model = SVC(kernel=kernel, C=C, gamma=gamma, degree=degree)
    model.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, model.predict(X_train))
    test_acc = accuracy_score(y_test, model.predict(X_test))
    return model, train_acc, test_acc, (X_train, y_train, X_test, y_test)
