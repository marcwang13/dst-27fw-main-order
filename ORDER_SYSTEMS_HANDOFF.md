# 經銷線上訂貨系統：AI 交接文件

> **這份文件是唯一正本**，只維護在 `marcwang13/dst-27fw-main-order` 的 `ORDER_SYSTEMS_HANDOFF.md`。其他訂貨 repo（SDR、DST Early Buy、BY 27SS、BY 27FW，以及後來的 WAAC）裡的同名檔只指向這裡，不要再各寫一份完整副本。
> 給接手的 AI：這份文件描述艾盟仕（EMERS GROUP）批發事業處各套經銷線上訂貨系統的完整現況。讀完這份，再讀範本 repo 的程式碼，就能接手維護、修改或複製新品牌。
> 文件更新：2026-11-23 14:16（Asia/Taipei，Grok Bot；2XU H2-27 已上線並開通收單）。以 GitHub 本 repo 最新 commit 為準；文件和程式碼衝突時，相信程式碼，並回報差異。

## 0. 先知道這些

- 負責人：Marc Wang（王柏棛），批發事業處業務經理。公司帳號 `marc_wang@emers.com`（Google Workspace），GitHub 帳號 `marcwang13`。
- 溝通：繁體中文（台灣），直接講重點，文字不要有 AI 腔。
- 早期四套系統（SDR、DST Early Buy、BY 27SS、BY 27FW）**程式碼幾乎一樣**，只差商品資料、品牌色、名稱字串和 localStorage key。後來又加了 DSTC、鞋類站、WAAC 現貨站，規則仍以 SDR 範本為準，但各站有自己的例外（見第 9 節）。後端 `Code.gs` 早期四套之間約差 20 行（品牌色、Excel 檔名、寄件名稱，另有健康檢查文字、訂單頁標題、信件主旨與內文中的品牌名）；複製新品牌時以 `diff` 比對範本逐行改。
- 範本是 SUN DAY RED FW27（`sdr-fw27-order`）。新功能先在範本做，再同步到其他三套。
- 不要做的事：不輸入任何登入密碼、不幫人建帳號、不在網站或給客戶的檔案放供貨價或外幣價。需要授權、建 repo、驗證碼的步驟交給 Marc 本人。

## 0.5 多個 AI 輪流維護（同步規則，一定要照做）

Marc 同時用 Claude 和 Grok Bot 維護這些訂貨系統，一次只會有一邊在改。目的是其中一邊額度用完時，另一邊可以直接接手，而且換電腦也一樣。

1. **GitHub repo 是唯一正本。** 本機不留任何非 repo 的修改；開工前一定先 `git pull`（或重新 clone）拿 main 最新版。
2. **改完一定推回 main。** 不留沒合併的分支或只改在本機的東西。
3. **後端 `Code.gs` 一律先改 repo 裡的檔案**，commit 之後再貼到 Apps Script，部署用「管理部署作業 → 新版本」。不要只在 Apps Script 編輯器裡改，否則 repo 會落後。
4. **每次改動都在本文件第 11 節「變更紀錄」加一行**（日期、哪個 AI、哪套系統、改了什麼、commit），跟程式改動放在同一個 commit。
5. **本文件只在 `dst-27fw-main-order` 維護一份正本。** 其他訂貨 repo 的 `ORDER_SYSTEMS_HANDOFF.md` 只放指向本檔的一行連結。改交接內容只改這一份，不要再複製到其他 repo。
6. ADMIN_KEY 等密碼不准寫進 repo。

## 1. 系統清單

| 代號 | 品牌／季 | 狀態 | 客戶網址 | repo | 商品筆數（款色）／款數 | 訂單編號前綴 | 主題色 | localStorage 前綴 |
|---|---|---|---|---|---|---|---|---|
| SDR | SUN DAY RED FW27 | 上線收單中（範本） | https://marcwang13.github.io/sdr-fw27-order/ | marcwang13/sdr-fw27-order | 207／105 | `FW27-` | `#610e0e` 酒紅 | `sdr-` |
| DST | DESCENTE 27FW Early Buy | 上線收單中 | https://marcwang13.github.io/dst-27fw-order/ | marcwang13/dst-27fw-order | 69／23 | `DST27-` | `#0a3f94` 藍 | `dst-` |
| DSTC | DESCENTE 27FW 正式訂貨（27Q3Q4 Convention） | 建置中（台灣定價待定；網頁不顯示價格，Excel 附韓幣 MSRP） | https://marcwang13.github.io/dst-27fw-main-order/ | marcwang13/dst-27fw-main-order | 1,114／456 | `DSTC27-` | `#0a3f94` 藍 | `dstc-` |
| WAAC | WAAC FW26 現貨（現有庫存接單） | 上線收單中（2026-11-19） | https://marcwang13.github.io/waac-fw26-stock-order/ | marcwang13/waac-fw26-stock-order | 19／11（25 個尺寸 SKU，168 件） | `WAAC26S-` | `#141414` 黑＋`#c8102e` 紅 | `waac-` |
| 2XU | 2XU H2-27 正式訂貨 | 上線收單中（經銷商截止 2026/11/26） | https://marcwang13.github.io/2xu-h227-order/ | marcwang13/2xu-h227-order | 503／149 | `2XU27-` | `#111111` 黑 | `2xu-` |
| BYS | BLACK YAK 27SS | 未完成（已上線，未正式開放） | https://marcwang13.github.io/by-27ss-order/ | marcwang13/by-27ss-order | 747／349 | `BYS27-` | `#141414` 黑 | `bys-` |
| BYF | BLACK YAK 27FW | 未完成（已上線，未正式開放） | https://marcwang13.github.io/by-27fw-order/ | marcwang13/by-27fw-order | 680 款色（2026-11-13 變更紀錄；舊表寫的 150／148 已過時） | `BYF27-` | `#141414` 黑 | `byf-` |

另有 `marcwang13/dst-27fw-ftw-order`（DESCENTE 27FW 鞋類，https://marcwang13.github.io/dst-27fw-ftw-order/），各份交接副本都沒列這套，這裡不另寫完整說明；細節以該 repo 與 `emers-whl-system` 為準。

### 各系統後端

| 代號 | Apps Script 端點（`config.js` 的 SUBMIT_URL，以各 repo 預設分支現況為準） | 後台試算表（2026-11-12 系統信箱搬家後） |
|---|---|---|
| SDR | https://script.google.com/macros/s/AKfycbxk-oaR5vl4JiY3s6Q65j7OidmNFojFO2NtBIy1hBfQnKPvuJJLclmpbOVgCAoalknxQA/exec | https://docs.google.com/spreadsheets/d/1sRusT6TIYMA2F7CkcHCLHazegNcwWcUjl7jgulOy77U/edit |
| DST | https://script.google.com/macros/s/AKfycbzsqRbmJYu8EsA6bD4E7uGDt8gIIdAiMv0ifNaPvfeZN_iuPxt4hNYyo0M0y-_UGbK_ng/exec | https://docs.google.com/spreadsheets/d/1neJWTtmfiRUcqILg3QarvxFCghP6jJzXRaCju7HjTXA/edit |
| DSTC | https://script.google.com/macros/s/AKfycbxvudd7CBJzFcuxFbhq1_huI9BwEY3zXGxW-_ODDJrs2SSTNJmPVLJYULRk_uiDaqzy/exec | https://docs.google.com/spreadsheets/d/1Z3xtNZ-P6mepW-d0DIFg8O96bDfxRFOoU15BjaZko5w/edit |
| WAAC | https://script.google.com/macros/s/AKfycbyavOzjw-zJrwZqn7JqGYRQYhPsQEF0RHZw8-BAXLYeidJ1qlmDLY7JylstqYQTFQlrNw/exec | https://docs.google.com/spreadsheets/d/11aMcRd0iNLH0lq3qHW3M4-HlRcdExsFNsiOGSNpnx_w/edit （「WAAC FW26 現貨 線上訂單」） |
| 2XU | https://script.google.com/macros/s/AKfycbx_cDgnQo3qKWI2BrA_8bdBfPCBe_5ttDNonuz5EcfqEBy_mge-g4LhMa-p4cSR2tEu/exec | https://docs.google.com/spreadsheets/d/1uG5_S6ga0fLiHiL4U_5OB-zYVQyy_yQmaKRqTVMpJnc/edit （「2XU H2-27 正式訂貨 線上訂單」） |
| BYS | https://script.google.com/macros/s/AKfycbwP84Djd2jZP7VGq1Gxmd_YoraTY1p0nFPNNVWkcgXPNlISX7Dj7vn3EtISkIPQL61gaQ/exec | https://docs.google.com/spreadsheets/d/1Z2UpiXz4dZZvuXFO7AeLsQTjIH0eY_sEaOt-N6Kx-SE/edit |
| BYF | https://script.google.com/macros/s/AKfycbzcL9SX9r67Eot15i-06QlKfDT2yf-XXw57AbmKLodejvJ7tseMEUI-2lO5aLYu-t8ILQ/exec | https://docs.google.com/spreadsheets/d/1LpGzpLezmmh1uhZyYBkuGEyXTXDpwKvUxp2XYzygVEA/edit |

2026-11-12 起，後台試算表與 Apps Script 改在系統帳號 `emerswhlsystem.marc@gmail.com` 名下（舊表仍可能留在 `marc_wang@emers.com`，不要再用搬家前的表或舊部署網址）。明細見 `emers-whl-system` 的 `docs/SYSTEM_MAILBOX.md`。上面的 SUBMIT_URL 是 2026-11-19 從各 repo GitHub 預設分支 `config.js` 讀到的；試算表 ID 以系統帳號那份與 `tools/preorders_sync.py` 為準。Apps Script 專案列表：https://script.google.com/home/my

### 收單現況（2026-11-02 10:40 用 list API 讀後台；SDR 12／6,785／40,779,200 不變，DST 已增至 14 張）

| 代號 | 訂單數 | 件數 | 零售金額（台幣） | 備註 |
|---|---|---|---|---|
| SDR | 12 | 6,785 | 40,779,200 | 雷根兩店（高夢、西門）分兩張單 |
| DST | 14 | 25,002 | 70,320,100 | 雷根 16 分店一張連鎖單 19,219 件；動力主義 4 店分 4 張單 |
| BYS | 0 | 0 | 0 | 還沒開放 |
| BYF | 0 | 0 | 0 | 還沒開放 |

