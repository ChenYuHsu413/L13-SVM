# 專案開發日誌 (Development Log)

> SVM 互動式教學網站 — 從零建立到部署的完整開發紀錄，含所有討論、Q&A、技術決策與問題排除。

- **專案**：SVM Support Vector Machine 互動式教學網站
- **GitHub**：<https://github.com/ChenYuHsu413/L13-SVM>
- **線上 Demo**：<https://l13-svm-interactivatepage.streamlit.app/>
- **本機路徑**：`D:\AI Class ChenYu\AIClass\L12-SVM`

---

## 開發環境重點

| 項目 | 狀況 |
| --- | --- |
| 主環境 Python | **3.14.3**（太新，Manim 相依套件無預編譯 wheel） |
| Manim 渲染環境 | 用 `uv` 另裝 **Python 3.12.13**（獨立 venv `.venv-manim/`） |
| ffmpeg | 用 pip 的 `imageio-ffmpeg` 取得，複製成 `tools_ffmpeg/ffmpeg.exe` |
| Git 認證 | Git Credential Manager 2.7.0（首次推送跳瀏覽器登入） |
| OS | Windows 11，PowerShell + Git Bash |

---

## 完整 Q&A 與工作紀錄（依時間順序）

### 1️⃣ 初始需求：從零建立完整教學網站（MVP 優先）

**使用者要求**：建立 SVM 互動教學網站，教 SVM 核心概念、數學直覺、Support Vectors、Margin、Kernel Trick；用 sklearn 訓練真實模型畫 decision boundary；可部署到 Streamlit Community Cloud。
關鍵限制：Streamlit 雲端不即時跑 Manim，Manim 只在本機渲染 mp4，網站只播放預渲染影片。先做 MVP。

**完成內容**：
- 建立完整專案結構：`app.py` + 5 個 pages + `utils/` 4 模組 + 3 個 Manim scenes + `requirements.txt` / `README.md` / `.gitignore`
- `utils/datasets.py`：`generate_dataset()` 產生 4 種資料集（linear/blobs/moons/circles）
- `utils/svm_model.py`：`train_svm()` 訓練 SVC，回傳 (model, accuracy)
- `utils/plotting.py`：`plot_decision_boundary()` 用 Plotly 畫決策區域/邊界/margin/support vectors
- `utils/explanations.py`：繁中教學文字 + kernel/參數對照表
- `utils/media.py`：`play_video()` 安全播放影片，找不到 mp4 時顯示提示不 crash
- 5 個頁面：SVM Concept / Margin & Support Vectors / Interactive SVM / Kernel Trick / Quiz
- 加分項：參數對照表、overfitting/underfitting 提示、參數解讀、SV 佔比、Quiz 分數、每頁「下一步建議」
- **驗證**：所有檔案編譯通過；dataset × kernel 全組合 pipeline 測試通過

**技術決策**：requirements.txt 刻意不含 manim（部署輕量）；Manim scenes 只用 `Text`（不用 `MathTex`），避免需要安裝 LaTeX。

---

### 2️⃣ 「可以先幫我在本地跑起來看看嗎」

**完成**：用背景方式啟動 `streamlit run app.py --server.port 8501`，確認 `/_stcore/health` 回 **200**、主頁 200。提供 <http://localhost:8501> 給使用者瀏覽。此時影片尚未渲染，影片區塊顯示提示文字（預期行為）。

---

### 3️⃣ 「請幫我渲染產生三個影片」

**問題**：主環境只有 Python 3.14，`pip install manim` 失敗——`moderngl`/`glcontext` 需要 MSVC C++ Build Tools 編譯（無 3.14 wheel），且 ffmpeg 未安裝。環境也沒有 conda/winget/uv。

