/* DESCENTE 27Q3Q4 季節商品資訊（來源：27Q3Q4 Convention Sheet EN、H2-27 Specialised Digital Catalogue，系統內各系列說明；上市月取自訂單資料）
   比照 BLACK YAK 27FW：只放商品本身的資訊（材質、機能、版型、搭配）。
   不放任何價格（含韓國參考價）、銷售目標、售罄率、款數／SKU、折扣、內部時程。
   season = 季節商品面板（右上「季節商品資訊」按鈕）。 */
window.DST_STORY = {
  season: {
    title: '27Q3Q4 季節商品資訊',
    lead: '這一季從夏末的涼感訓練、通風跑步，一路接到冬天的輕量羽絨和滑雪系列。Q3 重點是透氣、速乾、好活動；Q4 改成保暖疊穿，羽絨、刷毛、WINDSTOPPER 都在這一段上市。鞋款比服裝早，5 月起陸續到。',
    sections: [
      {
        h: '上市節奏',
        note: '各款實際上市月以商品卡上的月份為準，這張表只看大方向。',
        table: {
          head: ['月份', '服裝', '配件', '鞋款'],
          rows: [
            ['5–7月', '—', '—', 'MOVEWEAR 先到（SNEAKERS、CHRON、聯名、CLASSIC RUNNING、UTILITY）；7 月跑鞋全線上市'],
            ['8月', 'TRAINING 涼感／F-360、RUNNING 通風與日常跑、WELSH 鐵人三項、TOUGH、WOMENS 三線、SWISS SKI 輕量款', '大部分 Q3 帽款、包款、跑步配件', 'DELTA、ENERZITE、CHRON、CLASSIC RUNNING 第二波'],
            ['9月', 'D-ESSENTIAL、D-TECH 換季套裝、DAILY RUN 長袖', '—', 'TRAIL 越野鞋'],
            ['10月', 'NEO-ARCHIVE GORE-TEX、DE:LIGHT、CANON、POLARTEC POWER DRY、NEW CONTOUR、DAWN CHASER V2', 'PREMIUM TECH ESSENTIAL 冬季帽款、SWISS SKI、女款雪地配件開始', '冬季鋪棉靴、瑪莉珍、拖鞋'],
            ['11–12月', 'SWISS SKI 主力、POLARTEC 微刷毛、D-TECH 都會羽絨、DAWN CHASER V2 主力', '女款雪地配件、PERTEX 保暖配件', '—']
          ]
        }
      },
      {
        h: '服裝系列',
        cards: [
          { t: 'RUNNING', b: [
            'HYPER-ENGINEERED RUN（Q3）：工程提花網布照身體散熱分區配網孔，高熱區雷射打孔，主打通風。',
            'DAWN CHASER V2（Q4）：給冬季、清晨練跑的中高階跑者，WINDSTOPPER、羽絨拼接、刷毛疊穿。',
            'DAILY RUN：日常跑步基本款，速乾、輕、好搭。',
            'DELTA PRO：跑步最高階競速線，依選手回饋開發。'
          ]},
          { t: 'INSPIRED：WELSH TRIATHLON', b: [
            '第一次推出英國威爾斯鐵人三項隊的隊伍圖案。',
            'EARLY COOL SHIFT 夏轉秋涼感單品，涼感經編布加機械彈性布。',
            '重點搭配：機械彈性梭織防風外套＋短褲套裝、涼感經編 T 恤。'
          ]},
          { t: 'TRAINING', b: [
            'F-360：照肌肉動作設計的人體工學版型，加 ABS 通風（提花／網布拼接），運動中快速排汗。',
            'COOLING：尼龍彈性涼感經編布，摸起來是涼的，夏季訓練用。',
            'SORONA：玉米生質機械彈性布，耐用有彈性，輕度訓練到日常都行。',
            'OVER FIT（GIANT）：寬版輪廓的連帽 T、運動褲。'
          ]},
          { t: 'SNOW', b: [
            'SWISS SKI：以瑞士國家滑雪隊為靈感，Q3 輕量材質，Q4 加入瑞士滑雪傳統的實用單品。',
            'DE:LIGHT：PERTEX QUANTUM 10D 超輕量面料加高比例羽絨，表布、內裡、副料全部減重。',
            'CANON：DESCENTE 冬季代表羽絨，HEAT NAVI 蓄熱內裡、紋理撞色布。',
            'POLARTEC®：MICRO FLEECE 微刷毛輕量保暖；POWER DRY 雙組分網眼，可單穿或當中層。',
            'SKI ESSENTIAL：滑雪場基本款，防風防水長褲與運動外套。'
          ]},
          { t: 'WOMENS SNOW：NEW CONTOUR', b: [
            '風格優先，拿掉羽絨的臃腫感，輪廓俐落。',
            '女性化冬季面料：HEAT NAVI、光澤布、仿麂皮、菱格絎縫。',
            '重點搭配：菱格絎縫羽絨外套、光澤羽絨外套。'
          ]},
          { t: 'PREMIUM TECH ESSENTIAL', b: [
            'D-TECH：Q3 都會機能套裝，褲型多種可選；Q4 URBAN TRANSIT DOWN，霧面輕量布料的都會羽絨。',
            'D-ESSENTIAL：Supima 棉毛圈布、AERO KNIT 舒適套裝；Q4 從刷毛毛圈到 80:20 鴨絨 Puffer，依溫度分層。',
            'TOUGH：招牌 TOUGH 布（吸濕排汗、彈性、保型）短袖、長袖、POLO；新增高密度防透 TOUGH SHIELD，以及寬版、女款半短版。'
          ]},
          { t: 'WOMENS', b: [
            'GYM FIT：FLEX-SKIN（尼龍 66＋高含量彈性纖維），像第二層皮膚一樣貼合，HYROX 訓練也能穿。',
            'ALL-DAY FIT：羅紋針織、菱紋毛圈、MICRO MODAL、刷毛針織，運動和日常兩用。',
            'RUN FIT：給中階女跑者，防潑水套裝和速乾單品。'
          ]},
          { t: 'NEO-ARCHIVE：DESCENTE × GORE-TEX', b: [
            '用 GORE-TEX 做的城市跑步通勤服，能跑也能上班。',
            '上衣加強通風，褲子調整版型；外套和背心之間有扣合系統，秋冬疊穿方便。',
            '重點搭配：GORE-TEX 外套、WINDSTOPPER 長褲。'
          ]}
        ]
      },
      {
        h: '配件',
        cards: [
          { t: 'PREMIUM TECH ESSENTIAL ACC', b: [
            '依用途和材質分：PACKABLE（可收納）、PACKET（軍事工裝）、BOUND（夏季網布）、D-TECH（通勤）。',
            '帽款從夏末、換季到冬季分段規劃；毛帽分厚度，另有保暖圍脖。'
          ]},
          { t: 'RUNNING ACC', b: [
            '新推輕量可收納跑步包款。',
            '跑帽有通風款和保暖款；袖套、小腿套、頭套、圍脖可成套搭配。'
          ]},
          { t: 'SNOW ACC', b: [
            'SWISS SKI：Q3 LOGO 單肩包與帽款，Q4 滑雪實用單品。',
            'PERTEX 與女款雪地配件集中在 10–11 月，搭冬季外套一起看。'
          ]},
          { t: 'TRAINING／WOMENS／WELSH ACC', b: [
            '跟著服裝系列走，同系列可以整套搭配陳列。'
          ]}
        ]
      },
      {
        h: '鞋款',
        cards: [
          { t: 'FTW RUNNING', b: [
            'ELITE（DELTA）：給追個人紀錄的跑者，和 DISC 研究所合作，PEBA、A-TPU 輕量高回彈中底。',
            'PERFORMER（ENERZITE）：把競速鞋的中底和 Z FOAM BETA+ 帶進日常跑鞋，有緩震、中性、穩定、GORE-TEX 幾種配置。',
            'EASY：ZEROMOTION 好穿好脫，日常緩震、輕量。',
            'TRAIL：GEKSEN 短中距離硬地越野；SOREVO V2 給 50km 以上超馬；ULTRARIDGE V2 BOA® 是頂級越野鞋。'
          ]},
          { t: 'FTW MOVEWEAR', b: [
            'CLASSIC RUNNING：DMARATHON 等復古跑鞋，加上跑鞋緩震大底的混血休閒鞋。',
            'CHRON：經典檔案現代復刻，新增寬楦和天然皮革版。',
            'SNEAKERS：DRIBBLE NEO、EDGE COURT 球場鞋，D.WIDE 寬楦免手穿。',
            'UTILITY：ZEROMOTION 免手穿、BOA® 旋鈕、POWERGRIP 大底，城市到輕度登山。',
            'SEASONAL：女款瑪莉珍、緩震拖鞋、冬季鋪棉靴 ARCTIC SHIELD、AERO-PUFF。',
            'COLLABO：和 HATCHINGROOM 的聯名限量款。'
          ]}
        ]
      }
    ],
    foot: '內容整理自原廠 Convention 資料，只放商品資訊。台灣主打款、行銷點款式待 C TEAM 確認後補上。'
  }
};