## 2. 架構

```
經銷商瀏覽器
  │ 開客戶網址（純靜態頁）
  ▼
[前台] GitHub Pages：marcwang13/<brand>-<season>-order
  │ index.html  單一檔案的前端（HTML+CSS+JS，無框架、無 build）
  │ data.js     商品資料 window.SDR_ITEMS（BY 另有 BY_RUNS、BY_CFG）
  │ imgs.js     縮圖 base64，window.SDR_IMG
  │ big/        大圖
  │ config.js   window.SDR_CONFIG = { SUBMIT_URL }
  │
  │ fetch POST，body 是 JSON 字串，Content-Type: text/plain;charset=utf-8（避開 CORS 預檢）
  │ fetch GET ?action=list&key=…（管理頁）
  ▼
[收單] Google Apps Script 網頁應用程式（綁在試算表上）
  │ 執行身分：我（marc_wang@emers.com）；存取：任何人
  │ LockService 排隊寫入
  ├─► [後台] Google 試算表「<品牌> <季> 線上訂單」
  └─► [通知] MailApp：驗證碼信、新單／修改（附 Excel 訂單本）、取消信
```

前台沒有資料庫。「我的訂單」和管理頁都即時讀試算表，所以直接改試算表＝系統同步改。

外部函式庫（前端用 CDN 動態載入）：ExcelJS（產 Excel 訂單本、交單檔）、SheetJS（匯入 Excel）。

## 3. repo 檔案

```
<repo>/
├── index.html          前端全部程式（約 14 萬字元；SDR 83 個函式，DST／BYS／BYF 85～86 個，BY 多 SZL、fullSizes、szConv 等）
├── data.js             商品資料
├── imgs.js             縮圖（base64）
├── big/                大圖（檔名對應商品 doll 欄位的 hash）
├── config.js           SUBMIT_URL
├── apps-script/Code.gs 後端（471 行）；改完要貼到 Apps Script 並重新部署
├── README.md
└── tools/              （只有 BY 兩套）gen.py 重產 data.js；parse.py 讀原廠匯出；fw_zh.py 中文品名；szconv.py 尺寸對照
                        實際：BYS＝brand.py、fw_zh.py、gen.py、gen2.py、parse.py、szconv.py；BYF＝fw_zh.py、gen.py、gen2.py、parse.py（沒有 szconv.py）
```

### data.js 商品欄位（一筆＝一個款色）

| 欄位 | 意思 |
|---|---|
| `id` | 唯一 key（SDR／DST 是「分頁-序號」，BY 是色碼 SKU） |
| `sheet` | 前台分頁（品類大分類） |
| `mon` | 月份／系列篩選值 |
| `theme`、`drop`、`monTag` | 主題、Drop、月份標記 |
| `cat` | 品類（交單分類 `divOf()` 也看這欄） |
| `gen` | 性別：男／女／中性 |
| `style` | 款號 |
| `zh`、`en` | 中文品名、英文品名 |
| `color`、`cc`、`sku` | 顏色、色號、色碼 SKU |
| `sizes` | 這個款色有開的尺寸 |
| `price` | 台灣建議售價（台幣），**網站上唯一可顯示的價格** |
| `fab`、`tech`、`ov`、`dt`、`series`、`note`、`icon` | 材質、機能、商品概述、細節、系列、備註、標章 |
| `launch`、`eta` | 上市月份、到貨日 |
| `doll` | 圖片 hash，對 `imgs.js` 與 `big/` |
| `part`、`run` | 上身 top／下身 bottom；尺寸段 key |
| `div` | （選填）強制指定交單分類 APP／ACC／FTW |
| BY 專用：`krw`、`whl`、`whlr`、`tw` | 韓國售價、內部選款標記、選款理由、台灣市場建議 |

### 各系統分頁（`sheet`）

- SDR：服裝-男 120、服裝-女 16、配件 38、球袋 6、鞋款 27
- DST：上衣 TOUGH 33、羽絨 23、GORE-TEX 13
- BYS：上身 352、下身 132、配件 246、鞋款 17
- BYF：上身 105、下身 39、套裝 6（**尺寸全是 `ASSORTED`，只填總數量，沒有尺寸段**）

### index.html 重要常數與函式

- 常數：`SHEETS`、`MONTH_ORDER`、`SIZE_COLS`（各分頁尺寸段）、`SHARE`／`SHARE_CAT`（前季尺寸銷售佔比）、`HKEY`（已送出紀錄 key）、`DRAFT_KEY`（草稿 key）、`AKEY`（登入 token key）、`OV_COL`／`GEN_COL`（圓餅圖色）、`FIXED`（Excel 訂單本固定欄）、`HO_BRAND`／`HO_FILE`／`HO_KEY`／`HO_DISC`（交單檔）。
- 下單：`renderList`、`itemHTML`、`matrixHTML`、`submit`、`xlsxForMail`、`post`。
- 連鎖分店：`brList`、`brDialog`、`openBranchMgr`、`branchTableHTML`、`branchesForExport`。
- 我的訂單：`startMine`、`renderMine`、`loadOrderToForm`。
- Excel：`buildBook`、`exportBook`、`importBook`、`loadExcelJS`、`loadSheetJS`。
- 管理：`startAdmin`、`renderAdmin`、`adminList`、`orderDetailHTML`、`adminSubmit`、`exitAdminEdit`、`reloadAdmin`。
- 下單分析：`analyzeLines`、`anAdminHTML`、`orderAnalysisHTML`、`anGroupOf`、`anSeries`。作廢不計；對不到商品標「找不到商品」。Excel 總表用公式，函式在 `buildBook`。
- 一鍵統整交單：`buildHandoff`、`exportHandoff`、`handoffCheck`、`divOf`、`hoUnits`、`hoSizes`。按鈕會先呼叫 `window.SDR_ADMIN.list()` 重新讀取最新訂單，`handoffCheck()` 檢查每張有效單（含各分店）明細件數＝訂單件數，不一致就提示稍後再按、不產出檔案。2026-11-02 先在 DST 做（57e31f4），已同步到 SDR、BYS、BYF。
- 右上角管理者登入：搜尋註解「右上角管理者登入」（約第 1246 行），按鈕 `#adm-btn`。

### 各系統字串差異（複製新品牌時要改的地方）

| 項目 | SDR | DST | BYS | BYF |
|---|---|---|---|---|
| `<title>` | SDR FW27 線上訂貨 | DESCENTE 27FW Early Buy 訂貨 | BLACK YAK 27SS 經銷訂貨 | BLACK YAK 27FW 經銷訂貨 |
| localStorage | sdr-auth、sdr-admin、sdr-dev、sdr-ho、sdr-fw27-sent-v1、sdr-fw27-draft-v1 | dst-auth、dst-admin、dst-dev、dst-ho、dst-27fw-sent-v1、dst-27fw-draft-v1 | bys-auth、bys-admin、bys-dev、bys-ho、bys-27ss-sent-v1、bys-27ss-draft-v1 | byf-auth、byf-admin、byf-dev、byf-ho、byf-27fw-sent-v1、byf-27fw-draft-v1 |
| HO_BRAND | SUN DAY RED FW27 | DESCENTE 27FW EARLY BUY | BLACK YAK 27SS | BLACK YAK 27FW |
| HO_FILE | SDR_FW27 | DESCENTE_27FW | BLACKYAK_27SS | BLACKYAK_27FW |
| Code.gs 寄件名稱（客戶） | SUN DAY RED 台灣 | DESCENTE 台灣 | BLACK YAK 台灣 | BLACK YAK 台灣 |
| Code.gs 寄件名稱（內部） | SDR FW27 線上訂貨 | DESCENTE 27FW 線上訂貨 | BLACK YAK 27SS 線上訂貨 | BLACK YAK 27FW 線上訂貨 |
| Code.gs 色碼 | #610e0e | #0a3f94 | #141414 | #141414 |

CSS 的 `--brand` 每套有兩個值（主色＋深色變體，例 SDR `#610e0e`／`#5a0d0e`），換色時兩個都要改。

注意：四套的 `config.js` 都用 `window.SDR_CONFIG`、商品都叫 `window.SDR_ITEMS`。同一頁要載入兩套以上就得改名。

## 4. 收單 API（四套共用）

全部打該系統的 `…/exec`。POST body 是 JSON 字串，header `Content-Type: text/plain;charset=utf-8`。

| 方法 | action | 參數 | 回傳 | 誰能用 |
|---|---|---|---|---|
| GET | （無） | — | 文字「… 收單程式運作中」，可當健康檢查 | 任何人 |
| GET | `list` | `key` | `{orders:[…]}` 含明細；錯誤 `{error:'forbidden'}` | 管理者 |
| POST | `otp_send` | `email` | `ok`／`wait`（60 秒內重送）／`invalid_email` | 任何人 |
| POST | `otp_verify` | `email`、`code` | `{email, token}` 或 `{error:'bad_code'/'expired'/'too_many'}` | 任何人 |
| POST | `mine` | `auth:{email,token}` | `{orders:[…]}`，只回這個帳號的單 | 已登入客戶 |
| POST | （無 action）＝送單 | `auth`、`oid`、`lines[]`、`store`、`contact`、`phone`、`email`、`note`、`branches`、`_xlsx`（base64）、`_xlsxName` | `ok`／`login_required`／`invalid` | 已登入客戶；同 oid 再送＝修改 |
| POST | `cancel` | `auth`、`oid` | 刪除結果 | 下單本人 |
| POST | `status` | `key`、`oid`、`status`（預設「已確認」） | `ok`／`forbidden` | 管理者 |
| POST | `admin_save` | `key`、`oid`、`lines[]`、`notifyCustomer` 等 | `ok`／`forbidden` | 管理者 |
| POST | `admin_delete` | `key`、`oid` | 刪除結果／`forbidden` | 管理者；內部呼叫 `cancel_(ss, oid, '', true)` 跳過帳號檢查 |

`lines[]` 每筆：`sheet`、`mon`、`style`、`sku`、`en`、`zh`、`color`、`size`、`qty`、`price`、`branch`（連鎖單才有）。

訂單編號：`<前綴><YYMMDD>-<HHmm><3 碼亂數>`，例 `FW27-261028-1544MTN`。

