# 從零開始養成我的 AI 管家

免費公開版教學書網站，使用 GitHub Pages 發布。

作者 LinkedIn：<https://www.linkedin.com/in/farceur-liu-636864b5/>
聯繫 Email：<farceur2021@gmail.com>

## 重新產生網站

```bash
python3 scripts/build_site.py
```

英文 PDF 需要另外產生：

```bash
python3 -m pip install -r requirements.txt
python3 scripts/build_english_pdf.py
```

產生內容：

- `index.html`：公開分享首頁
- `read.html`：線上閱讀版
- `read-en.html`：英文線上閱讀版
- `english.html`：English overview page for international readers
- `downloads/`：中文 / 英文 Markdown 來源檔與 PDF 下載檔
- `assets/`：網站樣式與封面預覽

## 內容來源

公開站內容以本 repo 內檔案為準。網站導覽只提供線上閱讀與 PDF；Markdown 保留為 repo 來源檔，不作為一般讀者的主要入口。

- `downloads/從零開始養成我的AI管家_公開版.md`
- `downloads/從零開始養成我的AI管家_免費公開版_v1.0.pdf`
- `downloads/ai-work-assistant-handbook_public-edition_v1.0_en.md`
- `downloads/ai-work-assistant-handbook_public-edition_v1.0_en.pdf`

## 流量與下載追蹤

網站使用 GoatCounter 做隱私友善追蹤，追蹤首頁、閱讀頁、英文頁瀏覽，以及 PDF 下載、線上閱讀、LinkedIn、Email 等點擊事件。

目前追蹤端點寫在 `scripts/build_site.py`：

- `https://farceur-ai-butler.goatcounter.com/count`

正式收數前需先建立對應 GoatCounter site；不需要在 repo 放任何 API key 或 token。

Threads 分享可用 UTM 連結：

```text
https://farceurliu.github.io/ai-butler-handbook/?utm_source=threads&utm_medium=social&utm_campaign=ai_butler_handbook_launch
```