**解法（全程命令列、不需互動式安裝）**：
1. `pip install uv` → `uv python install 3.12`（取得 Python 3.12.13）
2. `uv venv --python 3.12 .venv-manim` → `uv pip install manim imageio-ffmpeg`（Manim 0.20.1，3.12 有 wheel）
3. 取 `imageio_ffmpeg.get_ffmpeg_exe()` 路徑，複製成 `tools_ffmpeg/ffmpeg.exe` 並加到 PATH
4. 用 3.12 venv 渲染 3 個 scene（`manim -qh`），輸出複製到 `assets/videos/`

**產出**：svm_margin_intro.mp4 (14.1s)、support_vectors_intro.mp4 (11.0s)、kernel_trick_intro.mp4 (15.4s)，皆 1080p60。
主環境 Python 3.14 完全沒被動到；`.venv-manim/` 與 `tools_ffmpeg/` 加入 `.gitignore`。

---

### 4️⃣ 「Kernel 那個影片的呈現 我希望是 3D 的」

**完成**：把 `kernel_trick_scene.py` 從 2D 改寫為 **`ThreeDScene`**（class 與檔名不變，Streamlit 不用改）：
- 俯視角顯示 2D 同心圓 → 示範直線分不開
- 鏡頭傾斜成 3D，同時把每點依 **z = x² + y²** 升維（外圈抬高、內圈留低）
- 綠色水平平面滑入切開兩群 → 鏡頭環繞旋轉 → 結尾字卡
- 字幕用 `add_fixed_in_frame_mobjects` 固定在畫面前方，旋轉不歪
- 重新渲染並覆蓋 `kernel_trick_intro.mp4`（22.1s，1.5M）

---

### 5️⃣ 「我可以加入一個 3D decision function surface 嗎」

**釐清**：詢問加在哪裡（Streamlit 互動頁 / Kernel 頁 / Manim 影片）→ 使用者選 **Streamlit 互動頁**。

**完成**：
- `utils/plotting.py` 新增 `plot_decision_surface_3d()`：曲面高度 = `decision_function` f(x)，灰色 z=0 平面為決策邊界，資料點放在各自 f(x) 值上，support vectors 黑點約落在 ±1
- Page 3 改用分頁：**🗺️ 2D 邊界 / ⛰️ 3D 決策曲面**，兩者隨參數即時更新
- 效能：3D 用較粗格點（80×80）保持流暢
- **驗證**：3 種 kernel × 多資料集，每圖 5 traces，全部正常

---

### 6️⃣ 「幫我推送到 https://github.com/ChenYuHsu413/L13-SVM.git」

**過程**：
- 環境無 gh CLI、無 git 身分、無 credential helper，但有 Git Credential Manager 2.7.0
- `git init` → 設定 local 身分（name `ChenYuHsu413` / email `jolene19930413@gmail.com`）→ 設 `credential.helper manager`
- 排除 `streamlit_run.log`（執行日誌，加入 .gitignore 並 force unstage）
- **問題**：第一次 push 失敗 `src refspec main does not match any`——因為先前的 `git branch -M main` 在鏈式指令中途失敗未執行，commit 落在預設的 `master` 分支
- **修正**：`git branch -M master→main`，重新 push（GCM 跳瀏覽器登入完成認證）
- **結果**：commit `0078849` 推上空 repo，含 3 支影片

---

### 7️⃣ 「請幫我在 readme 最上面加入 demo 連結」

**完成**：README 標題下方加入 Demo 文字連結 + 「Open in Streamlit」徽章，連到 <https://l13-svm-interactivatepage.streamlit.app/>。commit `80fedb5` 推送（沿用憑證，未再跳瀏覽器）。

---

### 8️⃣ 「回到優化討論——還有哪些可以優化？」

**提出 4 個方向**，使用者**全選**：