`key` 就是 Apps Script 指令碼屬性 `ADMIN_KEY`。四套統一用同一組，數值向 Marc 拿，**不要寫進前端程式、README 或給客戶的文件**（repo 是公開的）。

### Code.gs 函式

`adminOk_`、`doGet`、`json_`、`listOrders_`、`setStatus_`、`doPost`、`saveOrder_`、`sheet_`、`logSheet_`、`findOid_`、`removeOid_`、`sizeCmp_`、`tabName_`、`writeOrderTab_`、`rebuildOrderTabs`（手動執行：補建每店分頁）、`cancel_`、`orderHtml_`、`notify_`、`customerMail_`、`authSecret_`、`normEmail_`、`tokenFor_`、`authEmail_`、`otpSend_`、`otpVerify_`、`out_`。

常數：`NOTIFY_TO`、`ORDER_HEAD`、`LINE_HEAD`、`SIZE_ORDER`、`RESERVED_TABS`。

指令碼屬性：`ADMIN_KEY`（手動設，改了立即生效）、`AUTH_SECRET`（第一次用自動產生，改了所有客人要重新登入）。

## 5. 後台試算表

| 分頁 | 內容 |
|---|---|
| 訂單 | 一張單一列：送出時間、訂單編號、經銷商／店名、聯絡人、電話、Email、訂單備註、款色數、件數、零售金額、分店數、分店、狀態、帳號 Email、最後修改 |
| 明細 | 一個款色尺寸一列：送出時間、訂單編號、經銷商／店名、分店、分頁、月份、款號、色碼 SKU、英文品名、中文品名、顏色、尺寸、數量、台灣建議售價、零售金額 |
| <店名> | 每張單自動開一頁，款色一列、尺寸橫排 |
| _紀錄（隱藏） | 收過的訂單編號，不能刪 |

- 狀態：「已送出」→「已確認」只是內部標記，客人還能改。要鎖單就把狀態改「作廢」，之後客人再送也不會寫入。
- 「最後修改」：`業務 YYYY/MM/DD HH:mm`（管理頁改的）或 `客人 …`（客人自己改的）。

## 6. 登入、權限、通知

- **客戶登入**：Email 收 6 位數驗證碼，10 分鐘有效，錯 5 次作廢，60 秒內不能重寄。開放註冊。token 用 HMAC-SHA256（AUTH_SECRET）簽章，存在瀏覽器 `<前綴>-auth`。每套各自簽章，四套要各登一次。
- **權限**：每張單記「帳號 Email」，只有同帳號能改、刪；換裝置同 Email 登入就看得到。
- **管理者**：網站右上角「管理者登入」→ 輸入密碼 → 前端打 `GET ?action=list&key=` 驗證，對了存進 localStorage `<前綴>-admin` 並跳到「訂單彙整」；按鈕變「登出管理者」。舊的 `?admin=<key>` 網址也還能用（帶入後網址上的 key 自動清掉；`?admin=off` 登出）。
- **通知收件人（四套相同）**：`marc_wang@emers.com,zero_wang@emers.com,zoe_chang@emers.com,vince_tian@emers.com,david_wu@emers.com,benson_wang@emers.com,max_lee@emers.com,kai_weng@emers.com`，另外寄給客戶本人。
- **信件**：新單、修改（附完整 Excel 訂單本）、客人取消、業務刪除（內部「訂單取消（業務刪除）」、客人「訂單已由業務取消」）、業務調整（可選是否通知客人）。回信地址是 NOTIFY_TO 第一位。

## 7. 功能

**客戶前台**：品類分頁、月份／系列篩選、搜尋、只看已下單；商品卡（娃娃圖／CAD 款式圖／實體圖點擊放大、商品說明與材質、完整尺寸段，沒開的尺寸斜線灰格）；前季尺寸銷售佔比；連鎖分店模式（分店 × 尺寸矩陣，匯出總數版或連鎖版，連鎖版多「分店配貨」頁）；下單總覽圓餅圖（品類、性別，件數與金額）；下載／匯入傳統 Excel 訂單本；草稿自動存；我的訂單（修改、刪除按兩次、Excel、CSV）。只顯示台灣建議售價。

**管理頁（訂單彙整）**：所有訂單列表、圓餅圖、下單分析、看明細、編輯訂單、Excel／CSV、全部明細 CSV、標記已確認、刪除訂單（按兩次）、**一鍵統整交單**。

**下單分析**（訂單彙整裡，圓餅圖下面）：依大類、分頁、系列、經銷商各一張表。每張有款色數（款號＋顏色，一個色碼算 1）、尺寸數（款號＋顏色＋有填數量的尺寸）、件數、零售金額、件數佔比、金額佔比。可切「全部」或單一經銷商。展開「看明細」看該單的拆分；連鎖單各分店標題有該店的款色、尺寸、件數、金額，整張單同一款色只算 1。作廢不計入。對不到商品的明細，大類和系列標「找不到商品」。

大類依各系統目錄。SDR：服裝（男裝＋女裝）、配件（含球袋）、鞋款。DST 這季都是服裝，依品類分成上衣（T 恤、POLO）、外套（羽絨外套、輕量羽絨、GORE-TEX 外套）、背心（含羽絨背心）、長褲，跟三個分頁（上衣 TOUGH、羽絨、GORE-TEX）不同。系列：SDR 取商品資料「系列：」後面的名稱，沒標則用主題；DST 取系列欄的「產品線｜主題」（例如 PREMIUM TECH ESSENTIAL｜TOUGH、SNOW｜CANON；NEO｜NEO 只寫 NEO），訂貨窗口不另拆，沒有系列欄就用主題。

Excel 訂單本「總表」有同樣的分頁、大類、系列（款色數、尺寸數、訂購總數、零售金額），公式連到各分頁的隱藏欄（大類鍵、系列鍵、尺寸格數）。改黃色數量格，已列出的列會重算；本來沒下、這次才開始下的系列，要重新匯出才會出現。這份 xlsx 在瀏覽器產生，Apps Script 不用改。經銷商那張表只在管理頁，因為一份訂單本就是一家。

**一鍵統整交單**：下載 `<HO_FILE>_交單彙整_YYYYMMDD.xlsx`，給品牌方交單。
- 只算狀態不是「作廢」的單；一般單一店一區塊，連鎖單每分店一區塊（「店名 分店名」），同名合併。
- 折數統一 5 折（`HO_DISC=0.5`），「總表」B4 可改，三個分頁的 WHL 一起重算。
- 分頁順序：總表、APP(衣)、ACC(配)、FTW(鞋)。`divOf()` 依 sheet＋cat 分類：鞋／靴→FTW；衣／衫／褲／裙／外套／背心／T恤／POLO／套裝→APP；配件／球袋／帽／手套／襪／包／毛巾／皮帶／球Tee／球桿套／眼鏡／燈／登山杖→ACC；其餘 APP；商品有 `div` 欄位就照欄位。
- APP／ACC／FTW 版面：左邊資訊欄（STYLE NO.、STYLE & COLOR、COLOR、顏色、CATEGORY、IMAGE、STYLE NAME、中文品名、GENDER、月份、TW-SRP）→ WHSL TTL 區（粉紅，公式加總各店）→ 各店區塊（黃色店名）。每區上方有 SRP TTL、WHL TTL 兩列；最下 TOTAL 列；凍結在第 7 列；橫向一頁寬。
- 總表（BY 客戶）：每店 APP／ACC／FTW 件數與 SRP 金額、客戶 TTL、件數佔比、SRP 加總、金額佔比、×折數 WHL；整體加總；品類佔比。全部用公式連到各分頁。

## 8. 常見維護操作

| 要做的事 | 怎麼做 |
|---|---|
| 改前端（文案、功能、商品） | 改 repo 檔案 → push 到 main → GitHub Pages 約 1 分鐘生效。改完用瀏覽器實際打開確認。 |
| 改後端 | 改 repo 的 `apps-script/Code.gs` → 打開試算表 → 擴充功能 → Apps Script → 先比對線上程式碼和 repo 是否一致 → 整份貼上（編輯器可用 `monaco.editor.getModels()[0].setValue(code)`）→ Ctrl+S → **部署 → 管理部署 → 鉛筆 → 版本選「新版本」→ 部署**。這樣端點網址不變。不要用「新增部署作業」，那會產生新網址。 |
| 新增／改商品 | SDR、DST：直接改 `data.js`（缺圖時一併補 `imgs.js` 與 `big/`）。BY：改原廠匯出檔後跑 `tools/gen.py` 重產。 |
| 改通知名單 | 改四套 `Code.gs` 的 `NOTIFY_TO`，四套都重新部署。 |
| 改管理密碼 | Apps Script → 專案設定 → 指令碼屬性 `ADMIN_KEY`，立即生效，不用重新部署。四套要一起改。 |
| 鎖單／作廢 | 試算表「訂單」分頁的狀態改「作廢」。 |
| 補店名分頁 | Apps Script 編輯器選 `rebuildOrderTabs` 執行。 |
| 範本加新功能 | 先做在 SDR，驗證後同步到 DST、BYS、BYF（前端 push、後端重新部署）。 |
| 開新品牌 | 照第 10 節。 |

測試：可用 Playwright 開頁面，攔截 `script.google.com` 的請求回假資料，跑下單、管理頁、交單檔；交單檔用 LibreOffice 重算後核對總表與各分頁 TTL／SRP／WHL。真實流程測試要用 Marc 信箱收驗證碼，測完刪測試單。

## 9. 待辦與已知問題

### BLACK YAK 27SS／27FW（未完成）
- [x] 售價：2026-11-12 起改用公司定案的台灣建議售價（TW-SRP），不再用韓國 MSRP × 0.0245 換算。重產資料時不要把 `price` 洗掉。27FW 仍有部分中國專屬款色價格表沒填（變更紀錄後續有加回／拿掉，以現行程式為準）。
- [ ] 尺寸對照只是參考（上衣韓國尺碼→字母、褲腰 cm→英吋、鞋 mm→US），不是原廠尺寸表。
- [ ] 27FW 服裝尺寸曾在 2026-11-12 依 27SS 相近款補上實際尺寸（不是原廠尺寸表；重跑 `gen_fw2.py` 會洗回 `ASSORTED`，之後要再跑 `fw_sizes_from_ss.py`）。原廠正式尺寸段出來後要改回來。配件／鞋是否仍為 `ASSORTED`，待對現行程式。
- [ ] 後台沒有任何訂單，全流程測試（登入→下單→通知信→修改→刪除→管理者登入→一鍵統整交單）還沒跑過。
- [ ] 客戶版「快速上手」文件、經銷商通知信還沒做。
- 前季尺寸銷售佔比：剛代理沒有資料，已關閉。DST、BYS、BYF 的 `shareFor()` 要 `window.DST_SHARE_ON` 為真才顯示，目前沒設；`SHARE` 表是從 SDR 複製過來的殘留資料，之後有真資料再換掉並打開開關。只有 SDR 有開。

