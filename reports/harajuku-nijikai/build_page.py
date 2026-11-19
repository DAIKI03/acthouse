#!/usr/bin/env python3
"""Build the shareable comparison page from venues.json.

Usage: python3 build_page.py venues.json out/index.html
"""
import json
import math
import sys
from html import escape


def e(s):
    return escape(str(s if s is not None else ""), quote=True)


MARK_LABEL = {
    "distance": "距離",
    "seat": "全員着席",
    "room": "個室・貸切",
    "budget": "予算",
    "mood": "雰囲気",
}
MARK_CLASS = {"◎": "m-best", "○": "m-ok", "△": "m-weak", "×": "m-ng", "？": "m-ask"}


def pill(text, kind="neutral"):
    return f'<span class="pill pill-{e(kind)}">{e(text)}</span>'


def marks_html(marks):
    cells = []
    for key, label in MARK_LABEL.items():
        m = marks.get(key, "？")
        cells.append(
            f'<span class="mark {MARK_CLASS.get(m, "m-ask")}">'
            f'<span class="mark-k">{e(label)}</span><span class="mark-v">{e(m)}</span></span>'
        )
    return '<div class="marks">' + "".join(cells) + "</div>"


def links_html(links, phone):
    parts = []
    for ln in links or []:
        parts.append(f'<a href="{e(ln["url"])}" rel="noopener">{e(ln["label"])}</a>')
    if phone:
        parts.append(f'<span class="tel">TEL {e(phone)}</span>')
    return '<div class="links">' + "".join(parts) + "</div>"


def map_svg(data):
    """Schematic straight-line map centred on the first-party venue."""
    o = data["origin"]
    lat0, lon0 = o["lat"], o["lon"]
    m_per_deg_lat = 111_000
    m_per_deg_lon = 111_000 * math.cos(math.radians(lat0))
    size, pad = 560, 20
    radius_m = 650
    scale = (size / 2 - pad) / radius_m
    cx = cy = size / 2

    def xy(lat, lon):
        dx = (lon - lon0) * m_per_deg_lon
        dy = (lat - lat0) * m_per_deg_lat
        return cx + dx * scale, cy - dy * scale

    out = [
        f'<svg viewBox="0 0 {size} {size}" role="img" aria-labelledby="map-title map-desc" class="map">',
        '<title id="map-title">原宿しずると候補店の位置関係</title>',
        '<desc id="map-desc">原宿しずるを中心に、直線200m・400m・600mの円と、候補店と駅の位置を示した略図。</desc>',
    ]
    for r in (200, 400, 600):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*scale:.1f}" class="ring"/>')
        out.append(f'<text x="{cx + 4}" y="{cy - r*scale - 4:.1f}" class="ring-label">直線{r}m</text>')
    out.append(f'<text x="{size - pad}" y="{pad + 6}" class="north" text-anchor="end">↑ 北</text>')
    for lm in data.get("landmarks", []):
        x, y = xy(lm["lat"], lm["lon"])
        out.append(f'<rect x="{x-5:.1f}" y="{y-5:.1f}" width="10" height="10" class="station"/>')
        anchor = lm.get("anchor", "start")
        dx = 9 if anchor == "start" else -9
        dy = lm.get("dy", 4)
        out.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" class="station-label" text-anchor="{anchor}">{e(lm["name"])}</text>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="7" class="origin"/>')
    out.append(f'<text x="{cx+11}" y="{cy+5}" class="origin-label">原宿しずる（一次会）</text>')
    placed = []
    for v in sorted(data["venues"], key=lambda v: v["rank"]):
        if v.get("lat") is None or v.get("lon") is None:
            continue
        x, y = xy(v["lat"], v["lon"])
        # Venues in the same building: spread the pins sideways so both numbers stay readable.
        same = [p for p in placed if abs(p[0] - x) < 1 and abs(p[1] - y) < 1]
        x_draw = x + 24 * len(same)
        placed.append((x, y))
        top = " top" if v["rank"] in data.get("top3", []) else ""
        out.append(f'<g class="pin{top}"><circle cx="{x_draw:.1f}" cy="{y:.1f}" r="11"/>'
                   f'<text x="{x_draw:.1f}" y="{y+4:.1f}" text-anchor="middle">{v["rank"]}</text></g>')
    out.append("</svg>")
    return "".join(out)