1. **Kernel 頁 2D/3D 對比圖**：Page 4 互動比較改成「2D 邊界對比 / 3D 決策曲面對比」兩分頁，linear/rbf/poly 並排
2. **加入 test accuracy（CP 值最高）**：`utils/svm_model.py` 新增 `train_svm_with_split()`（70/30 切分）；Page 3 顯示訓練 vs 測試準確率、用真實 train/test 落差判斷 overfitting；2D 圖加測試點(◆)疊圖；`plot_decision_boundary` 支援選用測試點參數
3. **UI 美化**：新增 `.streamlit/config.toml` 統一主題色（藍 primary、淺藍灰側欄）
4. **Page 2 互動 margin 示範**：拉 C 即時顯示 margin 寬度 = 2/‖w‖ 與 SV 數量

**驗證**：所有頁面編譯通過；新邏輯跨資料集正常；overfitting 情境實測（rbf gamma=10, C=100）train/test gap 從 +0.04 拉大到 +0.10，警告正常觸發。**此階段依使用者要求只在本地、不推送。**

---

### 9️⃣ 問題排除：`ImportError: cannot import name 'train_svm_with_split'`

**原因**：不是程式碼問題（函式確實在檔案、測試也 import 成功）。是**執行中的 Streamlit 伺服器模組快取**——伺服器在新增函式之前就啟動，舊版 `utils.svm_model` 被快取在 `sys.modules`，Rerun 只重跑頁面腳本、不重載子模組。

**解法**：停掉舊背景伺服器、清 `__pycache__`、重啟全新 `streamlit run`。
**教訓**：改 `utils/` 裡被 import 的模組後，最保險是整個重啟 streamlit（頁面檔熱重載可靠，被 import 的子模組有時不會）。

---

### 🔟 「關掉 server 後推送上去」

**完成**：用 PowerShell `Stop-Process` 關閉 Streamlit（health 回 000）；`git add -A`（確認無 secrets/venv/log）；commit `cb45ca7`（6 檔案：4 優化）推送成功。

---

### 1️⃣1️⃣ 「總結專案生成 workflow 丟給 ChatGPT 生成資訊圖表」→ 存成 `workflow.md`

**完成**：產出結構化專案摘要（定位、技術棧、三條工作流程：離線渲染/線上互動/部署、五頁面、設計原則、亮點），格式含流程箭頭、可直接複製給 ChatGPT。存成 `workflow.md`。

---

### 1️⃣2️⃣ 「把 workflow.png 加進 readme，放在 demo 連結下方」

**完成**：使用者用 ChatGPT 生成 `workflow.png`（1.88 MB，放在 repo 根目錄）。README 在徽章下方加入 `![專案架構與工作流程](workflow.png)`（相對路徑，GitHub 與本機皆可顯示）。commit `a6bf896` 推送。

---

### 1️⃣3️⃣ 「總結所有討論與 Q&A 寫進 log.md」

**完成**：即本檔案。

---

### 1️⃣4️⃣ 「README 最上面加入初始 Prompt 生成連結」

**完成**：README 標題下方、demo 連結之後，加入「💡 初始 Prompt 發想」連結（ChatGPT share 連結）。commit `829ec80` 推送。

---

### 1️⃣5️⃣ 「Manim 應該要能互動，使用者改參數後即時顯示動畫，可行嗎？」

**技術評估（重點討論）**：誠實回覆 **用 Manim 做即時互動不可行**，但目標可達成——換工具用 Plotly。
- Manim 是離線逐格渲染成影片，單支要數秒~數十秒，稱不上即時
- Manim 在雲端裝不起來（系統需 cairo/pango/ffmpeg，Streamlit Cloud 1GB 記憶體邊渲染邊服務會超時）
- **Plotly** 原生支援 animation frames + 播放按鈕，在瀏覽器端執行 → 真・即時、部署零負擔
- **建議**：保留 Manim 影片當電影級開場，另加 Plotly 互動動畫讓使用者玩參數（互補，非取代）

**使用者選擇**：先做「Kernel 升維互動動畫」。

