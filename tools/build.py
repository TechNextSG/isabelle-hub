"""Build index.html from hub_data.py + pages.json.
python tools/build.py            (run tools/fetch_pages.py first to refresh the page lists,
                                  tools/thumbs.py to refresh the pictures)"""
import json, pathlib, html, datetime, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from hub_data import GROUPS, ITEMS

V = "1"
PAGES = json.loads((ROOT / "tools" / "pages.json").read_text(encoding="utf-8"))
e = lambda s: html.escape(s, quote=True)

ICON_EXT = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>'
ICON_LINK = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>'
ICON_Q = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'


def short_title(t, site):
    # "Upcoming TRE™ Workshops & Events | HummingBeing" -> drop the trailing brand
    for brand in (" | HummingBeing", " | BHD Asia", " | TRE™ in Singapore", " | TRE in Singapore", " · TRE™ in Singapore"):
        if t.endswith(brand): t = t[: -len(brand)]
    return t.strip() or site


def page_path(u):
    p = u.split("://", 1)[1]
    p = p[p.find("/"):] if "/" in p else "/"
    return p


def card(it, i):
    pages = PAGES.get(it.get("pages", ""), [])
    words = " ".join([it["title"], it["host"], it["desc"], it["status"], it["url"]])
    st_cls = "ix-st" + ("" if it["status"] == "Live" else " ix-st--preview")
    out = [f'<article class="ix-card" style="--i:{i}" data-words="{e(words)}">',
           f'<a class="ix-thumb" href="{e(it["url"])}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">',
           f'<img src="assets/img/thumbs/{it["slug"]}.jpg?v={V}" alt="" width="960" height="540" loading="lazy">',
           f'<img class="ix-thumb-2" src="assets/img/thumbs/{it["slug"]}-2.jpg?v={V}" alt="" width="960" height="540" loading="lazy" decoding="async">',
           f'<span class="{st_cls}">{e(it["status"])}</span></a>',
           '<div class="ix-body">',
           f'<p class="ix-meta">{e(it["host"])}</p>',
           f'<h3><a href="{e(it["url"])}" target="_blank" rel="noopener">{e(it["title"])}</a></h3>',
           f'<p class="ix-desc">{e(it["desc"])}</p>']
    if pages:
        lis = "".join(
            f'<li><a href="{e(p["url"])}" target="_blank" rel="noopener"><b>{e(short_title(p["title"], it["title"]))}</b><span>{e(page_path(p["url"]))}</span></a></li>'
            for p in pages)
        out.append(f'<details class="ix-pages"><summary>Every page <span class="ix-pc">{len(pages)} pages</span></summary><ol>{lis}</ol></details>')
    out += ['<div class="ix-acts">',
            f'<a class="ix-btn ix-btn--p" href="{e(it["url"])}" target="_blank" rel="noopener">{ICON_EXT}Open</a>',
            f'<button type="button" class="ix-btn ix-btn--t ix-copy" data-url="{e(it["url"])}">{ICON_LINK}<span class="ix-cl">Copy link</span></button>',
            '</div></div></article>']
    return "".join(out)


n_sites = sum(1 for it in ITEMS if it["g"] == "sites")
n_pages = sum(len(PAGES.get(it.get("pages", ""), [])) for it in ITEMS)
n_other = len(ITEMS) - n_sites

tabs = ['<button type="button" class="ix-tab" data-tab="all" aria-pressed="true">All <span>%d</span></button>' % len(ITEMS)]
sections = []
i = 0
for key, name, lead in GROUPS:
    its = [it for it in ITEMS if it["g"] == key]
    tabs.append(f'<button type="button" class="ix-tab" data-tab="{key}" aria-pressed="false">{e(name.split(" &")[0])} <span>{len(its)}</span></button>')
    cards = []
    for it in its:
        cards.append(card(it, i)); i += 1
    sections.append(f'<section class="ix-group" data-g="{key}" aria-labelledby="g-{key}"><header class="ix-gh"><h2 id="g-{key}">{e(name)}</h2>'
                    f'<span class="ix-n">{len(its)}</span><p>{e(lead)}</p></header><div class="ix-grid">{"".join(cards)}</div></section>')

today = datetime.date.today().strftime("%d %b %Y").lstrip("0")
doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="color-scheme" content="light">
<title>Isabelle's Websites &amp; Pages · TechNext</title>
<meta name="description" content="Every website and HTML page TechNext built for Isabelle Claus Teixeira: HummingBeing, BHD Asia, TRE in Singapore, event pages, brand kits and planning tools.">
<link rel="icon" href="assets/img/favicon-48.png" sizes="48x48">
<link rel="apple-touch-icon" href="assets/img/favicon-192.png">
<link rel="stylesheet" href="assets/fonts.css?v={V}">
<link rel="stylesheet" href="assets/hub.css?v={V}">
</head>
<body>
<header class="ix-hero">
  <div class="ix-wrap">
    <div class="ix-top"><span class="ix-logo"><img src="assets/img/logo-horizontal-white.png" alt="TechNext" width="160" height="32"></span><span class="ix-for">Website compilation</span></div>
    <div class="ix-hero-row">
      <div>
        <p class="ix-kicker">Isabelle Claus Teixeira</p>
        <h1>Every website and page, <span>in one place</span></h1>
        <p class="ix-lead">HummingBeing, BHD Asia and TRE™ in Singapore with all their pages, plus the event pages, brand kits and planning tools we built.</p>
      </div>
      <dl class="ix-stats">
        <div><dt>Websites</dt><dd>{n_sites}</dd></div>
        <div><dt>Web pages</dt><dd>{n_pages}</dd></div>
        <div><dt>Other HTML</dt><dd>{n_other}</dd></div>
      </dl>
    </div>
  </div>
</header>
<main class="ix-wrap">
  <div class="ix-bar" role="search">
    <label class="ix-q">{ICON_Q}<span class="sr" hidden>Search</span><input id="q" type="search" placeholder="Search sites and pages" aria-label="Search websites and pages" autocomplete="off"></label>
    <div class="ix-tabs" role="group" aria-label="Show">{"".join(tabs)}</div>
  </div>
  <div class="ix-results">{"".join(sections)}
    <div class="ix-empty" id="empty" hidden><b>Nothing matches that search</b><p>Try a page name like “events” or a site like “BHD”.</p></div>
  </div>
</main>
<footer class="ix-foot"><div class="ix-wrap"><span>Compiled by TechNext for Isabelle Claus Teixeira</span><span>Updated {today}</span></div></footer>
<script src="assets/hub.js?v={V}" defer></script>
</body>
</html>
"""
(ROOT / "index.html").write_text(doc, encoding="utf-8")
(ROOT / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
print("built index.html:", len(ITEMS), "cards,", n_pages, "pages")
