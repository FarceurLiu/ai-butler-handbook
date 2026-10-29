# 從零開始養成我的 AI 管家

免費公開版 v1.1 教學書，提供繁體中文、英文、線上閱讀及 PDF，使用 GitHub Pages 發布。

- [繁體中文首頁](https://farceurliu.github.io/ai-butler-handbook/)
- [English edition](https://farceurliu.github.io/ai-butler-handbook/english.html)
- 作者 [Farceur Liu](https://www.linkedin.com/in/farceur-liu-636864b5/)
- 聯繫：<farceur2021@gmail.com>

## 內容與建置

本版的唯一內容來源為 `handbook.md`、`handbook-en.md`。圖解與封面在 `assets/`。

```bash
python3 scripts/build_site.py
python3 scripts/test_site.py
```

建置僅需 Python 3.10+ 標準函式庫，產生 `index.html`、`english.html`、`read.html`、`read-en.html`。既有 `linkedin.html` 使用同版英文首頁，保留分享網址。沒有外部字型、追蹤腳本或背景 API 請求。

一般建置保留已驗證的 PDF，不會重新排版。內容或列印樣式有變時，另以已安裝的 Chrome／Chromium 重建，再檢查文字、連結、頁碼與實際畫面：

```bash
python3 scripts/build_site.py --pdf
```

PDF 下載檔為 `downloads/ai-butler-handbook_v1.1_zh.pdf`、`downloads/ai-butler-handbook_v1.1_en.pdf`。舊版 v1.0 下載保留歷史相容性，不作為目前入口。

## 發布與回退

GitHub Pages 來源為 `main` 分支根目錄；推送後須核對 Pages 成功終態、部署 commit 及實際公開檔案。只加入明確的公開檔案，不使用未經檢查的整目錄上傳。工作稿、截圖、驗收紀錄及個人路徑不屬於發布內容。

要回退時，對應發布 commit 建立 revert commit，再確認 Pages 與實際公開內容；不改寫既有歷史。舊版建置程式可從 Git 歷史取回，現行產生入口僅為 `scripts/build_site.py`。

## 使用與引用

使用、分享與引用方式以書內「公開版聲明」為準。軟體與服務可能更新；代理檢查不等於真人初學者跟做或市場成效驗證。