**完成**：
- `utils/plotting.py` 新增 `plot_kernel_lift_animation()`：Plotly 3D 動畫，把同心圓從 z=0 平滑升維、綠色平面切入，含 ▶ 播放/⏸ 暫停按鈕 + 升維進度滑桿
- Page 4 在 Manim 影片下方新增「🕹️ 互動升維動畫」區，含 noise / 升維強度 滑桿，改參數即時重建
- **驗證**：24 frames，slider/buttons 正常

---

### 1️⃣6️⃣ 「比較常見的升維切 3D 好像是用 RBF？」

**技術釐清**：使用者直覺有理但需澄清——原本的 `z = x²+y²` 其實對應 **多項式（poly degree-2）特徵**，不是 RBF。
- **多項式**：`z = x²+y²`（半徑平方），有限維、可精確畫；內圈低、外圈高
- **RBF**：`z = exp(-γ·r²)`（到中心的高斯相似度），內圈隆起成山頂、外圈在山腳（**上下相反**）
- 重要觀念：RBF 真正特徵空間是**無限維**、畫不出來，3D 圖是「以中心為 landmark」的簡化示意

**完成**：`plot_kernel_lift_animation()` 加 `mode`（poly/rbf）與 `gamma` 參數；Page 4 加「升維方式」切換鈕 + gamma 滑桿（poly 模式時 disable），兩模式各有對應中文解說。**驗證**：兩模式 z 值上下相反（poly 1.4~2.5 vs rbf 0.29~0.69）。commit `191c2f1` 推送。

---

### 1️⃣7️⃣ 「幫我更新 log」

**完成**：把第 14~16 段（prompt 連結、Manim 互動討論、poly/RBF 切換）補進 log.md，更新 Git 歷史表與踩雷總結。commit `76fb6f2` 推送。

---

### 1️⃣8️⃣ 雲端問題排除：`ImportError: cannot import name 'plot_kernel_lift_animation'`（/mount/src/...）

**原因**：錯誤路徑 `/mount/src/l13-svm/...` 是 **Streamlit Community Cloud**，不是本機。確認遠端 `origin/main` 的 plotting.py 確實有該函式（第 264 行）→ 程式碼沒問題。與本機那次相同的**模組快取**：雲端伺服器在函式加入前就啟動，舊版 `utils.plotting` 卡在 `sys.modules`。

**解法**：使用者在 Streamlit Cloud **Manage app → Reboot**（強制重新 git pull + 開乾淨進程）。Reboot 後恢復正常。
**教訓**：改 `utils/` 被 import 的模組後 push，雲端需手動 Reboot（等同本機重啟 streamlit）；只改 `pages/` 通常自動熱重載即可。

---

### 1️⃣9️⃣ 「把新增的 PDF 推送上去，加在 README 初始 Prompt 下方」

**完成**：`SVM 教學網站部署.pdf`（ChatGPT 對話紀錄存檔）加入 repo；README 在「初始 Prompt 發想」下方加連結（檔名空格用 `%20` 編碼）。commit `4475664` 推送。

---

### 2️⃣0️⃣ 「更新 log + 建立一份我下過的指令完整版」

**完成**：更新本日誌；新增 `prompts.md` 收錄使用者在本專案下過的所有指令（依時間順序）。

---

## Git 提交歷史

| Commit | 說明 |
| --- | --- |
| `0078849` | Initial commit：完整教學網站 + 3 支影片 |
| `80fedb5` | docs：README 加入 demo 連結與徽章 |
| `cb45ca7` | feat：train/test 準確率、3D kernel 對比、margin 互動、主題色 |
| `a6bf896` | docs：README 加入 workflow 資訊圖表 |
| `e45e053` | docs：加入 log.md 開發日誌與 workflow.md |
| `829ec80` | docs：README 加入初始 Prompt 分享連結 |
| `191c2f1` | feat：互動 2D→3D 升維動畫（poly/RBF 切換） |
| `76fb6f2` | docs：log 更新（互動動畫改版） |
| `4475664` | docs：加入 ChatGPT 對話 PDF 存檔並連結至 README |

