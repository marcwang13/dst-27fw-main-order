#!/usr/bin/env python3
"""27FW 新款對照過往銷售（北／中／南／綜合），產出 ref.js 與對照表 Excel。

用法：
  python3 tools/build_ref.py --whl ../emers-whl-system [--xlsx 對照表.xlsx] [--override tools/ref_override.json]

資料來源（emers-whl-system）：
  dealer/data/chain_leigen_*.json、chain_dongli_*.json、internal/data/direct_chain_*.json
只算 DESCENTE（不含 DESCENTE GOLF），排除 OUTLET、特賣、倉庫。
對照三層：L1 同款延續（同款號去掉年份碼，或英文品名相同）、L2 同系列同品類（系列碼＋品類碼＋性別，FW）、
L3 同品類同價格帶（品類碼＋性別，FW，價格 ±20%）。
ref_override.json 可人工指定：{"SS321TJK91": ["SQ321TJK91"], "SS999XXX99": []}（空陣列＝無對照）。
"""
import argparse, json, re, statistics, collections, os, datetime

CODE = re.compile(r'S([A-Z])(\d)(\d)(\d)([A-Z])([A-Z]{2})([A-Z0-9])([A-Z0-9])')
YEAR = {'P': 24, 'Q': 25, 'R': 26, 'S': 27}

# 店點區域：直營用主檔 region；經銷依店名。None＝不算（OUTLET、特賣、倉庫）
LEIGEN_REGION = {'0001': '中部', '0046': None, '0000': '南部'}  # 0000 天王待確認，暫列南部（目前無銷售）
DONGLI_REGION = {'0066': '北部', '0067': '北部', '0000': None, '0401': None, '0901': None, '0ZZZZ': None, '0968': None}
REG_KEY = {'北部': 'n', '中部': 'c', '南部': 's'}


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def style_of(key, item):
    for s in (key, (item or {}).get('raw', ''), (item or {}).get('k', '')):
        m = CODE.search(s or '')
        if m:
            return m.group(0)
    return None


def color_of(key):
    return key.split('-', 1)[1] if '-' in key else ''


def is_fw(code):
    t = code[8]
    return t in '789'


def region_of(src, sid, store):
    if src == 'direct':
        if store.get('channel') in ('OUTLET', '特賣'):
            return None
        return store.get('region')
    if src == 'leigen':
        return LEIGEN_REGION.get(sid, '南部')
    return DONGLI_REGION.get(sid, '中部')


# ---------- 尺寸正規化 ----------
TOP = {'男': {85: 'XS', 90: 'S', 95: 'M', 100: 'L', 105: 'XL', 110: '2XL', 115: '3XL', 120: '4XL'},
       '女': {80: 'XS', 85: 'S', 90: 'M', 95: 'L', 100: 'XL', 105: '2XL'},
       '中性': {80: 'W-XS', 85: 'W-S', 90: 'W-M', 92: 'W-L', 95: 'M', 100: 'L', 105: 'XL', 110: '2XL', 115: '3XL', 120: '4XL'}}
BOT = {'男': {80: 'S', 85: 'M', 90: 'L', 95: 'XL', 100: '2XL', 105: '3XL', 110: '4XL'},
       '女': {65: 'XS', 70: 'S', 75: 'M', 80: 'L', 85: 'XL', 90: '2XL'},
       '中性': {65: 'W-XS', 70: 'W-S', 75: 'W-M', 80: 'W-L', 85: 'M', 90: 'L', 95: 'XL', 100: '2XL', 105: '3XL'}}


def norm_size(z, it):
    z = str(z or '').strip().upper()
    if not z:
        return None
    m = re.search(r'\(([^)]+)\)', z)
    if m:
        return m.group(1).strip()
    cls = it.get('cls')
    if cls == '鞋':
        try:
            v = float(z)
        except ValueError:
            return None
        return str(int(round(v * 10))) if v < 40 else str(int(v))
    if cls == '配':
        return 'F'
    if re.fullmatch(r'(W-)?(XS|S|M|L|XL|2XL|3XL|4XL)', z):
        return z
    if re.fullmatch(r'\d+', z):
        g = it.get('gx') if it.get('gx') in ('男', '女') else '中性'
        tab = BOT if '褲' in (it.get('t') or '') else TOP
        return tab[g].get(int(z))
    return None


def adapt_size(label, gen):
    """把舊款尺寸標籤換成新款尺寸段的寫法。"""
    if gen == '女':
        return label if label.startswith('W-') else 'W-' + label
    if gen == '男':
        return None if label.startswith('W-') else label
    if label == 'S':
        return 'W-L'  # 中性新款沒有男 S，最接近 W-L
    return label


