"""Plotly-based visualisation of SVM decision boundaries.

The main entry point is `plot_decision_boundary`, which draws:
  - filled decision regions (predicted class on a grid)
  - the decision boundary and (for linear kernels) the margin lines
  - the data points coloured by true label
  - the support vectors, circled
"""

import numpy as np
import plotly.graph_objects as go


# Colours kept consistent across the whole app.
CLASS_COLORS = ["#1f77b4", "#d62728"]  # class 0 (blue), class 1 (red)
REGION_COLORSCALE = [[0.0, "#cfe3f5"], [1.0, "#f7d4d4"]]


def _make_mesh(X, padding=0.5, resolution=300):
    """Build a 2D grid covering the data extent (plus padding)."""
    x_min, x_max = X[:, 0].min() - padding, X[:, 0].max() + padding
    y_min, y_max = X[:, 1].min() - padding, X[:, 1].max() + padding
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, resolution),
        np.linspace(y_min, y_max, resolution),
    )
    return xx, yy


def plot_decision_boundary(X, y, model, title="SVM Decision Boundary", X_test=None, y_test=None):
    """Return a Plotly Figure showing the decision boundary for `model`.

    Parameters
    ----------
    X, y : training points drawn as filled circles (these define the SVs shown).
    model : fitted sklearn SVC
    title : str
    X_test, y_test : optional held-out points, drawn as diamonds so students can
        see how unseen data falls relative to the boundary.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    xx, yy = _make_mesh(X)
    grid = np.c_[xx.ravel(), yy.ravel()]

    # Predicted class for each grid cell -> filled regions.
    Z_pred = model.predict(grid).reshape(xx.shape)
    # Signed distance to the boundary -> contour lines (boundary + margins).
    Z_dec = model.decision_function(grid).reshape(xx.shape)

    fig = go.Figure()

    # 1) Decision regions (filled background).
    fig.add_trace(
        go.Heatmap(
            x=xx[0],
            y=yy[:, 0],
            z=Z_pred,
            colorscale=REGION_COLORSCALE,
            showscale=False,
            opacity=0.55,
            hoverinfo="skip",
        )
    )

    # 2) Decision boundary (decision_function == 0) and margins (== +/-1).
    is_linear = getattr(model, "kernel", None) == "linear"
    margin_levels = [-1, 0, 1] if is_linear else [0]
    for level in margin_levels:
        is_boundary = level == 0
        fig.add_trace(
            go.Contour(
                x=xx[0],
                y=yy[:, 0],
                z=Z_dec,
                showscale=False,
                contours=dict(
                    start=level,
                    end=level,
                    size=1,
                    coloring="none",
                ),
                line=dict(
                    width=3 if is_boundary else 1.5,
                    color="black" if is_boundary else "gray",
                    dash="solid" if is_boundary else "dash",
                ),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    # 3) Data points, coloured by true label.
    for cls in np.unique(y):
        mask = y == cls
        fig.add_trace(
            go.Scatter(
                x=X[mask, 0],
                y=X[mask, 1],
                mode="markers",
                name=f"Class {cls}",
                marker=dict(
                    color=CLASS_COLORS[int(cls) % len(CLASS_COLORS)],
                    size=8,
                    line=dict(width=1, color="white"),
                ),
            )
        )

    # 3b) Held-out test points (optional), drawn as diamonds.
    if X_test is not None and y_test is not None:
        for cls in np.unique(y_test):
            mask = y_test == cls
            fig.add_trace(
                go.Scatter(
                    x=X_test[mask, 0],
                    y=X_test[mask, 1],
                    mode="markers",
                    name=f"Test Class {cls}",
                    marker=dict(
                        color=CLASS_COLORS[int(cls) % len(CLASS_COLORS)],
                        size=9,
                        symbol="diamond",
                        opacity=0.6,
                        line=dict(width=1, color="black"),
                    ),
                )
            )

    # 4) Support vectors, circled.
    if hasattr(model, "support_vectors_") and len(model.support_vectors_) > 0:
        sv = model.support_vectors_
        fig.add_trace(
            go.Scatter(
                x=sv[:, 0],
                y=sv[:, 1],
                mode="markers",
                name="Support Vectors",
                marker=dict(
                    color="rgba(0,0,0,0)",
                    size=16,
                    line=dict(width=2.5, color="black"),
                    symbol="circle",
                ),
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title="Feature 1",
        yaxis_title="Feature 2",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=60, b=10),
        height=560,
    )
    fig.update_xaxes(constrain="domain")
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


def plot_decision_surface_3d(X, y, model, title="Decision Function Surface (3D)"):
    """Return a Plotly 3D Figure of the SVM decision function as a surface.

    The surface height is z = model.decision_function(x1, x2). The flat grey
    plane at z = 0 is the decision boundary; data points sit at their own
    decision values, so points of each class land on opposite sides of z = 0.

    A coarser grid (resolution ~80) keeps the 3D surface responsive.
    """
    xx, yy = _make_mesh(X, padding=0.5, resolution=80)
    grid = np.c_[xx.ravel(), yy.ravel()]
    Z = model.decision_function(grid).reshape(xx.shape)

    fig = go.Figure()

    # 1) The decision function surface. reversescale -> high f(x) red (class 1),
    #    low f(x) blue (class 0), matching the 2D colours.
    fig.add_trace(
        go.Surface(
            x=xx[0],
            y=yy[:, 0],
            z=Z,
            colorscale="RdBu",
            reversescale=True,
            opacity=0.9,
            showscale=True,
            colorbar=dict(title="f(x)"),
            contours={
                "z": {
                    "show": True,
                    "usecolormap": True,
                    "highlightcolor": "limegreen",
                    "project_z": True,
                }
            },
            name="f(x)",
        )
    )

    # 2) The z = 0 plane (the decision boundary lives where the surface crosses it).
    fig.add_trace(
        go.Surface(
            x=xx[0],
            y=yy[:, 0],
            z=np.zeros_like(Z),
            colorscale=[[0, "gray"], [1, "gray"]],
            showscale=False,
            opacity=0.3,
            hoverinfo="skip",
            name="z = 0",
        )
    )

    # 3) Data points placed at their own decision-function value.
    d_vals = model.decision_function(X)
    for cls in np.unique(y):
        mask = y == cls
        fig.add_trace(
            go.Scatter3d(
                x=X[mask, 0],
                y=X[mask, 1],
                z=d_vals[mask],
                mode="markers",
                name=f"Class {cls}",
                marker=dict(
                    size=4,
                    color=CLASS_COLORS[int(cls) % len(CLASS_COLORS)],
                    line=dict(width=0.5, color="white"),
                ),
            )
        )

    # 4) Support vectors (they sit near the +/-1 margin levels).
    if hasattr(model, "support_vectors_") and len(model.support_vectors_) > 0:
        sv = model.support_vectors_
        sv_z = model.decision_function(sv)
        fig.add_trace(
            go.Scatter3d(
                x=sv[:, 0],
                y=sv[:, 1],
                z=sv_z,
                mode="markers",
                name="Support Vectors",
                marker=dict(size=6, color="black", symbol="circle", opacity=0.9),
            )
        )

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="Feature 1",
            yaxis_title="Feature 2",
            zaxis_title="decision_function  f(x)",
        ),
        height=620,
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=0, xanchor="right", x=1),
    )
    return fig
