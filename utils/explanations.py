"""Teaching text (Traditional Chinese) reused across pages.

Each function returns a Markdown string so pages can drop it straight into
`st.markdown(...)`. Keeping the copy here avoids duplicating wording per page.
"""


def explain_c_parameter():
    return (
        "**C（懲罰參數 / Regularization）**\n\n"
        "- C 越大：模型越**不容忍**分類錯誤，會努力把每個點分對，margin 較窄，"
        "邊界較貼合資料，容易 **overfit**。\n"
        "- C 越小：允許更多錯誤分類，margin 較寬、邊界較平滑，容易 **underfit**。\n\n"
        "可以把 C 想成「犯錯的罰款」：罰款越高，模型越不敢犯錯。"
    )


def explain_gamma_parameter():
    return (
        "**gamma（RBF / poly kernel 的影響範圍）**\n\n"
        "- gamma 越大：單一資料點的影響範圍越**小**，邊界會變得更彎曲、更貼近個別點，"
        "容易 overfit。\n"
        "- gamma 越小：影響範圍越**大**，邊界更平滑。\n\n"
        "`scale`（預設）會依特徵變異數自動決定，通常是不錯的起點。"
    )


def explain_degree_parameter():
    return (
        "**degree（poly kernel 的多項式次數）**\n\n"
        "- 只有 `poly` kernel 會用到。\n"
        "- degree 越高，特徵空間越複雜，邊界可以越彎曲，但也越容易 overfit、計算越慢。"
    )


def explain_kernel():
    return (
        "**Kernel（核函數）決定邊界的形狀**\n\n"
        "- `linear`：直線邊界，適合**線性可分**的資料。\n"
        "- `rbf`：可產生彎曲、封閉的邊界，適合**非線性**資料（最常用）。\n"
        "- `poly`：多項式特徵空間，degree 越高邊界越複雜。"
    )


def explain_support_vectors():
    return (
        "**Support Vectors（支持向量）**\n\n"
        "就是**離邊界最近、決定 margin 的那幾個資料點**。\n\n"
        "SVM 的邊界只由這些點決定 —— 把其他遠離邊界的點刪掉，邊界也不會改變。"
        "這也是「Support（支撐）Vector」名稱的由來。"
    )


def explain_margin():
    return (
        "**Margin（間隔）**\n\n"
        "margin 是邊界到最近資料點的距離，公式為 **margin = 2 / ||w||**。\n\n"
        "SVM 的目標就是找出**讓 margin 最大**的那條邊界 —— margin 越大，"
        "代表分類器對新資料的容忍度越高，泛化能力通常越好。"
    )


# --- Reference tables (used as bonus content) --------------------------------

KERNEL_TABLE = [
    {"Kernel": "linear", "適用情境": "線性可分資料", "邊界形狀": "直線", "備註": "速度快、可解釋性高"},
    {"Kernel": "rbf", "適用情境": "非線性、彎曲邊界", "邊界形狀": "曲線 / 封閉區域", "備註": "最常用，需調 gamma"},
    {"Kernel": "poly", "適用情境": "多項式關係", "邊界形狀": "多項式曲線", "備註": "degree 越高越複雜"},
]

PARAM_TABLE = [
    {"參數": "C", "變大的效果": "margin 變窄、容易 overfit", "變小的效果": "margin 變寬、容易 underfit"},
    {"參數": "gamma", "變大的效果": "邊界更彎曲、容易 overfit", "變小的效果": "邊界更平滑"},
    {"參數": "degree", "變大的效果": "邊界更複雜（僅 poly）", "變小的效果": "邊界較簡單"},
]


def interpret_current_params(kernel, C, gamma, degree):
    """Return a short Chinese interpretation of the current parameter combo."""
    lines = [f"目前使用 **{kernel}** kernel，C = **{C}**。"]
    if C >= 10:
        lines.append("C 偏大：模型嚴格、margin 較窄，留意 **overfitting**。")
    elif C <= 0.1:
        lines.append("C 偏小：模型寬鬆、margin 較寬，留意 **underfitting**。")
    else:
        lines.append("C 適中：在容錯與 margin 之間取得平衡。")

    if kernel in ("rbf", "poly"):
        lines.append(f"gamma = **{gamma}**。" + ("gamma 偏大時邊界會更彎曲。" if gamma != "scale" else ""))
    if kernel == "poly":
        lines.append(f"degree = **{degree}**，次數越高邊界越複雜。")
    return "\n\n".join(lines)
