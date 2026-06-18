"""Page 3 — Interactive SVM（核心互動頁）。"""

import numpy as np
import pandas as pd
import streamlit as st

from utils.datasets import DATASET_OPTIONS, generate_dataset
from utils.svm_model import train_svm_with_split
from utils.plotting import plot_decision_boundary, plot_decision_surface_3d
from utils.explanations import (
    explain_c_parameter,
    explain_gamma_parameter,
    explain_degree_parameter,
    explain_kernel,
    interpret_current_params,
    PARAM_TABLE,
)

st.set_page_config(page_title="Interactive SVM", page_icon="⭐", layout="wide")


# --- cached compute ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_dataset(dataset_key, n_samples, noise, random_state=42):
    return generate_dataset(dataset_key, n_samples, noise, random_state)


@st.cache_resource(show_spinner=False)
def get_model(dataset_key, n_samples, noise, kernel, C, gamma, degree):
    # Re-generate the same (cached) data, then fit on a train split. The cache key
    # includes every parameter so the model is re-fit only when something changes.
    X, y = get_dataset(dataset_key, n_samples, noise)
    model, train_acc, test_acc, splits = train_svm_with_split(
        X, y, kernel=kernel, C=C, gamma=gamma, degree=degree
    )
    return model, train_acc, test_acc, splits


# --- sidebar controls -------------------------------------------------------
st.sidebar.header("⚙️ SVM 參數設定")

dataset_label = st.sidebar.selectbox("資料集 Dataset", list(DATASET_OPTIONS.keys()))
dataset_key = DATASET_OPTIONS[dataset_label]

kernel = st.sidebar.selectbox("Kernel 核函數", ["linear", "rbf", "poly"], index=1)

# C uses a log-scale select_slider for a wide, intuitive range.
C_choices = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0]
C = st.sidebar.select_slider("C（懲罰參數）", options=C_choices, value=1.0)

# gamma only matters for rbf / poly.
gamma = "scale"
if kernel in ("rbf", "poly"):
    use_scale = st.sidebar.checkbox("gamma 使用 'scale'（自動）", value=True)
    if use_scale:
        gamma = "scale"
    else:
        gamma = st.sidebar.slider("gamma", 0.001, 10.0, 1.0, step=0.001, format="%.3f")

# degree only matters for poly.
degree = 3
if kernel == "poly":
    degree = st.sidebar.slider("degree（多項式次數）", 2, 5, 3)

noise = st.sidebar.slider("Noise 雜訊", 0.0, 0.5, 0.1, step=0.05)
n_samples = st.sidebar.slider("n_samples 資料量", 100, 500, 200, step=50)


# --- main panel -------------------------------------------------------------
st.title("3️⃣ Interactive SVM ⭐")
st.markdown("調整左側參數，即時觀察 **decision boundary**、**support vectors** 與 **accuracy** 的變化。")

X, y = get_dataset(dataset_key, n_samples, noise)
model, train_acc, test_acc, splits = get_model(dataset_key, n_samples, noise, kernel, C, gamma, degree)
X_train, y_train, X_test, y_test = splits

n_sv = int(len(model.support_vectors_))
sv_ratio = n_sv / len(X_train)
acc_gap = train_acc - test_acc

col_plot, col_info = st.columns([3, 2])

