"""Page 1 — SVM 是什麼？"""

import streamlit as st

from utils.media import play_video
from utils.explanations import explain_margin, explain_support_vectors

st.set_page_config(page_title="SVM 是什麼？", page_icon="🧠", layout="wide")

st.title("1️⃣ SVM 是什麼？")

st.markdown(
    """
**支持向量機（Support Vector Machine, SVM）** 是一種強大的**監督式分類**演算法。

### 🎯 二元分類問題
假設我們有兩群資料（例如：紅色點 vs 藍色點），目標是找一條線（在高維是一個 **hyperplane 超平面**）
把它們分開，之後遇到新資料就能判斷它屬於哪一邊。

### 🤔 為什麼不是隨便找一條分隔線？
能把兩群資料分開的線有**無限多條**。但它們的「品質」不一樣：

- 太靠近某一群的線，遇到稍微不同的新資料就會分錯。
- SVM 認為最好的線，是**離兩邊資料都最遠**的那條 —— 也就是 **margin（間隔）最大** 的線。

### 📏 最大 Margin 的概念
> SVM 會選擇 **margin 最大** 的那條 hyperplane。

margin 越大，分類器越「穩」，對沒看過的新資料容忍度越高（泛化能力更好）。
    """
)

st.divider()
st.subheader("🎬 概念動畫：最大 Margin")
play_video("svm_margin_intro.mp4", caption="SVM 如何在眾多分隔線中選出 margin 最大的那一條")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🔑 三個關鍵名詞")
    st.markdown(
        """
- **Hyperplane（超平面）**：用來分開兩類的決策邊界。在 2D 是一條線，3D 是一個平面。
- **Margin（間隔）**：邊界到最近資料點的距離（兩側合計為 2/||w||）。
- **Support Vector（支持向量）**：剛好落在 margin 邊上、決定邊界位置的關鍵資料點。
        """
    )
with col2:
    st.markdown("### 💡 一句話總結")
    st.success("SVM = 找出一條「離兩邊都最遠」的分隔線，讓分類最穩健。")
    st.markdown(explain_margin())

with st.expander("延伸：什麼是 Support Vectors？（下一頁會深入）"):
    st.markdown(explain_support_vectors())

st.divider()
st.markdown("#### ➡️ 下一步建議")
st.info("前往 **「2 Margin and Support Vectors」**，看看 margin 背後的數學公式。")
