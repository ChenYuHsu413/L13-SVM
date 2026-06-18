# 使用者指令完整紀錄 (User Prompts Archive)

> 本檔案收錄使用者在「SVM 互動式教學網站」專案中下過的所有指令，依時間順序、盡量逐字保留。
> 對應的執行內容與技術決策請見 [log.md](log.md)。

---

## 1. 初始需求（完整建站規格）

```
你是一位資深 Python、Machine Learning、Manim、Streamlit 教學網站開發者。

我想建立一個「SVM Support Vector Machine 互動式教學網站」，用來教學 SVM 的核心概念、
數學直覺、Support Vectors、Margin、Kernel Trick，並且使用 sklearn 的 SVM 實際訓練資料，
畫出真實 decision boundary。

請你幫我從零建立完整專案，並且讓它可以部署到 Streamlit Community Cloud / streamlit.io。

請注意：
不要讓 Streamlit 在雲端即時執行 Manim render。
Manim 只負責製作概念動畫，先在本機渲染成 mp4 影片。
Streamlit 網站只負責播放這些預先輸出的影片，並使用 sklearn + Plotly 或 Matplotlib
進行互動式 SVM 視覺化。

（內容涵蓋：專案目標、技術限制與設計原則、完整專案結構、五個教學頁面內容、
三個 Manim scene 需求、utils 模組需求、requirements.txt 與 README 部署需求、
品質要求、加分項目，最後要求先完成 MVP 版本：
  1. Streamlit 多頁面網站可以跑
  2. sklearn SVM 互動 decision boundary 可以正常顯示
  3. Manim scene 檔案先建立好
  4. 影片不存在時用提示文字取代
  5. 確認可以部署後，再美化 UI）

Please follow CLAUDE.md
```

> 完整原始規格亦可參考 README 上方的「初始 Prompt 發想」ChatGPT 分享連結。

---

## 2.
```
可以先幫我在本地跑起來看看嗎
```

## 3.
```
請幫我渲染產生三個影片
```

## 4.
```
Kernal那個影片的呈現 我希望是3D的 可以做得到嗎
```

## 5.
```
我可以加入一個 3D decision function surface嗎
```

## 6.
```
https://github.com/ChenYuHsu413/L13-SVM.git 幫我推送到這裡
```

## 7.
```
請幫我在readme最上面加入demo 連結 https://l13-svm-interactivatepage.streamlit.app/
```

## 8.
```
好了 再來回到你剛才說的 還有哪些部分可以優化? 你說在kernel加入2D 3D對比圖?
對了 接下來改動先不要推送 我先在本地端檢查效果
```

## 9.（問題回報）
```
page 3 show ImportError: cannot import name 'train_svm_with_split' from 'utils.svm_model'
(D:\AI Class ChenYu\AIClass\L12-SVM\utils\svm_model.py)
File "...\pages\3_Interactive_SVM.py", line 8, in <module>
    from utils.svm_model import train_svm_with_split
```

## 10.
```
沒問題 幫我把本機端server關掉後推送上去
```

## 11.
```
可以幫我總結這份專案做了什麼 生成workflow 我要丟去給chatgpt生成資訊圖表
```

## 12.
```
可以幫我存成workflow.md嗎
```

## 13.
```
can you add workflow.png into my readme? you can put it below demo link
```

## 14.
```
can you summarize everything and write to log.md, including all discussion and Q&A
```

## 15.
```
推送上去
```

## 16.
```
幫我在readme上面加入一個初始prompt生成連結 https://chatgpt.com/share/6a336023-01f8-83ee-ad46-e36ccf3aff4b
```

## 17.
```
我想要在改版一下 manim應該要能給使用者互動, 使用者可以改變參數以後即時顯示動畫 這樣可行嗎
```

## 18.
```
比較常見的升維切3D 好像是用rbf?
```

## 19.
```
好
```

## 20.
```
幫我推送上去
```

## 21.
```
好 幫我更新log
```

## 22.（問題回報）
```
ImportError: cannot import name 'plot_kernel_lift_animation' from
'utils.plotting' (/mount/src/l13-svm/utils/plotting.py)
```

## 23.
```
有了 已經可以跑起來了
```

## 24.
```
你幫我把我剛才新增的pdf也推送上去 加在readme的初始prompt發想下面,作為chatgpt對話紀錄的存檔
```

## 25.
```
更新一下log,另外我想要一份是我下過的指令完整版 放到prompt裡面吧
```