### DESCENTE 27FW 正式訂貨（DSTC，`dst-27fw-main-order`）現況與 2026-11-18 改動（Grok）

**網頁（`index.html`）**
- **原廠日期全拿掉**：data.js 已刪 eta／launch／etd 欄位；`mon` 欄位還在（已 +1 個月），只供內部用，網頁、CSV、Excel 都不顯示。卡片沒有 ETA 標籤、沒有月份篩選；清單改依大類（上身／下身／配件／鞋類）分組，「只看已下單」時標題是「分頁 · 大類」。也沒有交期。
- **價格**：網頁完全不顯示韓幣或任何金額，卡片價格位置固定顯示「台灣定價待定」；`#t-amt` 金額格隱藏。韓幣只出現在下載的 Excel／CSV（欄名「韓幣 MSRP(₩)」「韓幣金額(₩)」）。台灣定價確定後：把 data.js 每筆 `price` 換成台幣，卡片 `.price` 改回顯示價格、打開 `#t-amt`，Excel／CSV 欄名改回「台灣建議售價／零售金額」，並從 `dataNotes()` 拿掉第一條。
- **篩選列（上方三排膠囊，同樣式）**：第一排 性別（全部／男／女／中性）→ 第二排 大類（全部／上身／下身／配件／鞋類）→ 第三排 系列分頁。三者交集，下排數字依上排選擇計算；0 筆的膠囊變淡不能按；選了之後目前分頁沒東西會自動跳到第一個有的分頁（`fixSel()`）。桌機分頁列換行、手機橫滑並自動捲到選中的分頁。資料 `gen` 只有 男 246／女 246／中性 622（配件 153、鞋 156 都算中性；女配件 41）。大類由 `cgOf()` 算：div FTW＝鞋類、ACC＝配件、part bottom＝下身、其他＝上身。
- **資料待更新說明**：頁首一個條列區（`#dnote`，由 `dataNotes(true)` 產生，數字即時計算）：台灣定價待定、尺寸參考 DESCENTE 尺寸對照表待原廠更新（含各性別尺寸段）、各色開放尺寸原廠未附暫依性別全段開放、實體圖待更新、部分款式圖為多色合圖、到貨月份待確認、18 款色原廠暫定品名、157 款色材質待提供（多為鞋）、5 款色顏色／色號待確認。同一份清單（`dataNotes(false)`，第一條改寫成附韓幣 MSRP）放在 Excel 訂單本「總表」G 欄；各分頁 B2 提示見總表。每張卡片尺寸區上方小字「尺寸待更新（目前參考前季）」，沒有實體圖的再加「・實體圖待更新」。
- **單色款式圖**：`pc.js`（`window.DSTC_PC={品號色:[左,上,右,下] 比例]}`）告訴前端怎麼從多色款式圖 `big/<hash>.jpg` 裁出單一配色；`applyPC()` 用 canvas 在瀏覽器裁（卡片、放大、Excel 款式圖欄都用裁好的）。目前 897／926 個多色圖款色已單色（自動 418＋人工目視 479），剩 29 款色仍是多色合圖。產生工具與人工指派紀錄在 emers-whl-system `tools/dstc_percolor/`（README 有步驟；注意 review.py 會 import match2 而重寫 crops.json）。
- **按鈕**：卡片圖片下「款式圖」（單色裁切）＋「實體圖」。`it.photos` 只放實體圖：目前 141 款色（全是鞋，實際是原廠多色配色渲染圖，43 張共用）有，其他款色「實體圖」按鈕灰掉。原本「全部配色」按鈕已拿掉。Excel 第 4 欄改名「實體圖」。（2026-11-20 起另加韓國門市實拍 259 款色，見下方「實體圖」段）
- **其他**：WHL logo 在標題左邊；沒有管理入口（訂單彙整按鈕只有管理者看得到）；不放任何會員 Email。

**Excel／CSV**
- 訂單本各分頁欄位：KEY、No.、款式圖、實體圖、主題、Drop、品類、性別、款號、中文品名、英文品名、顏色、色號、色碼 SKU、Icon、布料、系列／尺寸、商品概述、商品細節、材質與科技、備註、韓幣 MSRP(₩)、各尺寸、訂購總數、韓幣金額(₩)（後面是隱藏的分析鍵）。沒有月份／ETA。
- 匯入是依表頭名稱讀，`SKIP` 正規式含 月份／ETA／MSRP／韓幣／₩，所以舊檔（有 ETA、月份、韓國參考價欄）照樣能匯入。2026-11-18 測過：下載→填數量→匯入→套用 OK。
- **還沒改的後端**：`apps-script/Code.gs` 的訂單明細表頭仍有「月份」、通知信合計寫「參考金額 ₩」。要改的話先改 repo 再貼 Apps Script、部署新版本（需要 Marc 授權），本輪沒動。

**內部網站串接**：emers-whl-system 內部站已把這套列進預訂單系統（key `dst-27fw-main`，頁面 `pre.dstc`），比照 ftw 做法。DSTC 後台試算表沒有開「知道連結的人可檢視」，內部站讀不到，所以筆數顯示「筆數待更新」；要 Marc 開共用或改用系統帳號讀取。

**部署方式**：這個 repo 用 GH_TOKEN_WHL `git push` 會 403，所以改檔後放在 box 的 `/workspace/upl2/`、`/workspace/upl3/dst-27fw-main-order/`，由 Marc（或 Grok 的瀏覽器）在 GitHub 網頁「Add file → Upload files」上傳。已上線：ac245f3（pc.js 418 款色）；之後本機 commit fa2d052（pc.js 897）、c01980d 與本輪（拿掉 ETA、三排篩選、實體圖、待更新說明、韓幣 MSRP 欄）待上傳。

**實體圖（2026-11-20，Grok Bot）**：Marc 給的 4 本韓國門市實拍相簿（拍照順序：標牌品號→正面→反面，共 650 張）已比對後上線。
- 結果：218 組中 189 組上線，**259 款色**有實體圖（單色正反面 144 款色、同框多色 115 款色；PREMIUM TECH ESSENTIAL 96、ACC 48、FTW MOVEWEAR 43、SNOW 36、FTW RUNNING 25、NEO-ARCHIVE 11），共 375 張圖。待確認 29 組沒上線（無標牌 4、標牌款號 SS323UTS75 不在系統 3、品項或顏色對不上 22），畫質待確認 4 張（a3/137、140、143、146 失焦或晃動）。逐筆紀錄在 `tools/realphoto/`（`match.csv`、`pending.csv`、`groups_decisions.txt`、`README.md`）。
- 檔案：圖在 `big/rp_<相簿a1–a4>_<序號>.jpg`（原圖 3472×4624 手機原檔 `=d` 下載，EXIF 轉正，Lanczos 縮到長邊 2000px，JPEG q90；11 張為了單檔 <1MB 用 q87–89）。對應表在 `rp.js`：`DSTC_RP`（圖檔鍵→[寬,高]）、`DSTC_RPI`（款色 id→[[圖檔鍵, 說明]]）。**data.js 沒動**。
- 前端：index.html 讀 rp.js 後合併進 `it.photos`／`it.phcap`。已有原廠配色照（141 款色鞋）的款色，單色實拍排最前、同框多色實拍排在原廠配色照後面（Excel 實體圖欄取第一張）。放大檢視（2026-11-20 Marc 第二次修改）：實體圖**填滿圖片區高度、視窗貼合照片**——圖框高度沿用娃娃圖（min(76vh,620px)），照片 `object-fit:contain` 整張不裁切、四周只留 8px 內距；`fitPhoto()` 用 rp.js 的原始寬高同步算出視窗寬度（依照片比例收窄，最窄 300px、最寬 min(94vw,960px)），寬度不夠時（手機）改縮視窗高度貼合，所以切換娃娃圖／實體圖只有寬度改變、不閃動。標題列在實體圖模式可換行，箭頭、切換鈕、借圖說明不被擠壓。直接用 2000px 原檔由瀏覽器縮小（高 DPI 仍清楚），不另產小檔。已拿掉「原尺寸」1:1 檢視。2026-11-20 測：桌機 1440 實拍 418×557（視窗 434×620）、借圖款 366×487；手機 390 寬 351×467。底列顯示「實體正面／實體反面／同框多色：…」說明。`hasImg()` 取代原本 `IMG[h]` 判斷，實體圖不進 imgs.js。
- Excel 訂單本：實體圖欄嵌入解析度維持長邊 400px、JPEG .85（款式圖 320px .78），但**顯示框跟同列款式圖一樣大**（照片縮在款式圖的顯示寬高內，2026-11-20 測 339 列全部沒有比款式圖大）。全部款色產檔約 13.8MB（寄信附檔上限 15MB）。
- **同款借圖（2026-11-20）**：沒有自己實拍的款色，借同款號有實拍的顏色的正反面（優先單色正反面，沒有才借同框多色；待確認 29 組與畫質待確認照片不借；不複製圖檔，`rp.js` 的 `DSTC_RPB`＝款色 id→[借用款色 id, 說明] 指向同一批 `big/rp_*.jpg`）。共 **143 款色**借圖（其中 27 款色只能借同框多色照；23 款色是已有原廠配色照的鞋，借圖排在配色照後面）。說明照 WHL `build_imgref.py` 寫法，例如「實際商品為 海軍藍(NAVY)，實體圖為同款 黑色(BLK0) 款式供參考，顏色不同」：放大檢視在圖下方淡黃說明列顯示（娃娃圖／實體圖兩種模式都顯示，圖框不跳）、每張圖說寫「同款實體正面／反面」；Excel 寫在「備註」欄（前綴【同款實體圖】）。卡片按鈕：自己的實拍寫「實體圖」，只有借圖的寫「同款實體圖」。合計有實拍可看的款色：自己的 259＋借同款 143＝402。
- 疑似 pc.js／款式圖錯置（待確認時一併看）：SS423SCPO1 款式圖是側背包、SS423SCPO2 是耳罩帽、SS423SGLOA 裁切出來是漁夫帽，但實拍分別是耳罩帽、漁夫帽、連指手套。

