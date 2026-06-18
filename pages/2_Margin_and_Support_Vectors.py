"""Page 2 — Margin 與 Support Vectors。"""

import streamlit as st

from utils.media import play_video
from utils.explanations import explain_support_vectors, explain_margin

st.set_page_config(page_title="Margin 與 Support Vectors", page_icon="📏", layout="wide")

st.title("2️⃣ Margin 與 Support Vectors")

st.markdown("### 🧮 決策函數（Decision Function）")
st.latex(r"f(x) = w \cdot x + b")
st.markdown("分類規則是看 $f(x)$ 的正負號：")
st.latex(r"\hat{y} = \operatorname{sign}(w \cdot x + b)")
st.markdown("- $f(x) > 0$ → 判為一類；$f(x) < 0$ → 判為另一類；$f(x) = 0$ → 剛好在邊界上。")

st.divider()

st.markdown("### 📏 Margin 公式")
st.latex(r"\text{margin} = \frac{2}{\lVert w \rVert}")
st.markdown(
    "margin 是兩條虛線（$f(x)=+1$ 與 $f(x)=-1$）之間的距離。"
    "要讓 margin **變大**，就要讓 $\\lVert w \\rVert$ **變小**。"
)

st.divider()

st.markdown("### 🎯 SVM 的最佳化問題")
st.latex(r"\min_{w,b} \; \tfrac{1}{2}\lVert w \rVert^2")
st.latex(r"\text{subject to}\quad y_i\,(w \cdot x_i + b) \ge 1,\quad \forall i")

st.markdown(
    """
#### 為什麼要最小化 $\\tfrac{1}{2}\\lVert w \\rVert^2$？

- 我們真正想要的是**最大化 margin = 2 / ||w||**。
- 最大化 $2/\\lVert w \\rVert$ 等同於**最小化 $\\lVert w \\rVert$**。
- 為了數學上好微分、好求解，改寫成最小化 $\\tfrac{1}{2}\\lVert w \\rVert^2$（平方去掉根號、$\\tfrac12$ 讓微分更乾淨）。
- 限制式 $y_i(w \\cdot x_i + b) \\ge 1$ 要求**每個點都被正確分類，而且落在 margin 之外**。
    """
)

st.divider()
st.subheader("🎬 概念動畫：Support Vectors")
play_video("support_vectors_intro.mp4", caption="只有離邊界最近的那幾個點，才會決定 margin")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.markdown(explain_support_vectors())
with col2:
    st.markdown(explain_margin())
    st.success(
        "關鍵直覺：把遠離邊界的點刪掉，邊界完全不變；"
        "只有 **support vectors** 真正影響邊界。"
    )

st.divider()
st.markdown("#### ➡️ 下一步建議")
st.info("前往 **「3 Interactive SVM」**，親手調整 C / kernel / gamma，看真實邊界怎麼變化。")
