# DESCENTE 27FW 正式訂貨（27Q3Q4 Convention）經銷線上訂貨

APP 衣 316 款／ACC 配件 86 款／FTW 鞋 54 款，共 456 款、1,114 個款色。資料來源：原廠 27Q3Q4 Convention Monthly Map（APP、ACC）、H2-27 Specialised Digital Catalogue（FTW）、Convention Sheet（系列故事）。

- `index.html`：下單頁（商品資料在 `data.js`，縮圖在 `imgs.js`，大圖在 `big/`）
- `config.js`：收單網址設定（`SUBMIT_URL`）。留空時為「傳單模式」，經銷商下載 Excel 後用 LINE / Email 傳給業務。
- `apps-script/Code.gs`：貼到 Google 試算表的 Apps Script，部署成網頁應用程式後即可收單。

## 價格
台灣定價待定。網頁不顯示任何價格或韓幣，卡片顯示「台灣定價待定」。`data.js` 的 `price`（＝`krw`）是韓國 MSRP（韓幣，取自 Monthly Map 總覽頁），只出現在下載的 Excel／CSV「韓幣 MSRP(₩)」「韓幣金額(₩)」欄。
台灣定價出來後：把每筆 `price` 換成台幣，卡片 `.price` 改回顯示價格、打開金額格，Excel／CSV 欄名改回「台灣建議售價／零售金額」，`dataNotes()` 拿掉第一條；`apps-script/Code.gs` 的「參考金額 ₩」也要改。

## 資料待更新說明
頁首條列與 Excel 總表 G 欄共用 `dataNotes()`：台灣定價、尺寸（參考 DESCENTE 尺寸對照表）、各色開放尺寸、實體圖、多色合圖、到貨月份、暫定品名、材質、色號待確認。資料補齊後從 `dataNotes()` 拿掉對應條目。

## 篩選與圖片
- 上方三排：性別 → 大類（上身／下身／配件／鞋類）→ 系列分頁，交集；不顯示 ETA／月份（`mon` 只留在 data.js 內部）。
- `pc.js`：多色款式圖裁成單色的比例框（897／926），卡片「款式圖」顯示單色；「實體圖」只在有配色照時可按（目前 141 款色鞋款）。產生工具在 emers-whl-system `tools/dstc_percolor/`。
- 詳細交接見 `ORDER_SYSTEMS_HANDOFF.md` 第 9 節。

## 過往參考
商品卡「過往參考」與「過往熱賣優先」排序用 `ref.js`，由 `tools/build_ref.py --whl ../emers-whl-system` 產生（直營＋雷根＋動力 POS，區域合計）。人工改對照：`tools/ref_override.json` 填 `{"27FW款號": ["舊款號"]}`，空陣列＝無對照。

## 其他
- 與 Early Buy（`dst-27fw-order`）重複的 21 款保留，卡片標「Early Buy 已開訂」。
- 原廠未附各色開放尺寸：衣服依性別全段開放、配件 F、鞋 220–300（女款限定色 220–260）。
- 訂單編號前綴 `DSTC27-`，localStorage 前綴 `dstc-`。