**過往參考（2026-11-19，Claude）**：`ref.js`（`window.DSTC_REF`）由 `tools/build_ref.py` 從 emers-whl-system 的 `dealer/data/chain_*`、`internal/data/direct_chain_*` 算出。區域：直營依主檔 region；動力新竹巨城、中和環球＝北部，其餘門市＝中部；雷根大甲＝中部、其餘＝南部（天王暫列南部，待 Marc 確認）。雷根、動力目前沒有 25FW 整季資料，中部、南部畫面不顯示資料期間提醒（Marc 11/19 要求拿掉），ref.js 也不放體系名稱與期間。每月 POS 匯入後重跑：`python3 tools/build_ref.py --whl ../emers-whl-system --xlsx 對照表.xlsx`，再更新 index.html 的 `ref.js?v=`。

### WAAC FW26 現貨（`waac-fw26-stock-order`）現況（2026-11-19，Grok）
- 2026-11-19 15:00 上線：後台在 emerswhlsystem.marc@gmail.com（Apps Script 部署 v1），指令碼屬性未設 PREORDER_SSO_SECRET／ADMIN_KEY，訂單彙整驗票由 Early Buy 收單程式代驗（`SSO_PROXY_URL`）。
- 用途：手上已到貨的現貨新品接單，不是預訂。以 DST Early Buy 前台為底、Code.gs 以 DSTC（含會員票券 SSO）為底。
- 商品：WAAC FW26 帽款＋桿頭套 19 款色／11 款，全部 ACC（品類：棒球帽、遮陽帽、漁夫帽、護耳帽、桿頭套）。來源 Excel 分頁 FW26（款號、色號、品號、SRP、Order 欄）。
- 庫存：每個尺寸有 `stock`（現有庫存）與 `pn`（品號）。來源＝WHL 每日倉庫庫存（emers-whl-system `unmatched_stock_codes.csv`，2026-11-19 的資料；這批品號還不在 WHL 主檔，所以內部站庫存頁看不到），25 個品號全對到，數量跟 Excel 的 Order 欄一致。`window.WAAC_STOCK_DATE` 顯示在頁首。
- 數量上限（2026-11-19 Marc 決定：只限單張訂單）：卡片每個尺寸顯示「庫存 N」，一張訂單各尺寸（連鎖分店合計）不能超過現有庫存，不扣其他訂單。輸入超過會自動壓回並提示；送單時 Code.gs `stockCheck_` 再擋一次（錯誤 `over_stock:[...]`）。`LIMIT_ACROSS_ORDERS = false`、index.html `USE_AVAIL = false`（不呼叫 `avail`）；要改先送出先占，兩個都改 true。多張單合計超過庫存由業務在款色彙總分配。
- 卡片直接顯示材質與產地（代碼行下方，手機版上下兩行），沒有「材質與產地」展開按鈕。
- 更新庫存：改 `tools/build_data.py`（重產 data.js）＋ Code.gs 的 `STOCK`／`STOCK_DATE` 常數（兩邊要一致），Code.gs 改完要部署新版本。
- 價格：顯示「建議售價」（SRP，NT$2,800／3,800）；HO 分店配貨折數沿用範本 0.5，未確認。
- 圖片：只有原廠 Excel 內嵌的線稿／實體混合小圖，多色合圖已裁成單色（`tools/crop.py`），沒有放大處理；沒有獨立實體圖。品名、中文顏色為暫定。頁首「資料待更新說明」列出這幾點。
- 前台沒有任何登入後台的入口；訂單彙整（刪除訂單、一鍵統整交單）只能從內部站 03 卡片「訂單彙整」開（#admin=會員票券，Code.gs 用指令碼屬性 PREORDER_SSO_SECRET 驗證）。
- 內部站串接（emers-whl-system，已上線）：key `waac-fw26-stock`、權限 `pre.waacs`，試算表 ID 已填進 tools/preorder_counts.py、tools/preorders_sync.py、internal/preorder-view.js 與 03 卡片／首頁後台連結。

### 入口網站串接（規劃中）
內部站（`emers-whl-system`）03 預訂單已經用連結掛上各系統，訂單彙整改走 WHL 會員票券，公開站不要放管理者入口。下面是較早的規劃筆記，仍可供參考：

| 做法 | 怎麼做 | 注意 |
|---|---|---|
| 連結（最穩） | 入口放按鈕，新分頁開客戶網址 | 不用改程式 |
| iframe 內嵌 | `<iframe src="https://marcwang13.github.io/<repo>/">` | Safari 會隔離 iframe 的儲存，客人可能每次都要重收驗證碼；建議新分頁開 |
| 入口讀訂單 | 入口網站**伺服器端**打 `GET <exec>?action=list&key=<ADMIN_KEY>` | ADMIN_KEY 只能放伺服器端 |
| 統一登入 | 四套 AUTH_SECRET 設成同一組（token 就能共用，但 localStorage key 不同，前端也要改成讀同一個 key），或改由入口網站發 token | 要改程式 |

### 其他
- **SDR 交單檔少 10 件**：「森富」訂單有一筆 `sku＝待確認`（配件、FREE SIZE、10 件、單價 3,280，零售 32,800）在 data.js 找不到商品，`hoUnits()` 會略過，交單檔總計 6,775 件／40,746,400，比 list API 少 10 件／32,800。`handoffCheck` 只比對訂單件數 vs 明細件數，抓不到這種情況。要請 Marc 確認這筆是什麼商品，改成正確 SKU；或之後在 `handoffCheck` 加「明細找不到商品」的提示。
- 同一張「森富」單有 LH0179 Presidio 球鞋 7W 2 件，但該款色只開 8W～12W（可能是客人匯入或業務改的），請確認。
- DST 客人「永璨體育登山用品社」聯絡 Email 欄有空白（`yt.sport@msa.hinet .net`），帳號 Email 正確，不影響通知。
- 有些單是業務用自己的帳號代下（帳號 Email 是 shihyao21@gmail.com、kai_weng@、vince_tian@、zero_wang@），這些單客人自己看不到。

## 9.5 交接驗證紀錄（2026-11-02，Grok Bot）

- GitHub：四個 repo 可讀（匿名 clone）。四站與 config.js 正常，四個端點健康檢查正常，錯誤 key 回 forbidden，正確 key 可讀 list。
- 測試方式：Playwright 攔截 script.google.com 回假資料，跑管理者登入、訂單彙整、刪除訂單按鈕、一鍵統整交單（含不一致時擋下）；交單檔用 LibreOffice 重算，核對總表與 APP／ACC／FTW 分頁的件數與 SRP。
- 文件和程式碼的差異已在上面各節更正（Code.gs 差異行數、tools 檔案、函式數、`--brand` 雙值、handoffCheck 原本只在 DST）。

## 10. 開新品牌（照範本複製）

> **2026-11-23 起（Marc 指示「以後都是」）：新品牌的線上訂單＋Excel 訂單本一律比照 DSTC（`dst-27fw-main-order`）架構**——卡片＝一款、同款多色列、性別／大類／系列篩選、尺寸格、下單總覽、Excel 訂單本（含款式圖／實體圖）匯出匯入、Apps Script 收單、金色 EMERS-WHL TW logo 在品牌名左邊、換品牌色。第一個照做的是 2XU H2-27（`2xu-h227-order`）：`tools/adapt_from_dstc.py` 是把 DSTC `index.html` 逐條改成新品牌的腳本（失敗會停在那一條），`tools/build_data.py` 從原廠訂單表＋型錄 PDF 產資料與圖，可當下一個品牌的起點。下面 1～6 步的流程照舊，第 3 步的「範本」改成 DSTC。

1. **收資料**：品牌訂單本 Excel（款號、品名、色號、色碼 SKU、尺寸、零售價、月份／交期、主題、商品說明）、尺寸表、娃娃圖或 CAD 圖、實體圖、前季尺寸銷售佔比、主題色。缺零售價、交期年份錯、整列標黃的先列給 Marc 確認；原表反黃＝不建議下單，品名加註。
2. **Marc 建 repo**：`marcwang13/<brand>-<season>-order`，開 GitHub Pages（main／root），給 AI 的 GitHub 帳號或 App 寫入權限。
3. **複製範本**：把 `sdr-fw27-order` 全部檔案複製過去，重產 `data.js`、`imgs.js`、`big/`；改第 3 節「字串差異」表的每一項、CSS `--brand` 色、`SHEETS`、`MONTH_ORDER`、`SIZE_COLS`、`SHARE`、訂單編號前綴；`NOTIFY_TO` 用固定名單。
4. **後端**：公司帳號新建試算表「<品牌> <季> 線上訂單」→ Apps Script 貼 `Code.gs` → 指令碼屬性加 `ADMIN_KEY`（與其他套相同）→ 部署成網頁應用程式（執行身分：我，存取：任何人）→ Marc 按授權 → 網址寫進 `config.js`。
5. **測試全流程**（第 8 節），測完刪測試資料。
6. **交付**：客戶網址、試算表連結給 Marc；做客戶版快速上手文件。管理密碼不寫進任何給客戶的東西。

## 11. 變更紀錄