def build(data):
    venues = sorted(data["venues"], key=lambda v: v["rank"])
    by_rank = {v["rank"]: v for v in venues}
    top3 = [by_rank[r] for r in data.get("top3", []) if r in by_rank]

    summary = "".join(f"<li>{e(s)}</li>" for s in data.get("summary", []))

    top_cards = []
    for i, v in enumerate(top3, 1):
        top_cards.append(f"""
<article class="pick">
  <p class="pick-no">おすすめ {i} ・ ランキング{v['rank']}位</p>
  <h3><a href="#v{v['rank']}">{e(v['name'])}</a></h3>
  <p class="pick-genre">{e(v['genre'])}</p>
  <p class="pick-key"><strong>徒歩{e(v['walk_label'])}</strong> ・ {e(v['seat_short'])}</p>
  <p class="pick-key">{e(v['price_short'])}</p>
  <p class="pick-why">{e(v.get('top3_reason', ''))}</p>
</article>""")
    backup = data.get("backup")
    if backup:
        bv = by_rank[backup["rank"]]
        top_cards.append(f"""
<article class="pick pick-backup">
  <p class="pick-no">保険 ・ ランキング{bv['rank']}位</p>
  <h3><a href="#v{bv['rank']}">{e(bv['name'])}</a></h3>
  <p class="pick-genre">{e(bv['genre'])}</p>
  <p class="pick-key"><strong>徒歩{e(bv['walk_label'])}</strong> ・ {e(bv['seat_short'])}</p>
  <p class="pick-key">{e(bv['price_short'])}</p>
  <p class="pick-why">{e(backup['reason'])}</p>
</article>""")

    rows = []
    for v in venues:
        rows.append(f"""
<tr>
  <td class="num">{v['rank']}</td>
  <td><a href="#v{v['rank']}" class="tname">{e(v['name'])}</a><span class="tgenre">{e(v['genre'])}</span></td>
  <td class="nowrap">{e(v['walk_label'])}</td>
  <td>{e(v['seat_short'])}</td>
  <td>{e(v['price_short'])}</td>
  <td>{e(v['hours_short'])}</td>
  <td>{e(v['dec17_short'])}</td>
  <td>{marks_html(v.get('marks', {}))}</td>
</tr>""")

    details = []
    for v in venues:
        pills = "".join(pill(p["text"], p.get("kind", "neutral")) for p in v.get("pills", []))
        pros = "".join(f"<li>{e(x)}</li>" for x in v.get("pros", []))
        cons = "".join(f"<li>{e(x)}</li>" for x in v.get("cons", []))
        ask = "".join(f"<li>{e(x)}</li>" for x in v.get("ask", []))
        items = [
            ("1. 店名・住所", f"{e(v['name'])}<br>{e(v['address'])}"),
            ("2. 原宿しずるから", e(v["walk_detail"])),
            ("3. 雰囲気・写真", e(v["atmosphere"])),
            ("4. 営業時間・21時以降", e(v["hours"])),
            ("5. 15〜20名の着席", e(v["seating"])),
            ("6. 個室・貸切", e(v["private"])),
            ("7. 料金・飲み放題", e(v["price"])),
            ("8. 12/17(木)の予約", e(v["dec17"])),
            ("9. 公式・予約・電話", links_html(v.get("links"), v.get("phone"))),
        ]
        dl = "".join(f"<div><dt>{k}</dt><dd>{val}</dd></div>" for k, val in items)
        details.append(f"""
<article class="venue" id="v{v['rank']}">
  <header class="venue-head">
    <span class="rank">{v['rank']}</span>
    <div>
      <h3>{e(v['name'])}</h3>
      <p class="venue-genre">{e(v['genre'])} ・ 徒歩{e(v['walk_label'])}</p>
    </div>
  </header>
  <div class="pills">{pills}</div>
  <dl class="facts-dl">{dl}</dl>
  <div class="procon">
    <div><h4>メリット</h4><ul>{pros}</ul></div>
    <div><h4>デメリット・未確認点</h4><ul>{cons}</ul></div>
  </div>
  <div class="ask"><h4>電話で聞くこと</h4><ol>{ask}</ol></div>
</article>""")

    decision = "".join(
        f"<tr><td>{e(d['if'])}</td><td>{e(d['then'])}</td><td>{e(d['cost'])}</td></tr>"
        for d in data.get("decision", [])
    )
    schedule = "".join(
        f'<li><span class="sch-date">{e(s["date"])}</span><span class="sch-todo">{e(s["todo"])}</span>'
        f'<span class="sch-note">{e(s.get("note", ""))}</span></li>'
        for s in data.get("schedule", [])
    )
    checklist = "".join(
        f'<li><span class="ck-title">{e(c["title"])}</span><span class="ck-detail">{e(c["detail"])}</span></li>'
        for c in data.get("checklist", [])
    )
    notes = "".join(f"<li>{e(n)}</li>" for n in data.get("notes", []))
    excluded_rows = "".join(
        f'<tr><td>{e(x["name"])}</td><td class="nowrap">{e(x["walk"])}</td><td>{e(x["reason"])}</td></tr>'
        for x in data.get("excluded", [])
    )
    sources = "".join(
        f'<li><a href="{e(s["url"])}" rel="noopener">{e(s["label"])}</a></li>' for s in data.get("sources", [])
    )

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(data['title'])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Shippori+Mincho:wght@600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header class="masthead">
  <div class="wrap">
    <p class="eyebrow">二次会の会場候補 ・ {e(data['asof_label'])}</p>
    <h1>{e(data['title'])}</h1>
    <p class="lede">{e(data['lede'])}</p>
    <ul class="conds">
      <li><span>日時</span>2026年12月17日(木) 21:00頃から約2時間</li>
      <li><span>人数</span>15〜20名、全員着席</li>
      <li><span>予算</span>1人3,000〜5,000円（雰囲気を優先し、多少の超過は可）</li>
      <li><span>距離</span>原宿しずるから徒歩5分以内を優先、最大10分</li>
    </ul>
  </div>
