"""Page 5 — Quiz（小測驗）。"""

import streamlit as st

st.set_page_config(page_title="Quiz", page_icon="📝", layout="wide")

st.title("5️⃣ SVM 小測驗")
st.markdown("作答後按下 **「送出答案」**，會顯示分數與每題解析。")

# Each question: prompt, options, correct index, explanation.
QUESTIONS = [
    {
        "q": "1. Support vectors（支持向量）是什麼？",
        "options": [
            "資料集中數值最大的點",
            "離 decision boundary 最近、決定 margin 的關鍵資料點",
            "被分類錯誤的所有點",
            "資料集的平均中心點",
        ],
        "answer": 1,
        "explain": "Support vectors 是離邊界最近、剛好落在 margin 上的點；只有它們決定邊界，刪掉其他點邊界也不變。",
    },
    {
        "q": "2. C 變大通常會造成什麼效果？",
        "options": [
            "margin 變寬，模型更寬鬆，容易 underfit",
            "對缺失值更穩健",
            "margin 變窄，模型更嚴格，容易 overfit",
            "完全不影響邊界",
        ],
        "answer": 2,
        "explain": "C 越大代表越不容忍錯誤分類，邊界貼合資料、margin 變窄，容易 overfitting。",
    },
    {
        "q": "3. gamma 變大通常會造成什麼效果？",
        "options": [
            "邊界更平滑",
            "單點影響範圍變小，邊界更彎曲，容易 overfit",
            "只影響訓練速度，不影響邊界",
            "讓 linear kernel 變成 rbf",
        ],
        "answer": 1,
        "explain": "gamma 越大，單一資料點的影響範圍越小，邊界會更彎曲、更貼近個別點，容易 overfitting。",
    },
    {
        "q": "4. margin 越大代表什麼？",
        "options": [
            "模型一定 100% 正確",
            "訓練速度一定更快",
            "分類器對新資料的容忍度較高，泛化能力通常較好",
            "support vectors 一定變多",
        ],
        "answer": 2,
        "explain": "margin 越大，邊界離兩邊資料越遠，對沒看過的新資料更穩健，泛化能力通常更好。",
    },
    {
        "q": "5. RBF kernel 適合處理什麼資料？",
        "options": [
            "只有線性可分的資料",
            "非線性、需要彎曲邊界的資料",
            "只有文字資料",
            "只有一維資料",
        ],
        "answer": 1,
        "explain": "RBF kernel 能形成封閉、彎曲的邊界，最適合像 moons / circles 這種非線性資料。",
    },
]

user_answers = []
with st.form("quiz_form"):
    for i, item in enumerate(QUESTIONS):
        st.markdown(f"**{item['q']}**")
        choice = st.radio(
            label=item["q"],
            options=list(range(len(item["options"]))),
            format_func=lambda idx, opts=item["options"]: opts[idx],
            index=None,
            key=f"q_{i}",
            label_visibility="collapsed",
        )
        user_answers.append(choice)
        st.divider()
    submitted = st.form_submit_button("✅ 送出答案")

if submitted:
    score = 0
    for i, item in enumerate(QUESTIONS):
        chosen = user_answers[i]
        correct = item["answer"]
        if chosen == correct:
            score += 1
            st.success(f"第 {i + 1} 題 ✅ 正確！")
        elif chosen is None:
            st.warning(f"第 {i + 1} 題 ⬜ 未作答。正確答案：**{item['options'][correct]}**")
        else:
            st.error(
                f"第 {i + 1} 題 ❌ 你選了「{item['options'][chosen]}」，"
                f"正確答案是「**{item['options'][correct]}**」"
            )
        st.caption(f"💡 {item['explain']}")

    st.divider()
    total = len(QUESTIONS)
    st.markdown(f"## 🏆 你的分數：{score} / {total}（{score / total:.0%}）")
    if score == total:
        st.balloons()
        st.success("太強了！你已經完全掌握 SVM 的核心概念 🎉")
    elif score >= total * 0.6:
        st.info("不錯喔！再回頭複習錯的題目就更穩了。")
    else:
        st.warning("建議回到前面幾頁再複習一次 margin、C、gamma 與 kernel 的概念。")

st.divider()
st.markdown("#### ➡️ 下一步建議")
st.info("回到 **「3 Interactive SVM」** 多玩幾組參數，把概念和實際邊界對應起來，學習效果最好！")
