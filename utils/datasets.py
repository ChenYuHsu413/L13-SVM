"""Dataset generation utilities for the SVM teaching app.

All generators return a tuple (X, y) where:
  - X is an (n_samples, 2) float array (2D so we can draw it)
  - y is an (n_samples,) int array of class labels {0, 1}
"""

import numpy as np
from sklearn.datasets import (
    make_blobs,
    make_circles,
    make_classification,
    make_moons,
)

# Human-readable dataset names shown in the UI -> internal keys
DATASET_OPTIONS = {
    "線性可分 (Linearly separable)": "linear",
    "團塊 (Blobs)": "blobs",
    "月亮 (Moons)": "moons",
    "同心圓 (Circles)": "circles",
}


def generate_dataset(dataset_name, n_samples=200, noise=0.1, random_state=42):
    """Generate a 2D binary-classification dataset.

    Parameters
    ----------
    dataset_name : str
        One of the internal keys: "linear", "blobs", "moons", "circles".
    n_samples : int
        Number of points (recommended 100-500).
    noise : float
        Noise level (0 - 0.5). Interpretation depends on the dataset.
    random_state : int
        Reproducibility seed.

    Returns
    -------
    X : np.ndarray, shape (n_samples, 2)
    y : np.ndarray, shape (n_samples,)
    """
    if dataset_name == "linear":
        # make_classification with 2 informative features, no redundancy.
        # class_sep grows as noise shrinks so the data stays visibly separable.
        X, y = make_classification(
            n_samples=n_samples,
            n_features=2,
            n_informative=2,
            n_redundant=0,
            n_repeated=0,
            n_clusters_per_class=1,
            class_sep=2.0 - 2.0 * noise,
            flip_y=noise * 0.2,
            random_state=random_state,
        )
    elif dataset_name == "blobs":
        X, y = make_blobs(
            n_samples=n_samples,
            centers=2,
            n_features=2,
            cluster_std=1.0 + 3.0 * noise,
            random_state=random_state,
        )
    elif dataset_name == "moons":
        X, y = make_moons(
            n_samples=n_samples,
            noise=noise,
            random_state=random_state,
        )
    elif dataset_name == "circles":
        X, y = make_circles(
            n_samples=n_samples,
            noise=noise,
            factor=0.5,
            random_state=random_state,
        )
    else:
        raise ValueError(f"Unknown dataset_name: {dataset_name!r}")

    return X.astype(float), y.astype(int)