| 日期 | AI | 系統 | 內容 | commit |
|---|---|---|---|---|
| 2026-11-23 | Grok Bot | 2XU | 開通收單：系統帳號試算表「2XU H2-27 正式訂貨 線上訂單」（ID `1uG5_S6ga0fLiHiL4U_5OB-zYVQyy_yQmaKRqTVMpJnc`，分享給 marc_wang@emers.com 可編輯）＋ Apps Script「2XU H2-27 正式訂貨 收單」v1（執行身分：我、存取：任何人；不設指令碼屬性，SSO 走 SSO_PROXY_URL，與 DSTC 相同）。前台 config.js 已接 SUBMIT_URL。repo main：a20cacb、066385a、f38a8f1（另有重複 commit 50ba526）。WHL 內部站改回一般收單卡片（v=20261123141612）。未完成：Claude 每日排程步驟 4 需加讀 2XU 試算表（`訂單!A1:Z500`＋分頁清單 → `--rows 2xu-h227=… --tabs 2xu-h227=…`）；一鍵統整交單 5 折沿用 DSTC（`HO_DISC=0.5`），尚未向 Marc 確認。 | a20cacb／066385a／f38a8f1 |
| 2026-11-23 | Grok Bot | 2XU | 新建 2XU H2-27 正式訂貨（本機 repo `2xu-h227-order`，照 DSTC 架構；未推 GitHub、未部署）：503 款色／149 款／2,619 尺寸，分頁＝原廠 Story 13 個，網頁顯示台灣建議售價 NT$；款式圖＝原廠訂單表內嵌圖（503 款色，8 款色借同款標示），實體圖＝型錄照（296 款色自有、32 借同款；長邊<220px 與漸層遮罩不用）；Drop 只顯示 Drop 1／2／3，不放月份（Marc 11/23）；原廠每色 20 件為全台灣合計，網站與 Excel 不寫；經銷商截止 2026/11/26；Code.gs 由 DSTC 版改品牌字串／Drop／NT$，要新開試算表＋Apps Script。第 10 節加「以後新品牌比照 DSTC」 | （本次） |
| 2026-11-20 | Grok Bot | DSTC | 實體圖放大改「填滿圖片區高度＋視窗寬度貼合照片」（不再限制不超過娃娃圖；手機改縮高度貼合；標題列可換行） | （本次） |
| 2026-11-20 | Grok Bot | DSTC | 實體圖改版（Marc 看完後）：放大檢視實體圖與娃娃圖同圖框、照片限制在娃娃圖顯示範圍內 contain（拿掉「原尺寸」）；Excel 實體圖顯示框同款式圖；同款借圖 143 款色（rp.js DSTC_RPB，說明在放大檢視與 Excel 備註，卡片「同款實體圖」） | （本次） |
| 2026-11-20 | Grok Bot | DSTC | 實體圖上線：4 本韓國門市實拍相簿比對後 259 款色、375 張（big/rp_*.jpg 長邊 2000px q90、rp.js 對照表、放大檢視加說明（「原尺寸」按鈕同日已拿掉）、Excel 實拍 400px）；待確認 29 組、畫質待確認 4 張見 tools/realphoto/ | （本次） |
| 2026-11-19 | Claude | DSTC | 同款多色列款式圖改固定 160px 正方形、上下置中（不再跟列高變大變小） | （本次） |
| 2026-11-19 | Claude | DSTC | 同款多色列的款式圖改成跟該列高度一樣（正方形、最小 120px），跟尺寸段對齊 | （本次） |
| 2026-11-19 | Claude | DSTC | 卡片標籤「Early Buy 已開訂」改顯示「Early Buy 已訂購款」（`ebLabel`，data.js 與 Excel 不動） | （本次） |
| 2026-11-19 | Claude | DSTC | 網頁分頁順序 NEO-ARCHIVE 移到 ACC 配件之後、鞋類之前（新增 `TAB_ORDER`，預設分頁改 TRAINING）；`SHEETS` 不動，Excel 訂單本與交單彙整順序不變 | （本次） |
| 2026-11-19 | Claude | DSTC | 原價售出比門檻改 9 折以上（build_ref.py 重跑 ref.js） | （本次） |
| 2026-11-19 | Claude | DSTC | 尺寸佔比數字改一般字重、內文字體 11.5px（不用粗體與等寬字） | （本次） |
| 2026-11-19 | Claude | DSTC | 按鈕平衡：商品細節改中深藍實心、過往參考加淡藍底＋粗框（CSS 變數 `--btn-pri`／`--btn-sec-*`）；尺寸佔比改整格深淺色塊（`--heat`，越高越深，拿掉長條） | （本次） |
| 2026-11-19 | Claude | DSTC | 版面：螢幕 ≥1100px 改左側欄（篩選、過往數據區域、搜尋、顯示選項、Excel、資料待更新說明），較窄維持原上方收合列；經銷資料填好後收成一行摘要（`renderDsum`，可再編輯）。過往參考改成跟商品細節同款按鈕、全價銷售比改名「原價售出比」；同款多色列的款式圖恢復 132px；對照款沒有的顏色標「此系列新色」；尺寸佔比加粗，最高的一格反白（`pctHTML`） | （本次） |
| 2026-11-19 | Claude | DSTC | 過往尺寸佔比放到每個尺寸格下方、對照款同色佔比放在色號旁（跟著北中南綜合切換）；過往參考面板保留 | （本次） |
| 2026-11-19 | Claude | DSTC | 同款不同色合併成一個外框（`groupHTML`／`rowHTML`）：外框上方一次顯示款名、說明、過往參考、「同款 N 色」，下面每色一列各自填數量；只有一色維持原卡片。只動畫面，訂單資料、Excel 訂單本、交單彙整都沒改 | （本次） |
| 2026-11-19 | Claude | DSTC | 過往參考拿掉中部／南部「資料期間較短」提醒，ref.js 不再放體系名稱與期間 | （本次） |
| 2026-11-19 | Claude | DSTC | 商品卡加「過往參考」：27FW 每款自動對照 25FW／26FW 舊款（同款延續／同系列同品類／同品類同價格帶／無對照），北部／中部／南部／綜合切換，顯示店均月銷、售罄率、全價銷售比、參考店數、尺寸分布、熱賣色（直營＋雷根＋動力，只給區域合計，不放店名與金額，排除 OUTLET／特賣／倉庫）。列表加「過往熱賣優先」排序、卡片加「去年熱賣」「新款無對照」標籤。資料由 `tools/build_ref.py --whl ../emers-whl-system` 產生 `ref.js`；人工改對照填 `tools/ref_override.json`。只同步這份文件，其他三個 repo 的副本待同步 | （本次） |
| 2026-11-02 | Grok | DST | 訂單彙整加下單分析：依大類（上衣／外套／背心／長褲）、分頁、系列（產品線｜主題）、經銷商統計款色數／尺寸數／件數／金額與佔比，可切換單一經銷商，展開訂單看該單。作廢排除，對不到商品標「找不到商品」。Excel 訂單本總表用公式同步。Apps Script 不用重新部署 | （本次） |
| 2026-11-02 | Grok | SDR | 訂單彙整加下單分析（範本，已併入 main）：依大類（服裝／配件／鞋款）、分頁、系列、經銷商。Excel 總表用公式 | fe901f0 |
| 2026-11-02 | Grok Bot | SDR、BY27SS、BY27FW | 一鍵統整交單：先重抓最新訂單並跑 handoffCheck，件數對不上就警告、不匯出 | b43842b／d0a4f4b／f791e22 |
| 2026-11-02 | Grok Bot | 四套 | 本文件放進四個 repo，新增同步規則（0.5 節）與變更紀錄 | （本次） |
| 2026-11-18 | Claude | DSTC | 新建 DESCENTE 27FW 正式訂貨（27Q3Q4）：APP／ACC／FTW 1,114 款色、詳細中文商品說明、FTW 分色圖、韓幣參考價、Early Buy 重複款標示 | （本次） |
| 2026-11-18 | Grok | DSTC | 原廠日期拿掉（data.js 刪 eta／launch、mon +1 月，只顯示「ETA X月」）；新增大類（上身／下身／配件／鞋類）與性別篩選；桌機分頁列換行；網頁不顯示韓國參考價與金額（Excel／CSV 保留）；掛進 WHL 內部站（dst-27fw-main，權限 pre.dstc） | （本次） |
| 2026-11-18 | Grok | DSTC | 單色款式圖 pc.js 擴充到 897／926（人工目視 479，工具在 emers-whl-system tools/dstc_percolor） | fa2d052 |
| 2026-11-18 | Grok | DSTC | ETA 全拿掉（卡片、篩選、分組、CSV／Excel）；上方三排篩選 性別／大類／系列（交集、0 筆變淡、自動跳分頁）；「全部配色」改「實體圖」按鈕（無圖灰掉＋實體圖待更新）；卡片「台灣定價待定」；頁首與 Excel 總表「資料待更新說明」條列；Excel 欄名「韓幣 MSRP(₩)」「韓幣金額(₩)」 | c01980d＋（本次） |
| 2026-11-19 | Claude | DSTC | 篩選列改四層四種樣式（性別分段／大類圖示分頁／系列標籤／小類文字，ACC、FTW 歸小類）、加「目前篩選」麵包屑；手機版篩選列可收合（頂端摘要列＋明顯「收合／展開篩選」按鈕，選系列後自動收合） | （本次） |

