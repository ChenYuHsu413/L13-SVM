# 🧠 SVM 互動式教學網站

### 🚀 線上 Demo：<https://l13-svm-interactivatepage.streamlit.app/>

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://l13-svm-interactivatepage.streamlit.app/)

一個用 **Streamlit** 打造的「支持向量機（Support Vector Machine, SVM）」互動式教學網站。
透過 **scikit-learn** 即時訓練模型、用 **Plotly** 畫出真實的 decision boundary，
並搭配 **Manim** 預先渲染的概念動畫，帶學習者從直覺一路理解到數學與 Kernel Trick。

> 設計原則：**Streamlit 不會在雲端即時跑 Manim**。Manim 只在本機把動畫渲染成 mp4，
> 網站只負責用 `st.video()` 播放。互動式 SVM 視覺化則完全用 sklearn + Plotly 即時計算。

---

## 1. 專案介紹

多頁面教學網站，包含五個頁面：

| 頁面 | 內容 |
| --- | --- |
| 1. SVM Concept | SVM 直覺、二元分類、最大 margin 概念 |
| 2. Margin & Support Vectors | 決策函數、margin 公式、最佳化問題 |
| 3. Interactive SVM ⭐ | 核心互動頁：調 C / kernel / gamma / degree，即時看邊界 |
| 4. Kernel Trick | 為什麼需要 kernel、三種 kernel 比較 |
| 5. Quiz | 5 題小測驗 + 分數與解析 |

### 專案結構

```
L12-SVM/
├── app.py                  # 首頁 / Streamlit 入口
├── requirements.txt        # 部署所需套件（不含 manim）
├── README.md
├── .gitignore
│
├── assets/
│   ├── videos/             # 放預先渲染好的 mp4（執行前需自行產生）
│   └── images/
│
├── manim_scenes/           # Manim 動畫原始碼（只在本機渲染用）
│   ├── svm_margin_scene.py
│   ├── support_vectors_scene.py
│   └── kernel_trick_scene.py
│
├── utils/
│   ├── datasets.py         # generate_dataset()
│   ├── svm_model.py        # train_svm()
│   ├── plotting.py         # plot_decision_boundary()
│   ├── explanations.py     # 教學文字與對照表
│   └── media.py            # 安全播放影片（找不到時顯示提示）
│
└── pages/                  # Streamlit 多頁面
    ├── 1_SVM_Concept.py
    ├── 2_Margin_and_Support_Vectors.py
    ├── 3_Interactive_SVM.py
    ├── 4_Kernel_Trick.py
    └── 5_Quiz.py
```

---

## 2. 本機執行方式

建議使用虛擬環境（Python 3.9+）：

```bash
# 建立並啟用虛擬環境（Windows PowerShell）
python -m venv .venv
.venv\Scripts\Activate.ps1

# 安裝套件
pip install -r requirements.txt
```

> macOS / Linux 啟用虛擬環境改用 `source .venv/bin/activate`。

---

## 3. Manim 動畫渲染方式（本機，選用）

> ⚠️ Manim **不在** `requirements.txt`，也**不需要**部署到雲端。
> 只有當你想自己產生動畫時，才在本機額外安裝。

```bash
# 安裝 Manim（需另外安裝 ffmpeg；Windows 可用 winget/choco）
pip install manim
```

渲染三個 scene（`-pqh` = 預覽 + 高畫質）：

```bash
manim -pqh manim_scenes/svm_margin_scene.py SVMMarginScene
manim -pqh manim_scenes/support_vectors_scene.py SupportVectorsScene
manim -pqh manim_scenes/kernel_trick_scene.py KernelTrickScene
```

渲染後，Manim 會把 mp4 輸出到 `media/videos/<scene>/1080p60/` 之類的資料夾。
請把它們**複製並改名**到 `assets/videos/`，檔名必須是：

| 來源 scene | 目標檔名（放在 `assets/videos/`） |
| --- | --- |
| `SVMMarginScene` | `svm_margin_intro.mp4` |
| `SupportVectorsScene` | `support_vectors_intro.mp4` |
| `KernelTrickScene` | `kernel_trick_intro.mp4` |

> 💡 若影片不存在，網站**不會 crash**，會在對應位置顯示提示文字。
> 所以你可以先跑網站、之後再補影片。

---

## 4. Streamlit 本機啟動方式

```bash
streamlit run app.py
```

瀏覽器會自動開啟 `http://localhost:8501`，左側選單即是五個教學頁面。

---

## 5. 部署到 Streamlit Community Cloud

1. 把整個專案 **push 到 GitHub**（公開或私有 repo 皆可）。
   - 若要連影片一起部署，記得把 `assets/videos/*.mp4` 也 commit 進去
     （`.gitignore` 只忽略 Manim 的 `media/` 中介檔，不會忽略 `assets/videos/`）。
2. 登入 <https://streamlit.io>（Community Cloud）。
3. 點 **New app**，選擇你的 GitHub repo 與 branch。
4. **Main file path** 設為 `app.py`。
5. 按 **Deploy**，等待安裝 `requirements.txt` 後即上線。

> 雲端只會安裝 `requirements.txt` 裡的套件（不含 manim），啟動快又穩定。

---

## 6. 常見問題排除（FAQ）

**Q：頁面顯示「影片尚未產生」？**
A：正常。請依第 3 節用 Manim 在本機渲染，並把 mp4 放到 `assets/videos/`（檔名要對）。
未放影片不影響其他功能。

**Q：`st.plotly_chart` 圖很慢？**
A：把 `n_samples` 調小（建議 100–300）。decision boundary 的格點解析度在 `utils/plotting.py`
的 `_make_mesh(resolution=...)` 可調低以加速。

**Q：按「下載 PNG」沒反應 / 報錯？**
A：Plotly 匯出靜態圖需要 `kaleido`：`pip install kaleido`。
未安裝時網站會改提示你用圖表右上角相機 icon 下載，不會 crash。

**Q：`poly` kernel 跑很久？**
A：degree 較高 + 樣本多時計算較重，屬正常現象，降低 degree 或 n_samples 即可。

**Q：找不到 `utils` 模組（ModuleNotFoundError）？**
A：請確定是用 `streamlit run app.py` 從**專案根目錄**啟動，而不是進到 `pages/` 內執行。

---

## 套件說明（requirements.txt）

| 套件 | 用途 |
| --- | --- |
| streamlit | 網站框架 |
| scikit-learn | 產生資料集 + 訓練 SVC |
| numpy | 數值運算 / 格點 |
| pandas | 表格顯示（參數摘要、對照表） |
| matplotlib | sklearn 相依與備用繪圖 |
| plotly | 互動式 decision boundary 圖表 |

> 選用：`kaleido`（PNG 下載）、`manim`（本機渲染動畫）。兩者皆**非部署必需**。
