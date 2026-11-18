# DESCENTE 27FW 正式訂貨（27Q3Q4 Convention）經銷線上訂貨

APP 衣 316 款／ACC 配件 86 款／FTW 鞋 54 款，共 456 款、1,114 個款色。資料來源：原廠 27Q3Q4 Convention Monthly Map（APP、ACC）、H2-27 Specialised Digital Catalogue（FTW）、Convention Sheet（系列故事）。

- `index.html`：下單頁（商品資料在 `data.js`，縮圖在 `imgs.js`，大圖在 `big/`）
- `config.js`：收單網址設定（`SUBMIT_URL`）。留空時為「傳單模式」，經銷商下載 Excel 後用 LINE / Email 傳給業務。
- `apps-script/Code.gs`：貼到 Google 試算表的 Apps Script，部署成網頁應用程式後即可收單。

## 價格
目前 `data.js` 的 `price` 是**韓國參考售價（韓幣）**，畫面與 Excel 都標「韓國參考價 ₩」。價格取自 Monthly Map 總覽頁（明細頁有 73 款價格是占位數字，已以總覽頁為準）。
台幣定價出來後：把每筆 `price` 換成台幣，並把 `index.html`、`Code.gs` 裡的「韓國參考價／參考金額(₩)／₩／KRW」改回「台灣建議售價／零售金額／NT$／TWD」，再拿掉頁首的價格說明。

## 其他
- 與 Early Buy（`dst-27fw-order`）重複的 21 款保留，卡片標「Early Buy 已開訂」。
- 原廠未附各色開放尺寸：衣服依性別全段開放、配件 F、鞋 220–300（女款限定色 220–260）。
- 訂單編號前綴 `DSTC27-`，localStorage 前綴 `dstc-`。