with col_plot:
    tab_2d, tab_3d = st.tabs(["🗺️ 2D 邊界", "⛰️ 3D 決策曲面"])

    with tab_2d:
        fig = plot_decision_boundary(
            X_train, y_train, model, title=f"{kernel} kernel｜C={C}", X_test=X_test, y_test=y_test
        )
        st.plotly_chart(fig, use_container_width=True)
        if kernel == "linear":
            st.caption("● 訓練點｜◆ 測試點｜黑實線：decision boundary｜灰虛線：margin（f(x)=±1）｜黑圈：support vectors")
        else:
            st.caption("● 訓練點｜◆ 測試點｜黑實線：decision boundary｜黑圈：support vectors")

    with tab_3d:
        fig3d = plot_decision_surface_3d(X_train, y_train, model, title=f"{kernel} kernel 決策曲面")
        st.plotly_chart(fig3d, use_container_width=True)
        st.caption(
            "曲面高度 = `decision_function` f(x)｜灰色水平面為 z=0（即 decision boundary）｜"
            "黑點為 support vectors（約落在 f(x)=±1）。可用滑鼠拖曳旋轉。"
        )
        st.info(
            "💡 看 **rbf** kernel 時把資料切成 Circles，會看到一座座「山丘」穿過 z=0 平面；"
            "**linear** kernel 則是一個傾斜的平面。這就是 SVM 在做的事：找一個高度函數，"
            "讓兩類資料分別落在 z=0 的上方與下方。"
        )

with col_info:
    st.markdown("### 📊 模型結果")
    m1, m2 = st.columns(2)
    m1.metric("訓練準確率 (Train)", f"{train_acc:.1%}")
    m2.metric("測試準確率 (Test)", f"{test_acc:.1%}", delta=f"{-acc_gap:.1%}", delta_color="inverse")
    m3, m4 = st.columns(2)
    m3.metric("Support Vectors", n_sv)
    m4.metric("SV 佔比 (訓練集)", f"{sv_ratio:.1%}")
    st.caption("資料以 70%/30% 切成訓練/測試集；模型只看訓練集。測試準確率才代表對新資料的泛化能力。")

    st.markdown("#### 模型參數摘要")
    st.dataframe(
        pd.DataFrame(
            {
                "參數": ["kernel", "C", "gamma", "degree", "n_samples"],
                "值": [kernel, C, str(gamma), degree if kernel == "poly" else "—", n_samples],
            }
        ),
        hide_index=True,
        use_container_width=True,
    )

    st.markdown("#### 🧭 目前參數解讀")
    st.info(interpret_current_params(kernel, C, gamma, degree))

    # Overfitting / underfitting hint, driven by the honest train/test gap.
    if acc_gap >= 0.12 and train_acc >= 0.9:
        st.warning(
            f"⚠️ 訓練準確率高、但測試掉了 **{acc_gap:.1%}** → 典型 **overfitting**。"
            "可試著調小 C 或 gamma、或換較簡單的 kernel。"
        )
    elif train_acc < 0.7 and test_acc < 0.7:
        st.warning("⚠️ 訓練與測試準確率都偏低 → **underfitting**，可換 kernel 或調大 C / gamma。")
    else:
        st.success("✅ 訓練與測試準確率接近，模型泛化情況良好。")


st.divider()

st.markdown("### 📥 下載目前圖表")
try:
    img_bytes = fig.to_image(format="png", scale=2)  # needs the 'kaleido' package
    st.download_button("下載 PNG", img_bytes, file_name="svm_boundary.png", mime="image/png")
except Exception:
    st.caption(
        "（若要下載 PNG，請安裝 `kaleido`：`pip install kaleido`。"
        "你也可以直接用圖表右上角的相機 icon 下載。）"
    )

st.divider()

# --- teaching text ----------------------------------------------------------
st.markdown("### 📖 參數教學")
c1, c2 = st.columns(2)
with c1:
    st.markdown(explain_c_parameter())
    if kernel in ("rbf", "poly"):
        st.markdown(explain_gamma_parameter())
with c2:
    st.markdown(explain_kernel())
    if kernel == "poly":
        st.markdown(explain_degree_parameter())

st.markdown("#### 📋 參數效果對照表")
st.dataframe(pd.DataFrame(PARAM_TABLE), hide_index=True, use_container_width=True)

st.divider()
st.markdown("#### ➡️ 下一步建議")
st.info("選擇 **Moons / Circles** 資料集，把 kernel 切成 `linear`，看看為什麼需要 **Kernel Trick**（下一頁）。")