</header>
<main class="wrap">
  <section id="summary" aria-labelledby="h-summary">
    <h2 id="h-summary">結論</h2>
    <ul class="summary">{summary}</ul>
  </section>

  <section id="picks" aria-labelledby="h-picks">
    <h2 id="h-picks">特におすすめの3店と保険</h2>
    <div class="picks">{''.join(top_cards)}</div>
  </section>

  <section id="ranking" aria-labelledby="h-ranking">
    <h2 id="h-ranking">候補ランキング（条件との一致度順）</h2>
    <p class="section-note">{e(data.get('ranking_note', ''))}</p>
    <div class="table-wrap">
      <table class="rank-table">
        <thead><tr><th>順位</th><th>店名</th><th>徒歩</th><th>席・個室/貸切</th><th>1人あたり</th><th>営業（木）</th><th>12/17</th><th>条件との一致</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
    <p class="legend">一致の記号：◎ 十分に満たす　○ 満たす　△ 条件付き・一部のみ　× 満たさない　？ 要問い合わせ</p>
  </section>

  <section id="map-section" aria-labelledby="h-map">
    <h2 id="h-map">位置関係</h2>
    <div class="map-box">{map_svg(data)}
      <p class="map-note">直線距離の略図です。徒歩分数は、実際の道のりを80m＝1分で換算した表の値を見てください。番号はランキングの順位、塗りつぶしの印がおすすめ3店です。2位と4位は同じビル（3階と地下1階）です。</p>
    </div>
  </section>

  <section id="details" aria-labelledby="h-details">
    <h2 id="h-details">各店の詳細</h2>
    <div class="venues">{''.join(details)}</div>
  </section>

  <section id="decide" aria-labelledby="h-decide">
    <h2 id="h-decide">電話の結果で決める</h2>
    <div class="table-wrap">
      <table class="plain-table">
        <thead><tr><th>電話で分かったこと</th><th>次の一手</th><th>1人あたりの目安</th></tr></thead>
        <tbody>{decision}</tbody>
      </table>
    </div>
  </section>

  <section id="schedule" aria-labelledby="h-schedule">
    <h2 id="h-schedule">予約までの段取り</h2>
    <ol class="schedule">{schedule}</ol>
  </section>

  <section id="checklist" aria-labelledby="h-check">
    <h2 id="h-check">予約するときに必ず確認すること</h2>
    <ol class="check">{checklist}</ol>
  </section>

  <section id="about" aria-labelledby="h-about">
    <h2 id="h-about">調査について</h2>
    <ul class="notes">{notes}</ul>
    <h3 class="sub">検討したが外した店</h3>
    <div class="table-wrap">
      <table class="plain-table">
        <thead><tr><th>店名</th><th>徒歩</th><th>外した理由</th></tr></thead>
        <tbody>{excluded_rows}</tbody>
      </table>
    </div>
    <h3 class="sub">主な出典</h3>
    <ul class="sources">{sources}</ul>
  </section>