---

## 最終專案結構

```
L13-SVM/
├── app.py                      # 首頁 / Streamlit 入口
├── requirements.txt            # 部署套件（不含 manim）
├── README.md                   # 含 demo 連結 + workflow.png
├── workflow.md                 # 給 ChatGPT 生成資訊圖表的摘要
├── workflow.png                # 專案架構資訊圖表
├── log.md                      # 本開發日誌
├── .gitignore
├── .streamlit/
│   └── config.toml             # 主題色設定
├── assets/
│   ├── videos/                 # 3 支預渲染 mp4（含 3D kernel trick）
│   └── images/
├── manim_scenes/               # 3 支 Manim 動畫原始碼
│   ├── svm_margin_scene.py
│   ├── support_vectors_scene.py
│   └── kernel_trick_scene.py   # 3D ThreeDScene
├── utils/
│   ├── datasets.py             # generate_dataset()
│   ├── svm_model.py            # train_svm() / train_svm_with_split()
│   ├── plotting.py             # plot_decision_boundary() / _surface_3d() / _kernel_lift_animation()
│   ├── explanations.py         # 教學文字與對照表
│   └── media.py                # 安全播放影片
└── pages/
    ├── 1_SVM_Concept.py
    ├── 2_Margin_and_Support_Vectors.py   # + 互動 margin 示範
    ├── 3_Interactive_SVM.py              # 2D/3D 分頁 + train/test 準確率
    ├── 4_Kernel_Trick.py                 # 2D/3D 對比分頁
    └── 5_Quiz.py
```

> 本地專屬、未進 repo：`.venv-manim/`（Python 3.12 + Manim）、`tools_ffmpeg/`（ffmpeg）、`media/`（Manim 中間檔）、`__pycache__/`、`streamlit_run.log`。

---

## 關鍵指令參考

```bash
# 本機啟動網站
streamlit run app.py

# 渲染 Manim 影片（PowerShell，需先設好 ffmpeg PATH）
$env:PATH = "$PWD\tools_ffmpeg;$env:PATH"
.\.venv-manim\Scripts\python.exe -m manim -qh manim_scenes\kernel_trick_scene.py KernelTrickScene
# 再把 media\videos\...\*.mp4 複製到 assets\videos\ 對應檔名

# 部署：push 到 GitHub → streamlit.io → New app → main file = app.py → Deploy
```

---

## 重要技術決策與踩雷總結

1. **Python 3.14 裝不了 Manim** → 用 uv 另開 3.12 venv，主環境不動。
2. **ffmpeg 無安裝權限** → 用 `imageio-ffmpeg` 的 bundled binary，複製成 `ffmpeg.exe` 加 PATH。
3. **Manim scene 只用 `Text` 不用 `MathTex`** → 免裝 LaTeX。
4. **Streamlit 改 utils 後出現 ImportError** → 模組快取（`sys.modules` 卡舊版）。本機需重啟 `streamlit run`；**雲端需 Manage app → Reboot**（非改 code）。只改 `pages/` 通常自動熱重載即可。
5. **git branch -M main 要在 commit 後執行** → 否則 commit 落在 master 導致 push refspec 錯誤。
6. **test accuracy 讓 overfitting 看得見** → 只看 training accuracy 會被騙（永遠很高）。
7. **影片不存在不 crash** → `media.py` 找不到檔顯示提示，先跑網站後補影片皆可。
8. **要「即時互動動畫」別用 Manim** → Manim 是離線渲染、雲端裝不起來；用 Plotly animation frames（瀏覽器端、即時、零部署負擔）。Manim 保留做電影級開場影片。
9. **kernel 升維示意：poly 與 RBF 不同** → `z=x²+y²` 是多項式（poly）特徵（內低外高）；`z=exp(-γr²)` 是 RBF 高斯特徵（內高外低，上下相反）；RBF 真正空間為無限維，3D 圖只是 landmark 簡化示意。
