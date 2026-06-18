"""SVM 互動式教學網站 — 首頁 (entry point).

執行方式：
    streamlit run app.py

側邊欄會自動列出 pages/ 內的多頁面。
"""

import streamlit as st

st.set_page_config(
    page_title="SVM 互動式教學",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 SVM 互動式教學網站")
st.subheader("Support Vector Machine：從直覺到實作")

st.markdown(
    """
歡迎來到 **支持向量機（SVM）** 的互動式教學！

這個網站會帶你一步步理解 SVM 的核心概念，並且可以**親手調整參數、即時看到 decision boundary 的變化**。

#### 📚 學習路線（請依左側選單由上而下進行）

1. **SVM 是什麼？** — 直覺介紹、最大 margin 的概念
2. **Margin 與 Support Vectors** — 背後的數學與最佳化問題
3. **Interactive SVM** — ⭐ 核心互動頁，調參數看真實邊界
4. **Kernel Trick** — 為什麼 SVM 能處理非線性資料
5. **Quiz** — 小測驗，檢驗學習成果

---

#### 🔧 這個網站怎麼運作？

- 概念動畫由 **Manim** 在本機預先渲染成影片，網站只負責播放。
- 互動式的 decision boundary 由 **scikit-learn + Plotly** 即時計算與繪製。
- 你可以自由調整 `C`、`kernel`、`gamma`、`degree` 等參數，立即看到效果。
    """
)

st.info("👈 從左側選單選擇 **「1 SVM Concept」** 開始吧！")

with st.expander("ℹ️ 給老師 / 開發者：影片尚未顯示？"):
    st.markdown(
        """
        概念動畫需要先在本機用 Manim 渲染，再把 mp4 放到 `assets/videos/`：

        ```bash
        manim -pqh manim_scenes/svm_margin_scene.py SVMMarginScene
        manim -pqh manim_scenes/support_vectors_scene.py SupportVectorsScene
        manim -pqh manim_scenes/kernel_trick_scene.py KernelTrickScene
        ```

        渲染完成後，把對應的 mp4 複製成下列檔名放進 `assets/videos/`：
        `svm_margin_intro.mp4`、`support_vectors_intro.mp4`、`kernel_trick_intro.mp4`。

        若影片不存在，網站會顯示提示文字，不會 crash。
        """
    )