| 2026-11-10 | Claude | BY27SS | 跟新的 27SS Dashboard（…AKfycbxY7psb9…/exec）逐款核對：747 款色、尺寸、英文品名全部一致，沒有新增或刪除。依 Dashboard 新欄位 included_in_sample 把「展示會有樣品」從 70 擴到 207 個款色（tools/ss_dash_1110.txt）。鞋款加註原廠款號（2TSBY-XOX…）。CAD 仍缺 218 個款色 | （本次） |
| 2026-11-10 | Claude | BY27SS | 依原廠「KOREA TARGET 27SS APPAREL PACKING LIST」標了「샘플 O」的 74 個款色，在備註加「展示會有樣品」（對到 70 個款色／58 款）。名單在 tools/ss_samples.json | （本次） |
| 2026-11-10 | Claude | BY27SS、BY27FW | 拿掉價格（韓國 MSRP、台幣換算、零售金額）與韓國入倉日：資料欄位清空、卡片與統計隱藏金額、Excel 訂單本隱藏價格欄（欄位順序不變，匯入照舊）。27SS 拿掉 Sample 選款敘述，改成「台灣主打」標籤與篩選（47 款），沒有台灣市場備註的補上；上市月改成「台灣預計 N 月上市」（韓國入倉月往後一個月）。27FW 配件主打加 4 款。台灣定價公告後要把價格放回來。Apps Script 沒動，通知信的 Excel 金額會是 0 | （本次） |
| 2026-11-10 | Claude | BY27FW | 讀中國 TAG-ON 清單 xlsx 本體：補 11 個款色的圖（還有 56 個沒圖）；配件 46 款、鞋款 8 款補上「展示會有樣品」，其餘標「無樣品，請看款式圖下單」。對照在 tools/fw_tagon_img.json、fw_tagon_styles.json | （本次） |
| 2026-11-10 | Claude | BY27SS、BY27FW | 拿掉價格（韓國 MSRP、台幣換算、零售金額）：資料欄位清空、卡片與統計隱藏金額、Excel 訂單本隱藏價格欄（欄位順序不變）。27FW 配件主打加 4 款（共 35 款主打）。台灣定價公告後要把價格放回來；韓國售價仍留在 tools/fw2_src.json。詳見 by-27ss-order 同日紀錄 | （本次） |
| 2026-11-10 | Claude | BY27FW | 改讀原廠 RAWDATA xlsx 本體：685 款色／271 款（上一版從文字匯出只抓到 660）；款式圖改成每個顏色各一張，618 款色有圖、67 沒圖 | （本次） |
| 2026-11-10 | Claude | BY27FW | 商品資料改用原廠 11/9 的 27FW RAWDATA：150 筆→660 款色／271 款（新增配件 89、鞋 30）；拆到款色；不放韓國計畫量；韓國入倉批次換成月份後往後一個月當台灣上市月；新增「台灣主打」標籤與篩選（87 款色／31 款）、每款台灣市場備註、有無樣品備註。新款 CAD 還沒有（319 款色無圖）。產生程式 tools/gen_fw2.py | （本次） |
| 2026-11-11 | Claude | BY27SS | 款式圖（娃娃圖）原廠是整個款號一張總表、各色並排。用 OCR 讀色名標籤把總表切成一色一張（只留該色那一件，同時去掉韓文表頭與韓國計畫量），切不出來的維持原圖。Excel 訂單本與卡片：有樣品的款色備註與色名欄標綠底粗體 | （本次） |
| 2026-11-11 | Claude | BY27FW | 款式圖（娃娃圖）原廠是整個款號一張總表、各色並排。用 OCR 讀色名標籤把總表切成一色一張（只留該色那一件，同時去掉韓文表頭與韓國計畫量），切不出來的維持原圖。Excel 訂單本與卡片：有樣品的款色備註與色名欄標綠底粗體 | （本次） |
| 2026-11-12 | Claude | BY27SS、BY27FW | 「此款…樣品」也標綠：卡片與 Excel 訂單本的綠底條件改成備註開頭是「展示會有樣品」或「此款」。27SS 151 款色備註改為「此款號展示會有樣品，樣品是哪個顏色以現場為準」（FW 鞋 30 款色文字不變） | （本次） |
| 2026-11-12 | Claude | BY27SS、BY27FW | 樣品標註改成照實際寄到的三份樣品清單（北京 Invoice 1109_update1、韓國 27SS 服裝 Packing List、韓國 27SS 鞋 17PCS）。原則：寧可少標不可多標。「展示會有樣品」＝該款色確定有（綠底）；清單沒列顏色的寫「此款展示會有樣品，顏色以現場為準」（不標綠）。27SS：鞋 17 款色「有樣品」，服裝 151 款色「此款有樣品」，品名對不上的 1BYHDMW501、1BYZTMW504 不標。27FW：350 款色「有樣品」（款號＋顏色逐筆對發票），鞋 30 款色「此款有樣品」，27FMGJ030-BU 發票品名錯不標。只動 data.js 的 note 欄 | （本次） |
| 2026-11-12 | Claude | BY27SS | 鞋款圖改完整：原本是整張 CAD 頁或只剩鞋跟局部，改由 CAD 頁依顏色裁出完整一隻（`tools/shoe_crops.py`，12 款色）；502/908/914 沒有 CAD 頁，借 27FW 同系列完整圖並標 `ref`=3「同系列鞋款（27FW 圖），配色不同，僅供參考」。仍是鞋跟局部：ABYSHXW902-BR／903-BK（YAKLOAD REMASTER），要原廠整隻圖 | （本次） |
| 2026-11-12 | Claude | BY27SS | 借來的圖加標註：data.js 品項新增 `ref`（1=同款其他色、2=同名另一性別），卡片圖下顯示「同款，顏色不同，僅供參考」／「同款式（另一性別）圖，僅供參考」；fill_images.py 之後會自動寫 ref | （本次） |
| 2026-11-12 | Claude | BY27SS | Marc 指示「都要有圖最重要」：沒圖的款色依序借 1) 同款號其他顏色的圖 2) 被移除的小圖工藝單（僅 27SS）3) 同品名同品類他性別的圖；借來的圖顏色可能不同。程式 `tools/fill_images.py`（重產後與 `post_1112_fix.py` 一起再跑，順序：先 post_1112_fix 再 fill_images）。仍沒圖：27SS 208 款色（配件 172）、27FW 44 款色，要原廠提供乾淨的圖 | （本次） |
| 2026-11-12 | Claude | BY27SS | 分類全面檢查：配件分頁裡 11 款（22 款色）其實是衣服，移到上身（排汗衣 5 款、背心 2 款、無袖上衣 3 款、DNS LIMIA 連帽衫 1 款）；3 款「女款」帽子性別改女。上身 352→374、配件 246→224。改寫程式 `tools/post_1112_fix.py`（重產 data.js 後要再跑）。款式圖：原廠整頁工藝單縮成 118 像素寬的小圖（韓文表格、尺寸、設計師欄位，71 張／166 款色）整批移除，這些款色改顯示「尚無圖片」，要補需原廠給乾淨的款式圖。仍留著的：多款拼貼的設計稿（帽子、襪子、背包、鞋款，一張圖含多個商品）與部分只有鞋跟的裁圖 | （本次） |
| 2026-11-12 | Claude | BY27SS、BY27FW | 所有 Excel／CSV 輸出都加「上市月」欄：下載訂單本（原隱藏的韓國入倉欄改名顯示）、CSV 明細／款色彙總、複製用 TSV、一鍵統整交單（月份後面插一欄）、Apps Script 的「明細」分頁（`LINE_HEAD` 最後新增「上市月」，舊資料為空）與每張訂單分頁。**Code.gs 要貼進編輯器並部署新版本才生效** | （本次） |
| 2026-11-12 | Claude | BY27SS、BY27FW | 上方分類篩選列（月份／系列 chip，id=`months`）由複選改單選：點一顆會取代前一顆，再點同一顆回到「全部」。只改 index.html 的 `#months` click handler，篩選條件 `S.months` 仍是 Set（最多一個值）| （本次） |
| 2026-11-12 | Claude | BY27SS、BY27FW | 沒有上市月的款式一律補上相近款的月份：27FW 509 款色（208 款）、27SS 35 款色（26 款）。27FW 依「同品名→同系列＋同品類＋款號最近」找參考款；配件與鞋款（56 款）同季沒有已知款，用全季最多款的 11 月。27SS 依「同品類＋同系列＋同性別＋款號最近」。對照表在 `tools/launch_infer.csv`（改月份只要改 data.js 的 `monTag`／`launch`）；頁面說明文字改成「月份參考相近款推估」| （本次） |
| 2026-11-12 | Claude | BY27SS、BY27FW | 台灣建議售價定案（公司 TW-SRP 價格表，一款色一價）：data.js 的 `price` 填入（27SS 747 款色全有；27FW 645 款色，40 個中國專屬款色表上沒填，卡片顯示「售價待確認」）；卡片、小計、總計、Excel 訂單本的價格欄與零售金額放回來（韓國入倉、韓國 MSRP 欄仍隱藏、仍是空的）；拿掉 index.html 結尾的 NOPRICE-SWEEP；Apps Script `SHOW_PRICE` 改 true（**要貼進 Apps Script 編輯器並部署新版本才生效**）| （本次） |
| 2026-11-12 | Claude | BY27FW | 借來的圖加標註：data.js 品項新增 `ref`（1=同款其他色、2=同名另一性別），卡片圖下顯示「同款，顏色不同，僅供參考」／「同款式（另一性別）圖，僅供參考」；fill_images.py 之後會自動寫 ref | （本次） |
| 2026-11-12 | Claude | BY27FW | Marc 指示「都要有圖最重要」：沒圖的款色依序借 1) 同款號其他顏色的圖 2) 被移除的小圖工藝單（僅 27SS）3) 同品名同品類他性別的圖；借來的圖顏色可能不同。程式 `tools/fill_images.py`（重產後與 `post_1112_fix.py` 一起再跑，順序：先 post_1112_fix 再 fill_images）。仍沒圖：27SS 208 款色（配件 172）、27FW 44 款色，要原廠提供乾淨的圖 | （本次） |
| 2026-11-12 | Claude | BY27FW | 分類與款式圖檢查：27XWET070 性別改女；其他T恤拆成 POLO衫／襯衫／無袖上衣；27WMPD652、27WWPD653 鋪棉外套→背心；27WUHD309 刷毛外套→連帽衫；「遠征羽絨外套（待原廠）」中性那筆背心→羽絨外套。移除錯的款式圖：Polartec 布料吊牌實拍（8 款色）、27FWRT008-TN 布料吊牌實拍、27UWPA156-HE 空白圖、韓文表頭設計稿（2 款色）、TRICOT 套裝長褲誤用外套圖（3 款色）、模特兒實拍（27WWPA101-DU）。改寫程式 `tools/post_1112_fix.py`（重產後要再跑） | （本次） |
| 2026-11-12 | Claude | BY27FW | 服裝尺寸段（原廠沒給）改照 27SS 同性別、同類型款式補：原本 ASSORTED「數量」的服裝款色改成實際尺寸（上身 85–130 數字碼、下身腰圍或 XS–XL；對照與規則見 `tools/fw_sizes_from_ss.py`，取 27SS 該類型至少 1/3 款有的尺寸，寧可多不要少）。拿掉備註「尺寸段待原廠提供」與頁面「數量」說明（改成「樣品」一句）；`szOrder` 併入 27SS 的數字尺碼。**原廠正式尺寸段出來後要改回來**；重跑 `gen_fw2.py` 會把尺寸洗回 ASSORTED，之後要再跑 `python3 tools/fw_sizes_from_ss.py data.js <27SS data.js> --write` | （本次） |
| 2026-11-12 | Claude | BY27FW | 中國專屬款整個拿掉（80 款色／31 款）：data.js 移除、`months` 清單移除該系列、拿掉「售價待確認」說明。原始資料仍在 `tools/fw2_src.json`，重產（gen_fw2.py）時要再排除中國專屬款。 | （本次） |
| 2026-11-13 | Claude | BY27FW | 與原廠 Dashboard（11/12 版）對齊：拿掉系統有、Dashboard 沒有的 224 款色（上身 185、下身 39；214 款色整個款號 Dashboard 沒有、10 款色是同款號其他色）。這批來自 Rob 11/9 的「KOREA TARGET 27FW_취합_RAWDATA-ACC.xlsx」，Marc 要拿清單問原廠。被拿掉的 id 清單在 `tools/removed_1113_not_in_dashboard.json`，原廠確認要供再從 git 歷史（64660b9）取回。`imgs.js` 沒刪對應圖。現在 456 款色。重產（gen_fw2.py）會把這批加回來，要再刪。 | （本次） |
| 2026-11-13 | Claude | BY27FW | 中國專屬款再加回 40 款色／15 款（原廠 Dashboard 有、公司價格表沒填價）：`price` 空、備註「中國專屬款；價格原廠待定」，卡片顯示「價格原廠待定」，Excel 價格欄空白。至此 Dashboard 的中國專屬款色除 27WMPD501／27WWPD501（4 色，有價 16,880，Marc 11/12 指示不加）與 27FMRT686-LG（Dashboard 沒有）外都在系統裡。現在 680 款色。 | （本次） |
| 2026-11-13 | Claude | BY27FW | 對照原廠 Dashboard（11/12 版）：中國專屬款加回 35 款色／13 款（只加價格表有價、且 Dashboard 有的；價格取自 11/12 拿掉前的 data.js）。**不加**：40 個價格表沒填價的款色，以及 27WMPD501／27WWPD501／27WMJK606／27WWJK606／27FWGJ682 這 5 款（Marc 11/12 指示不加）。27FMRT686-LG 原廠 Dashboard 沒有，也不加。備註只寫「中國專屬款」，不宣稱有無樣品；服裝尺寸段照 `fw_sizes_from_ss.py` 補。`BY_CFG.months` 加回「中國專屬款」。重產（gen_fw2.py）會洗掉這批，要再加。 | （本次） |
| 2026-11-16 | Grok Bot | BYS | 拿掉「展示會有樣品」和「此款號展示會有樣品，樣品是哪個顏色以現場為準」。特價商品等其他備註留著。卡片不再標綠，Excel 訂單本不再把色名和備註塗綠 | （本次） |
| 2026-11-16 | Grok Bot | BYF | 拿掉「展示會有樣品」：備註只刪這句（中國專屬款、延續款等其他備註留著），卡片不再標綠，Excel 訂單本不再把色名和備註塗綠。頁面說明改成圖片怎麼切換 | （本次） |
| 2026-11-16 | Grok Bot | BYF | 訂單彙整加下單分析（移植 SDR fe901f0，對齊現在的分頁）：依大類（服裝＝上身＋下身、配件、鞋款）、分頁、系列（主題）、經銷商統計款色數／尺寸數／件數／零售金額／佔比。可切換經銷商，展開訂單看該單。對不到商品標成找不到商品，作廢不計。Excel 總表用公式同步。韓國 MSRP 與零售金額 TWD 保留。另外 112 款色加上實拍（正面、背面；27FWPN071 黑灰實拍併入 G8，27WUPA301 藍綠連帽改掛 UB） | （本次） |
| 2026-11-17 | Claude | BY27SS、BY27FW | 防舊版快取：index.html 開頭先問 `version.json`（不走快取），發現自己不是最新版就自動換成帶 `?v=` 的新網址並保留 `#` 後面的內容，所以從入口網站、iframe、書籤進來都會拿到最新版；新增 `tools/bump_version.py`。**之後每次改完要 push 前都要跑 `python3 tools/bump_version.py`**（會更新 index.html 的版本號、script 的 `?v=`、version.json）。入口網站如果自己存了一份程式（不是連結或 iframe），不在這個機制內。 | 待填 |
| 2026-11-17 | Claude | BY27SS | 款卡加「機能素材」標章與中文說明：`tools/add_tech.py` 依 icon（特殊素材）、品名、概述、成分判斷每款用到的 GORE-TEX（PRO 3L／3L／2L／鞋款）、WINDSTOPPER、POLARTEC 各系列、PERTEX、PRIMALOFT、G-LOFT、羽絨（絨種／FP／絨羽比）、CORDURA、DYNEEMA、SCHOELLER、MERINO、VIBRAM，寫入 data.js 的 `tg`（卡片）與 `tech`（Excel「材質與科技」欄）；`fab` 成分加中文翻譯並保留原文。說明文字查自各品牌官方與通路資料；規格沒寫明的款（例如 GORE-TEX 沒寫層數、POLARTEC 沒寫系列、羽絨沒寫絨種）一律借同分頁同品類、最相近款的規格，不寫「原廠未註明」，借用清單在 add_tech.py 執行時印出；BLACK YAK 自家款名（AIR FLY、AIRDOT、HYPER 等）原廠沒給規格，不寫說明。重產 data.js 後要再跑 `python3 tools/add_tech.py data.js`。搜尋框可搜素材名。 | 4ee3848 |
| 2026-11-17 | Claude | BY27SS | 款卡與 Excel 訂單本加「編號」：data.js 的 `no` 填入訂單目錄（客戶版 A4，27SS 1–349、27FW 350–533）的編號，一個款號一個編號，同款各色同編號；卡片款號列前面顯示「編號 N」，搜尋框可用「編號」或數字找；編號來源是 11/13 版訂單目錄 PDF，依款號對應（本系統 1–349）。 | a5313e8 |
| 2026-11-17 | Claude | BY27FW | 款卡加「機能素材」標章與中文說明：`tools/add_tech.py` 依 icon（特殊素材）、品名、概述、成分判斷每款用到的 GORE-TEX（PRO 3L／3L／2L／鞋款）、WINDSTOPPER、POLARTEC 各系列、PERTEX、PRIMALOFT、G-LOFT、羽絨（絨種／FP／絨羽比）、CORDURA、DYNEEMA、SCHOELLER、MERINO、VIBRAM，寫入 data.js 的 `tg`（卡片）與 `tech`（Excel「材質與科技」欄）；`fab` 成分加中文翻譯並保留原文。說明文字查自各品牌官方與通路資料；規格沒寫明的款（例如 GORE-TEX 沒寫層數、POLARTEC 沒寫系列、羽絨沒寫絨種）一律借同分頁同品類、最相近款的規格，不寫「原廠未註明」，借用清單在 add_tech.py 執行時印出；BLACK YAK 自家款名（AIR FLY、AIRDOT、HYPER 等）原廠沒給規格，不寫說明。重產 data.js 後要再跑 `python3 tools/add_tech.py data.js`。搜尋框可搜素材名。 | 4cfee30 |
| 2026-11-17 | Claude | BY27FW | 款卡與 Excel 訂單本加「編號」：data.js 的 `no` 填入訂單目錄（客戶版 A4，27SS 1–349、27FW 350–533）的編號，一個款號一個編號，同款各色同編號；卡片款號列前面顯示「編號 N」，搜尋框可用「編號」或數字找；編號來源是 11/13 版訂單目錄 PDF，依款號對應（本系統 350–533）。 | 05fdf67 |
| 2026-11-18 | Claude | BY27SS | 把原廠「27SS Visual Strategy ZH」簡報（整合策略，24 頁）整理進訂貨頁：①新增「季節策略」面板（story.js，頁首按鈕）②各系列分組下加「商品資訊」摺疊說明 ③款名對得上的 73 個款色卡片加「商品資訊」欄（data.js 的 info 欄，tools/add_pdf_info.py 產生）④Excel 訂單本新增「商品資訊」欄（在「材質與科技」後、「備註」前，匯入照舊）。不放韓元目標、韓國售價、款數／SKU 計畫、折扣率、內部時程 | （本次） |
| 2026-11-18 | Claude | BY27SS | 依 Marc 指示，原廠簡報內容只留商品本身資訊（材質、規格、機能、搭配）：拿掉售出率、銷售做法、通路分工、每週銷售數字等；面板改名「季節商品資訊」。全頁不含任何韓國價格 | （本次） |
| 2026-11-18 | Claude | BY27SS | 系列「商品資訊」改成預設展開 | （本次） |
| 2026-11-18 | Claude | BY27FW | 把原廠「27FW Visual Strategy ZH」簡報的商品資訊整理進訂貨頁（比照 27SS）：頁首「季節商品資訊」面板（story.js）、各系列「商品資訊」摺疊說明、款名對得上的 149 個款色卡片加「商品資訊」（tools/add_pdf_info.py，gen_fw2.py 重產後要再跑）、Excel 訂單本加「商品資訊」欄（材質與科技後、備註前，匯入照舊）。只放商品本身資訊，不含任何韓國價格、銷售目標與銷售做法 | （本次） |
| 2026-11-18 | Claude | BY27FW | 系列「商品資訊」改成預設展開 | （本次） |
| 2026-11-19 | Claude | 手機版篩選列 | 篩選列頂端新增摘要列與明顯的「收合／展開篩選」按鈕，手機版可收合（桌機不變，狀態記在 sessionStorage） | （本次） |
| 2026-11-19 | Grok | WAAC | 上線：config.js 接系統帳號的 Apps Script，交接文件補後端網址與試算表 | （本次） |
| 2026-11-19 | Grok | WAAC | 數量上限改為只限單張訂單（LIMIT_ACROSS_ORDERS=false、USE_AVAIL=false，拿掉「可訂」字樣）；材質與產地直接顯示在卡片上，拿掉展開按鈕 | （本次） |
| 2026-11-19 | Grok | WAAC | 新增 WAAC FW26 現貨訂貨站：每尺寸顯示現有庫存、前後台都擋超過可訂量、現貨標籤、性別／品類篩選、無前台後台入口（只走內部站票券） | （本次） |
| 2026-11-19 | Grok Bot | 全部 | 將本檔定為唯一正本（只在 dst-27fw-main-order 維護）。補上其他 repo 副本裡仍有效、正本沒有的內容（WAAC 系統與現況、BY 變更紀錄與售價定案、各站手機篩選列等）。搬家前的舊試算表與舊 Apps Script 網址不搬；後端表改列 2026-11-19 核對過的現行網址與系統帳號試算表。其他 repo 的同名檔改成一行指向本檔。 | （本次） |