</main>
<footer class="wrap foot">
  <p>{e(data.get('footer', ''))}</p>
</footer>
</body>
</html>
"""


CSS = r"""
:root {
  /* Night-bar palette: ink navy on cool paper with a brass accent. Layout: one reading column; cards for picks and venues; wide tables scroll inside their own box. */
  --bg: #f3f4f6;
  --surface: #ffffff;
  --ink: #161b26;
  --muted: #566071;
  --line: #d8dce4;
  --accent: #8a5d14;
  --accent-soft: #f4ead8;
  --ok: #1f6f4f;
  --warn: #9a4f00;
  --ng: #a3262a;
  --ask: #5c6474;
  --font-display: "Shippori Mincho", "Hiragino Mincho ProN", "Yu Mincho", serif;
  --font-body: "Noto Sans JP", "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", sans-serif;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #11141b;
    --surface: #191e28;
    --ink: #e9eaee;
    --muted: #a3aab8;
    --line: #2b3242;
    --accent: #d9ad5f;
    --accent-soft: #2c2618;
    --ok: #6cc59a;
    --warn: #f0a656;
    --ng: #f08a8d;
    --ask: #a3aab8;
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg: #11141b;
  --surface: #191e28;
  --ink: #e9eaee;
  --muted: #a3aab8;
  --line: #2b3242;
  --accent: #d9ad5f;
  --accent-soft: #2c2618;
  --ok: #6cc59a;
  --warn: #f0a656;
  --ng: #f08a8d;
  --ask: #a3aab8;
  color-scheme: dark;
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.75;
}
a { color: var(--accent); text-underline-offset: 3px; }
a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 2px; }
.wrap { max-width: 1080px; margin: 0 auto; padding: 0 20px; }
h1, h2, h3 { font-family: var(--font-display); text-wrap: balance; line-height: 1.35; margin: 0; }
h1 { font-size: clamp(1.9rem, 4.5vw, 2.6rem); letter-spacing: 0.02em; }
h2 { font-size: 1.45rem; margin-bottom: 14px; padding-bottom: 8px; border-bottom: 1px solid var(--line); }
h3 { font-size: 1.15rem; }
h4 { font-size: 0.9rem; margin: 0 0 6px; color: var(--muted); font-weight: 700; }
.masthead { padding: 40px 0 28px; border-bottom: 1px solid var(--line); background: var(--surface); }
.masthead .wrap { display: grid; gap: 12px; }
.eyebrow { margin: 0; color: var(--accent); font-size: 0.85rem; letter-spacing: 0.08em; font-weight: 500; }
.lede { margin: 0; max-width: 46em; color: var(--muted); }
.conds { list-style: none; padding: 0; margin: 8px 0 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 8px 16px; }
.conds li { display: grid; gap: 2px; padding: 10px 12px; border: 1px solid var(--line); border-radius: 8px; background: var(--bg); font-size: 0.93rem; }
.conds span { font-size: 0.75rem; color: var(--muted); letter-spacing: 0.06em; }
main section { padding: 34px 0 6px; }
.summary { margin: 0; padding: 16px 18px 16px 2.2em; background: var(--surface); border: 1px solid var(--line); border-left: 4px solid var(--accent); border-radius: 8px; display: grid; gap: 8px; max-width: 62em; }
.section-note, .legend, .map-note { color: var(--muted); font-size: 0.88rem; margin: 6px 0 0; max-width: 62em; }
.section-note { margin: 0 0 12px; }
.picks { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }
.pick { background: var(--surface); border: 1px solid var(--line); border-top: 3px solid var(--accent); border-radius: 8px; padding: 16px 18px; display: grid; gap: 6px; align-content: start; }
.pick-backup { border-top-color: var(--muted); }
.pick-no { margin: 0; font-size: 0.8rem; color: var(--accent); font-weight: 700; letter-spacing: 0.04em; }
.pick-backup .pick-no { color: var(--muted); }
.pick h3 a { color: var(--ink); text-decoration: none; }
.pick h3 a:hover { text-decoration: underline; }
.pick-genre, .venue-genre, .tgenre { margin: 0; color: var(--muted); font-size: 0.85rem; }
.pick-key { margin: 0; font-size: 0.92rem; }
.pick-why { margin: 4px 0 0; font-size: 0.92rem; padding-top: 8px; border-top: 1px dashed var(--line); }
.table-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); }
table { border-collapse: collapse; width: 100%; font-size: 0.88rem; }
.rank-table { min-width: 1000px; }
.plain-table { min-width: 640px; }
th, td { text-align: left; vertical-align: top; padding: 10px 12px; border-bottom: 1px solid var(--line); }
thead th { font-size: 0.78rem; color: var(--muted); font-weight: 500; letter-spacing: 0.04em; background: var(--bg); }
tbody tr:last-child td { border-bottom: 0; }
td.num { font-variant-numeric: tabular-nums; font-weight: 700; color: var(--accent); }
.nowrap { white-space: nowrap; }
.tname { font-weight: 700; color: var(--ink); text-decoration: none; display: block; }
.tname:hover { text-decoration: underline; }
.tgenre { display: block; }
.marks { display: flex; flex-wrap: wrap; gap: 4px; min-width: 230px; }
.mark { display: inline-flex; align-items: center; gap: 4px; border: 1px solid var(--line); border-radius: 999px; padding: 0 8px; font-size: 0.75rem; white-space: nowrap; }
.mark-k { color: var(--muted); }
.mark-v { font-weight: 700; }
.m-best .mark-v, .m-ok .mark-v { color: var(--ok); }
.m-weak .mark-v { color: var(--warn); }
.m-ng .mark-v { color: var(--ng); }
.m-ask .mark-v { color: var(--ask); }
.map-box { display: grid; gap: 8px; justify-items: start; }
.map { width: 100%; max-width: 560px; height: auto; background: var(--surface); border: 1px solid var(--line); border-radius: 8px; }
.map .ring { fill: none; stroke: var(--line); stroke-width: 1.5; stroke-dasharray: 5 5; }
.map .ring-label, .map .north { fill: var(--muted); font-size: 12px; font-family: var(--font-body); }
.map .station { fill: var(--surface); stroke: var(--muted); stroke-width: 1.5; }
.map .station-label { fill: var(--muted); font-size: 12px; font-family: var(--font-body); }
.map .origin { fill: var(--ink); }
.map .origin-label { fill: var(--ink); font-size: 13px; font-weight: 700; font-family: var(--font-body); }
.map .pin circle { fill: var(--surface); stroke: var(--accent); stroke-width: 2; }
.map .pin text { fill: var(--accent); font-size: 12px; font-weight: 700; font-family: var(--font-body); }
.map .pin.top circle { fill: var(--accent); }
.map .pin.top text { fill: var(--surface); }
.venues { display: grid; gap: 18px; }
.venue { background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 18px 20px; display: grid; gap: 12px; scroll-margin-top: 16px; }
.venue-head { display: flex; gap: 14px; align-items: center; }
.rank { flex: none; width: 40px; height: 40px; border-radius: 50%; display: grid; place-items: center; background: var(--accent-soft); color: var(--accent); font-weight: 700; font-variant-numeric: tabular-nums; }
.pills { display: flex; flex-wrap: wrap; gap: 6px; }
.pill { font-size: 0.78rem; padding: 2px 10px; border-radius: 999px; border: 1px solid var(--line); color: var(--muted); }
.pill-ok { border-color: var(--ok); color: var(--ok); }
.pill-warn { border-color: var(--warn); color: var(--warn); }
.pill-ng { border-color: var(--ng); color: var(--ng); }
.pill-accent { border-color: var(--accent); color: var(--accent); }
.facts-dl { margin: 0; display: grid; border-top: 1px solid var(--line); }
.facts-dl > div { display: grid; grid-template-columns: 11.5em 1fr; gap: 12px; padding: 9px 0; border-bottom: 1px solid var(--line); }
.facts-dl dt { color: var(--muted); font-size: 0.85rem; }
.facts-dl dd { margin: 0; font-size: 0.93rem; overflow-wrap: anywhere; }
.links { display: flex; flex-wrap: wrap; gap: 6px 14px; align-items: baseline; }
.tel { font-variant-numeric: tabular-nums; font-weight: 500; }
.procon { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px 24px; }
.procon ul, .ask ol { margin: 0; padding-left: 1.3em; font-size: 0.92rem; }
.ask { background: var(--bg); border-radius: 6px; padding: 12px 14px; }
.schedule { list-style: none; margin: 0; padding: 0; display: grid; gap: 0; max-width: 62em; border-left: 2px solid var(--accent); }
.schedule li { display: grid; grid-template-columns: 9.5em 1fr; gap: 2px 16px; padding: 10px 0 10px 16px; border-bottom: 1px solid var(--line); }
.sch-date { font-weight: 700; font-variant-numeric: tabular-nums; grid-row: span 2; }
.sch-todo { font-size: 0.95rem; }
.sch-note { color: var(--muted); font-size: 0.85rem; }
.check { margin: 0; padding-left: 1.4em; display: grid; gap: 10px; max-width: 62em; }
.check li { padding-left: 4px; }
.ck-title { font-weight: 700; display: block; }
.ck-detail { color: var(--muted); font-size: 0.92rem; display: block; }
.notes, .sources { margin: 0; padding-left: 1.2em; font-size: 0.9rem; display: grid; gap: 4px; max-width: 62em; }
.sources { overflow-wrap: anywhere; }
h3.sub { font-size: 1rem; margin: 22px 0 8px; }
.foot { padding: 30px 20px 40px; color: var(--muted); font-size: 0.82rem; }
@media (max-width: 560px) {
  .facts-dl > div, .schedule li { grid-template-columns: 1fr; }
  .sch-date { grid-row: auto; }
  .masthead { padding-top: 28px; }
}
@media (prefers-reduced-motion: reduce) {
  * { scroll-behavior: auto !important; transition: none !important; animation: none !important; }
}
"""


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    html_out = build(data)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"wrote {dst} ({len(html_out):,} bytes)")