def norm_name(s):
    s = (s or '').lower()
    s = re.sub(r"\b(men'?s|women'?s|unisex|w's|m's|mens|womens)\b", ' ', s)
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return ' '.join(s.split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--whl', required=True)
    ap.add_argument('--repo', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--xlsx')
    ap.add_argument('--override', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ref_override.json'))
    a = ap.parse_args()

    srcs = {
        'direct': ('internal/data/direct_chain_sales.json', 'internal/data/direct_chain_stock.json', '直營'),
        'leigen': ('dealer/data/chain_leigen_sales.json', 'dealer/data/chain_leigen_stock.json', '雷根'),
        'dongli': ('dealer/data/chain_dongli_sales.json', 'dealer/data/chain_dongli_stock.json', '動力'),
    }
    old = {}  # style -> attrs
    sales = collections.defaultdict(list)  # style -> [(rk, sid, ym, size, qty, full, color)]
    stock = collections.defaultdict(lambda: collections.Counter())  # style -> {rk: qty}
    stores_by_reg = collections.defaultdict(set)
    periods = {}
    for src, (fs, fk, label) in srcs.items():
        S = load(os.path.join(a.whl, fs))
        periods[label] = (S['dateFrom'], S['dateTo'])
        smap = {s['id']: s for s in S['stores']}
        for r in S['rows']:
            key = r[2]
            it = S['items'].get(key) or {}
            if it.get('b') != 'DESCENTE':
                continue
            st = style_of(key, it)
            if not st:
                continue
            reg = region_of(src, r[0], smap.get(r[0], {}))
            o = old.setdefault(st, {'style': st, 'en': '', 'list': 0, 'gx': '', 't': '', 'cls': '', 'season': it.get('s') or ''})
            o['en'] = o['en'] or it.get('en') or it.get('cn') or ''
            o['list'] = o['list'] or it.get('list') or 0
            o['gx'] = o['gx'] or (it.get('gx') if it.get('gx') != '未標示' else '')
            o['t'] = o['t'] or it.get('t') or ''
            o['cls'] = o['cls'] or it.get('cls') or ''
            o['zh'] = o.get('zh') or it.get('z') or ''
            if not reg:
                continue
            qty = r[4] or 0
            amt, lst = r[5] or 0, r[6] or 0
            full = qty > 0 and lst > 0 and amt >= lst * 0.95
            sales[st].append((REG_KEY[reg], f'{src}:{r[0]}', r[1][:7], norm_size(r[3], it), qty, full, color_of(key)))
            if qty > 0:
                stores_by_reg[REG_KEY[reg]].add(f'{src}:{r[0]}')
        K = load(os.path.join(a.whl, fk))
        kmap = {s['id']: s for s in K['stores']}
        for r in K['rows']:
            it = K['items'].get(r[1]) or {}
            if it.get('b') != 'DESCENTE':
                continue
            st = style_of(r[1], it)
            reg = region_of(src, r[0], kmap.get(r[0], {}))
            if st and reg and r[3] > 0:
                stock[st][REG_KEY[reg]] += r[3]

    for st, o in old.items():
        o['qty'] = sum(x[4] for x in sales.get(st, []))
        o['fw'] = is_fw(st)
        o['yr'] = YEAR.get(st[1], 0)
        o['line'], o['it2'] = st[5], st[6:8]
        o['nn'] = norm_name(o['en'])
        o['g'] = o['gx'] or '中性'
    pool = [o for o in old.values() if o['qty'] >= 5]

    # ---------- 27FW 商品 ----------
    t = open(os.path.join(a.repo, 'data.js'), encoding='utf-8').read()
    items = json.loads(t[t.index('['):t.rindex(']') + 1])
    new = collections.OrderedDict()
    for i in items:
        s = new.setdefault(i['style'], {'style': i['style'], 'zh': i['zh'], 'en': i['en'], 'gen': i['gen'],
                                        'krw': i.get('krw') or i.get('price') or 0, 'div': i.get('div') or 'APP',
                                        'sheet': i['sheet'], 'cat': i.get('cat', ''), 'run': i.get('run')})

    ov = {}
    if a.override and os.path.exists(a.override):
        ov = load(a.override)

    by_code = {o['style'][0] + o['style'][2:]: o for o in pool}
    by_name = collections.defaultdict(list)
    for o in pool:
        if o['nn']:
            by_name[o['nn']].append(o)

    STOP = {'t', 'shirt', 'shirts', 'the', 'and', 'with', 'for', 's'}

    def sim(x, y):
        a_, b_ = set(norm_name(x).split()) - STOP, set(norm_name(y).split()) - STOP
        return len(a_ & b_) / len(a_ | b_) if a_ and b_ else 0

    def l1(n):
        hits = []
        o = by_code.get(n['style'][0] + n['style'][2:])
        if o and sim(n['en'], o['en']) >= 0.4:  # 同款號還要品名相近才算延續（韓國款號會跨年重用）
            hits.append(o)
        for o in by_name.get(norm_name(n['en']), []):
            if o not in hits:
                hits.append(o)
        hits.sort(key=lambda o: (-o['fw'], -o['yr'], -o['qty']))
        return hits[:2]

    # 價格換算：用 L1 配對算 台幣定價 / 韓幣
    ratios = [o['list'] / n['krw'] for n in new.values() for o in l1(n) if o['list'] and n['krw'] and n['krw'] < 900000]
    ratio = statistics.median(ratios) if ratios else 0.03
    print(f'L1 價格配對 {len(ratios)} 組，台幣/韓幣 中位數 {ratio:.4f}')

    def gmatch(n, o):
        return o['g'] == n['gen']

    def closest(n, cands, band):
        tgt = n['krw'] * ratio
        def dist(o):
            return abs(o['list'] - tgt) / tgt if tgt and o['list'] else 9
        c = [o for o in cands if dist(o) <= band] if band else cands
        c.sort(key=lambda o: (round(dist(o), 2), -o['yr'], -o['qty']))
        return c[:3]

    def match(n):
        s = n['style']
        if s in ov:
            return ('人工指定' if ov[s] else 'none'), [old[x] for x in ov[s] if x in old]
        h = l1(n)
        if h:
            return 'L1', h
        line, it2 = s[5], s[6:8]
        c = [o for o in pool if o['fw'] and o['line'] == line and o['it2'] == it2 and gmatch(n, o)]
        if c:
            return 'L2', closest(n, c, 0.3) or closest(n, c, 0)[:2]
        c = [o for o in pool if o['fw'] and o['it2'] == it2 and gmatch(n, o)]
        r = closest(n, c, 0.2)
        if r:
            return 'L3', r
        # 性別放寬：新款男／女可對中性舊款，新款中性可對任何性別
        c = [o for o in pool if o['fw'] and o['it2'] == it2 and (o['g'] == '中性' or n['gen'] == '中性')]
        r = closest(n, c, 0.2)
        if r:
            return 'L3', r
        return 'none', []

    TIER_NAME = {'L1': '同款延續', 'L2': '同系列同品類', 'L3': '同品類同價格帶', '人工指定': '人工指定', 'none': '無對照'}
    out, rows_x = {}, []
    for s, n in new.items():
        tier, refs = match(n)
        rec = {'t': tier, 'r': [[o['style'], o['en'] or o.get('zh', ''), o['season']] for o in refs], 'R': {}}
        rs = [o['style'] for o in refs]
        for rk in ('n', 'c', 's', 'a'):
            rows = [x for st in rs for x in sales.get(st, []) if rk == 'a' or x[0] == rk]
            pos = [x for x in rows if x[4] > 0]
            qty = sum(x[4] for x in rows)
            if qty < 5:
                rec['R'][rk] = None
                continue
            stores = {x[1] for x in pos}
            months = {x[2] for x in pos}
            stk = sum(stock[st][k] for st in rs for k in (('n', 'c', 's') if rk == 'a' else (rk,)))
            pq = sum(x[4] for x in pos)
            fp = sum(x[4] for x in pos if x[5]) / pq if pq else 0
            sz = collections.Counter()
            if n['run'] not in ('F',):
                for x in pos:
                    if x[3]:
                        lab = adapt_size(x[3], n['gen']) if n['div'] != 'FTW' else x[3]
                        if lab:
                            sz[lab] += x[4]
            szt = sum(sz.values())
            col = collections.Counter()
            for x in pos:
                if x[6]:
                    col[x[6]] += x[4]
            colt = sum(col.values())
            rec['R'][rk] = {
                'm': round(qty / max(len(stores), 1) / max(len(months), 1), 1),
                'st': round(qty / (qty + stk) * 100) if qty + stk > 0 else None,
                'fp': round(fp * 100),
                'k': len(stores),
                'sz': {z: round(v / szt * 100) for z, v in sz.items()} if szt >= 10 else None,
                'c': [[c, round(v / colt * 100)] for c, v in col.most_common() if v / colt >= 0.02] if colt >= 10 else None,
            }
        out[s] = rec
        A = rec['R'].get('a') or {}
        rows_x.append([s, n['zh'], n['en'], n['sheet'], n['cat'], n['gen'], TIER_NAME[tier],
                       '、'.join(x[0] for x in rec['r']), '／'.join(x[1] for x in rec['r']), '、'.join(x[2] for x in rec['r']),
                       A.get('m'), A.get('st'), A.get('fp'), A.get('k'),
                       *[(rec['R'].get(k) or {}).get('m') for k in ('n', 'c', 's')]])

    # 去年熱賣：L1／L2／人工指定，綜合店均月銷前 20%，且售罄率 ≥ 50%
    ms = sorted([v['R']['a']['m'] for v in out.values() if v['t'] in ('L1', 'L2', '人工指定') and v['R'].get('a')], reverse=True)
    cut = ms[max(int(len(ms) * 0.2) - 1, 0)] if ms else 999
    for v in out.values():
        A = v['R'].get('a')
        v['hot'] = 1 if (v['t'] in ('L1', 'L2', '人工指定') and A and A['m'] >= cut and (A['st'] or 0) >= 50) else 0

    def per(label):
        f, t_ = periods[label]
        return f'{f[:7].replace("-", "/")}–{t_[:7].replace("-", "/")}'
    meta = {
        'built': datetime.datetime.now().strftime('%Y-%m-%d'),
        'periods': {k: per(k) for k in periods},
        'stores': {k: len(v) for k, v in stores_by_reg.items()},
        'note': {
            'c': f'中部經銷（動力）只有 {per("動力")} 資料，還沒有 25FW 整季，數字以直營台中為主，僅供參考',
            's': f'南部經銷（雷根）只有 {per("雷根")} 資料，還沒有 25FW 整季，僅供參考',
        },
        'hotCut': cut,
    }
    pub = {'built': meta['built'], 'hotCut': cut}  # 公開檔不放體系名稱、期間與提醒文字
    with open(os.path.join(a.repo, 'ref.js'), 'w', encoding='utf-8') as f:
        f.write('// 過往銷售參考（tools/build_ref.py 產生，勿手改）。區域合計，不含店名與金額。\n')
        f.write('window.DSTC_REF=' + json.dumps({'meta': pub, 's': out}, ensure_ascii=False, separators=(',', ':')) + ';\n')
    cnt = collections.Counter(v['t'] for v in out.values())
    print('對照結果', dict(cnt), '熱賣', sum(v['hot'] for v in out.values()), '門檻', cut)

    if a.xlsx:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
        wb = Workbook(); ws = wb.active; ws.title = '對照表'
        hd = ['27FW 款號', '中文品名', '英文品名', '分頁', '品類', '性別', '對照層級', '對照舊款號', '舊款品名', '舊款季別',
              '綜合 店均月銷', '綜合 售罄率%', '綜合 全價比%', '綜合 店數', '北部 店均月銷', '中部 店均月銷', '南部 店均月銷']
        ws.append(hd)
        for c in ws[1]:
            c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='185FA5'); c.alignment = Alignment(wrap_text=True, vertical='center')
        fills = {'同款延續': 'E6F1FB', '同系列同品類': 'F1EFE8', '同品類同價格帶': 'FAEEDA', '無對照': 'FCEBEB'}
        for r in rows_x:
            ws.append(r)
            ws.cell(ws.max_row, 7).fill = PatternFill('solid', fgColor=fills.get(r[6], 'FFFFFF'))
        for col, w in zip('ABCDEFGHIJKLMNOPQ', [13, 26, 30, 18, 10, 6, 14, 26, 40, 12, 10, 10, 10, 8, 10, 10, 10]):
            ws.column_dimensions[col].width = w
        ws.freeze_panes = 'B2'; ws.auto_filter.ref = ws.dimensions
        n2 = wb.create_sheet('說明')
        for line in [
            '對照層級：同款延續＝同款號（去掉年份碼）或英文品名相同；同系列同品類＝系列碼＋品類碼＋性別相同的 FW 舊款，價格最接近；同品類同價格帶＝品類碼＋性別相同、價格 ±20%。',
            f'價格換算：台幣定價／韓幣 MSRP 中位數 {ratio:.4f}（由同款延續配對算出）。',
            '資料期間：' + '；'.join(f'{k} {v}' for k, v in meta['periods'].items()),
            '區域：直營依主檔區域；動力新竹巨城、中和環球＝北部，其餘門市＝中部；雷根大甲＝中部，其餘＝南部（天王暫列南部，目前無銷售）。',
            '排除：OUTLET、特賣、倉庫（直營林口三井 OUTLET／特賣、台中三井 OUTLET、雷根 SKM、動力管理處／倉庫）。',
            '店均月銷＝件數 ÷ 有賣的店數 ÷ 有賣的月數；售罄率＝銷售 ÷（銷售＋目前庫存）；全價比＝以 95 折以上賣出的件數比例。',
            '要改對照：在 tools/ref_override.json 填 {"27FW款號": ["舊款號", ...]}，空陣列＝無對照，重跑 build_ref.py。',
        ]:
            n2.append([line])
        n2.column_dimensions['A'].width = 140
        wb.save(a.xlsx)
        print('對照表', a.xlsx)


if __name__ == '__main__':
    main()
