請依以下內容，生成一張清晰的「專案架構＋工作流程」資訊圖表（infographic）。
風格：教學科技感、藍紅配色（對應 SVM 兩類資料）、分區塊、含流程箭頭。

═══════════════════════════════════════
專案名稱：SVM 互動式教學網站
一句話定位：用 Streamlit + scikit-learn + Plotly 打造的「支持向量機」互動教學網站，
            搭配 Manim 預渲染動畫，從直覺、數學到 Kernel Trick 完整教學。
線上 Demo：https://l13-svm-interactivatepage.streamlit.app/
GitHub：https://github.com/ChenYuHsu413/L13-SVM
═══════════════════════════════════════

【技術棧 Tech Stack】
- 前端/框架：Streamlit（多頁面 multi-page app）
- 機器學習：scikit-learn（SVC 模型、make_classification/blobs/moons/circles 資料集）
- 視覺化：Plotly（2D 決策邊界 + 3D 決策曲面，可互動旋轉）
- 概念動畫：Manim（僅本機離線渲染成 mp4）
- 語言：Python 3.12

【核心設計原則 Design Principle】
★ 關鍵：Streamlit 雲端「不」即時跑 Manim
  → Manim 只在本機把概念動畫渲染成 mp4
  → 網站只用 st.video() 播放預渲染影片
  → 互動式 SVM 視覺化才用 sklearn + Plotly 即時計算
  → 部署輕量穩定（requirements.txt 不含 manim）

【兩條工作流程 Workflow（重點，請用箭頭呈現）】

流程 A：離線動畫管線（本機，一次性）
  撰寫 Manim Scene（.py）
    → 本機渲染 manim -qh ...（用獨立 Python 3.12 環境）
    → 輸出 mp4
    → 複製到 assets/videos/
    → commit 進 GitHub

流程 B：線上即時互動（使用者每次操作）
  使用者在 sidebar 調參數（dataset / kernel / C / gamma / degree / noise / n_samples）
    → sklearn 產生資料 + 70/30 切分訓練/測試集
    → SVC 即時訓練（st.cache 加速）
    → Plotly 即時繪製：決策邊界、support vectors、margin、3D 曲面
    → 顯示訓練準確率 vs 測試準確率 + overfitting 提示

流程 C：部署管線 Deployment
  GitHub repo → Streamlit Community Cloud → 設定 app.py → 自動安裝 requirements → 上線

【五個教學頁面 Pages】
1. SVM 是什麼？
   - 直覺介紹、二元分類、為什麼要最大 margin、hyperplane/margin/support vector 名詞
   - 播放動畫：svm_margin_intro.mp4
2. Margin 與 Support Vectors
   - 決策函數 f(x)=w·x+b、margin=2/‖w‖、最佳化問題 min ½‖w‖²
   - 互動：拉 C 即時看 margin 寬度變化
   - 播放動畫：support_vectors_intro.mp4
3. Interactive SVM（核心互動頁）⭐
   - 即時調參數，2D 決策邊界 + 3D 決策曲面（分頁切換）
   - 顯示 support vectors、訓練 vs 測試準確率、overfitting/underfitting 提示
   - 訓練點(●)/測試點(◆)疊圖、參數解讀、可下載 PNG
4. Kernel Trick
   - 為什麼 linear 處理不了 circles/moons、RBF 如何升維分開
   - 2D 邊界對比 + 3D 決策曲面對比（linear/rbf/poly 並排）
   - 播放 3D 動畫：kernel_trick_intro.mp4（資料升維到高維被平面切開）
5. Quiz
   - 5 題選擇題複習 + 即時對答案/解析 + 分數統計

【三支 Manim 概念動畫】
- svm_margin_intro：眾多分隔線中選出最大 margin
- support_vectors_intro：只有最近的點決定邊界
- kernel_trick_intro：2D 同心圓 → 升維到 3D → 平面切開（3D 旋轉展示）

【專案結構 Structure】
app.py（首頁）
pages/（5 頁教學）
utils/（datasets / svm_model / plotting / explanations / media）
manim_scenes/（3 支動畫原始碼）
assets/videos/（預渲染 mp4）
requirements.txt / README.md / .streamlit/config.toml

【教學亮點 Highlights】
- 每個互動參數都有繁體中文解釋
- 用真實 sklearn 模型畫真實邊界（非示意圖）
- 訓練 vs 測試準確率讓 overfitting「看得見」
- 2D + 3D 雙視角理解決策函數
- 影片不存在時顯示提示、不會 crash
