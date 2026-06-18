"""Page 4 — Kernel Trick。"""

import pandas as pd
import streamlit as st

from utils.datasets import generate_dataset
from utils.svm_model import train_svm
from utils.plotting import (
    plot_decision_boundary,
    plot_decision_surface_3d,
    plot_kernel_lift_animation,
)
from utils.media import play_video
from utils.explanations import KERNEL_TABLE

st.set_page_config(page_title="Kernel Trick", page_icon="🌀", layout="wide")


@st.cache_resource(show_spinner=False)
def fit_for_kernel(dataset_key, n_samples, noise, kernel):
    X, y = generate_dataset(dataset_key, n_samples, noise)
    model, acc = train_svm(X, y, kernel=kernel, C=1.0, gamma="scale", degree=3)
    return X, y, model, acc


st.title("4️⃣ Kernel Trick（核技巧）")

st.markdown(
    """
### 🤔 為什麼 linear kernel 處理不了 circles / moons？

像**同心圓（circles）**或**月亮（moons）**這種資料，沒辦法用一條直線分開。
無論直線怎麼擺，都會切錯一堆點。

### 💡 Kernel Trick 的直覺
Kernel Trick 的想法是：**把資料映射到更高維的空間**，在那裡原本「彎曲」的分界
就可能變成一個「平的」超平面，於是又能用線性方式分開了。

最神奇的是 —— SVM **不需要真的算出高維座標**，只要用 kernel 函數計算點與點的相似度即可，
所以計算上非常有效率。這就是「Trick（技巧）」的精髓。

- **RBF kernel**：用「距離」衡量相似度，能形成封閉、彎曲的邊界，最適合非線性資料。
    """
)

st.divider()
st.subheader("🎬 概念動畫：Kernel Trick")
play_video("kernel_trick_intro.mp4", caption="資料被映射到高維空間後，就能用平面分開")

st.divider()

# --- interactive lift animation ---------------------------------------------
st.subheader("🕹️ 互動升維動畫：自己玩玩看")
st.markdown(
    "下面是**可互動**的版本（Plotly，瀏覽器即時運算）。"
    "按 **▶ 播放** 看同心圓被升維到 3D、平面切入；改下面的參數會**即時重建**。"
)

lift_label = st.radio(
    "升維方式",
    ["多項式 z = x²+y²", "RBF z = exp(-γ·r²)"],
    horizontal=True,
    key="lift_mode",
)
lift_mode = "rbf" if "RBF" in lift_label else "poly"

a1, a2, a3 = st.columns(3)
with a1:
    anim_noise = st.slider("Noise 雜訊", 0.0, 0.2, 0.06, step=0.02, key="anim_noise")
with a2:
    lift_strength = st.slider("升維強度（高度縮放）", 0.5, 4.0, 2.0, step=0.5, key="lift")
with a3:
    gamma = st.slider("gamma（僅 RBF）", 0.2, 5.0, 1.0, step=0.2, key="lift_gamma", disabled=(lift_mode == "poly"))

X_anim, y_anim = generate_dataset("circles", n_samples=200, noise=anim_noise)
anim_fig = plot_kernel_lift_animation(
    X_anim, y_anim, lift_strength=lift_strength, mode=lift_mode, gamma=gamma
)
st.plotly_chart(anim_fig, use_container_width=True)

if lift_mode == "rbf":
    st.caption(
        "RBF：用「到中心的高斯相似度」當高度 → **內圈隆起成山頂、外圈在山腳**（與多項式上下相反）。"
        "拉 gamma 看山丘變胖變瘦。註：RBF 真正的特徵空間是無限維，這是以中心為 landmark 的簡化示意。"
    )
else:
    st.caption(
        "多項式：用半徑平方當高度 → **內圈留在低處、外圈升到高處**，綠色平面從中間切開。"
        "這是 poly kernel（degree 2）的精確特徵映射。"
    )

st.divider()

# --- interactive comparison -------------------------------------------------
st.subheader("🔬 互動比較：同一份非線性資料，三種 kernel 的差異")

c1, c2 = st.columns(2)
with c1:
    dataset_label = st.radio("選擇資料集", ["同心圓 (Circles)", "月亮 (Moons)"], horizontal=True)
with c2:
    noise = st.slider("Noise 雜訊", 0.0, 0.3, 0.1, step=0.05)

dataset_key = "circles" if "Circles" in dataset_label else "moons"
n_samples = 300

tab_2d, tab_3d = st.tabs(["🗺️ 2D 邊界對比", "⛰️ 3D 決策曲面對比"])

with tab_2d:
    cols = st.columns(3)
    for col, kernel in zip(cols, ["linear", "rbf", "poly"]):
        with col:
            X, y, model, acc = fit_for_kernel(dataset_key, n_samples, noise, kernel)
            st.markdown(f"**{kernel} kernel** — accuracy: `{acc:.1%}`")
            fig = plot_decision_boundary(X, y, model, title=f"{kernel}")
            fig.update_layout(height=380, showlegend=False)
            st.plotly_chart(fig, use_container_width=True, key=f"2d_{kernel}")

with tab_3d:
    st.caption("曲面高度 = `decision_function`，灰色平面為 z=0（邊界）。可拖曳旋轉，對比三種 kernel 的「地形」。")
    cols3d = st.columns(3)
    for col, kernel in zip(cols3d, ["linear", "rbf", "poly"]):
        with col:
            X, y, model, acc = fit_for_kernel(dataset_key, n_samples, noise, kernel)
            st.markdown(f"**{kernel} kernel** — accuracy: `{acc:.1%}`")
            fig = plot_decision_surface_3d(X, y, model, title=kernel)
            fig.update_layout(height=420, showlegend=False)
            fig.update_traces(showscale=False, selector=dict(type="surface"))
            st.plotly_chart(fig, use_container_width=True, key=f"3d_{kernel}")

st.info(
    "👀 觀察：`linear` 的曲面是一個**斜平面**，z=0 切出的是直線，分不開彎曲資料；"
    "`rbf` 的曲面像**山丘/盆地**，能沿著資料彎曲；`poly` 介於兩者之間。"
)

st.divider()

st.markdown("### 📋 不同 kernel 的適用情境")
st.dataframe(pd.DataFrame(KERNEL_TABLE), hide_index=True, use_container_width=True)

st.markdown(
    """
- **linear kernel**：適合線性可分資料，速度快、好解釋。
- **rbf kernel**：適合非線性、彎曲邊界，最常用，但要調 `gamma`。
- **poly kernel**：使用多項式特徵空間，`degree` 越高邊界越複雜。
    """
)

st.divider()
st.markdown("#### ➡️ 下一步建議")
st.info("前往 **「5 Quiz」**，用 5 題小測驗檢驗你的學習成果！")
