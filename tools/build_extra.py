"""Builds pipeline.html (visual flowcharts of how work for Isabelle's 3 sites runs + the Claude skills/tools) and
links.html (every link made for Isabelle, from qa/ihub-links/links.json).  python tools/build_extra.py
Owner ask 8 Nov 2026: "html of compilation of pipeline, claude skills, in visual html flowchart, also include all links
i created for isabelle ... focus on hummingbeing, bhdasia and tre singapore. properly arrange everything." """
import json, html, re, datetime as dt
from pathlib import Path
R = Path(__file__).resolve().parents[1]
SRC = Path.home() / 'ClaudeWork/qa/ihub-links/links.json'
V = '20261108a'
e = html.escape


def head(title, desc, cur):
    nav = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}</a>'
                  for h, t in (('./', 'All websites &amp; pages'), ('pipeline.html', 'How it works (pipeline)'), ('links.html', 'Every link')))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><meta name="color-scheme" content="light">
<title>{title} · Isabelle · TechNext</title><meta name="description" content="{desc}">
<link rel="icon" href="assets/img/favicon-48.png" sizes="48x48">
<link rel="stylesheet" href="assets/fonts.css?v=1"><link rel="stylesheet" href="assets/hub.css?v=1"><link rel="stylesheet" href="assets/pages.css?v={V}">
</head><body>
<header class="ix-hero"><div class="ix-wrap">
<div class="ix-top"><span class="ix-logo"><img src="assets/img/logo-horizontal-white.png" alt="TechNext" width="160" height="32"></span><span class="ix-for">Isabelle Claus Teixeira</span></div>
<div class="ix-hero-row"><div><p class="ix-kicker">HummingBeing · BHD Asia · TRE&trade; in Singapore</p>
<h1>{title}</h1><p class="ix-lead">{desc}</p></div></div>
<nav class="pg-nav" aria-label="Hub pages">{nav}</nav></div></header>
<main class="ix-wrap">"""


FOOT = '<p style="margin:60px 0 40px;font-size:13px;color:var(--muted)">Unlisted page for Isabelle and the TechNext team · updated %s</p></main></body></html>'


def tags(*t):
    return '<div class="tg">' + ''.join(f'<span class="{c}">{x}</span>' for c, x in t) + '</div>'


def node(title, text, tg='', cls=''):
    return f'<div class="nd {cls}"><b>{title}</b><p>{text}</p>{tg}</div>'


def flow(rows):
    return '<div class="fl">' + ''.join(f'<div class="fl-row" style="--n:{len(r)}">' + ''.join(r) + '</div>' for r in rows) + '</div>'


S3 = tags(('hb', 'HummingBeing'), ('bhd', 'BHD Asia'), ('tre', 'TRE SG'))
LEGEND = ('<div class="fl-legend"><span><i></i>Step Claude does</span><span><i class="g"></i>Check that must pass</span>'
          '<span><i class="o"></i>Owner decides (never automatic)</span></div>')


def pipeline():
    new_event = flow([
        [node('Request from Isabelle', 'Her doc in the NEW REQUESTS Drive folder or a WhatsApp message. Every date, price, CCE and title is copied word for word.'),
         node('Facts + brand check', 'TRE&trade; never &reg;; contact bonjour@bhdasia.com (hidden from bots); discount codes never shown; Simba = Living with the Spirit logo.', tags(('gate', 'rules')), 'is-gate'),
         node('Event page on all 3 sites', 'Newest page format copied. Card, home strip, search data (JSON-LD), chatbot, llms.txt, sitemap. TRE page built by <code>_src/build.py</code>.', S3),
         node('Test + push live', 'Rendered in Chrome: no errors, right dates, countdown. Pushed to all 3 sites; every new link checked live (200).', tags(('gate', 'live check')), 'is-gate')],
        [node('Event kit (one command)', '<code>event_kit.py events/&lt;key&gt;.json --all</code> makes the 16:9 thumbnail, 4:5 poster with QR and 4 social posts, plus captions.', tags(('auto', 'automatic'))),
         node('Layout audit', 'Text fit, nothing under the footer, faces not covered, no hard cut-out edge. Contact sheet checked by eye.', tags(('gate', 'audit')), 'is-gate'),
         node('Drive delivery', '07. Event Images (auto) folders + My Drive &ldquo;&lt;Person&gt; Branding&rdquo; with running post numbers; md5-checked.', tags(('auto', 'automatic'))),
         node('Posting schedule', '5 posts &ldquo;To set up&rdquo; before the next session: poster first, &ldquo;who it is for&rdquo; one week before. Schedule rules applied.', tags(('auto', 'automatic')))],
        [node('Coverage gate', '<code>event_coverage.py</code>: every upcoming event must have materials + a schedule. Runs automatically after every <code>git push</code>.', tags(('gate', 'hook')), 'is-gate'),
         node('Buffer (owner GO)', 'A dry run shows exactly what would be queued. Nothing goes to Buffer until the owner says GO.', tags(('', 'owner')), 'is-owner'),
         node('Live on social', 'Facebook, Instagram, LinkedIn at the planned times. TRE site also drafts a preview blog post for approval.', tags(('', 'published')))],
    ])
    change = flow([
        [node('Change request', 'Example 7 Nov 2026: Module 1 moved to 24&ndash;25 Apr 2027, group session 5 May, early bird to 31 Mar.'),
         node('Sweep all 3 sites', 'Scripted find-and-replace over pages, search data, chatbots, llms.txt; dry run first, then zero old values must remain.', S3),
         node('Artwork patch', 'Posters/thumbnails redrawn with only the changed text, in the original fonts; a self-check re-draws the old text to prove the match.'),
         node('Social posts + plan', 'Affected posts re-rendered from their own builders; captions fixed; plan dates moved by the rules.')],
        [node('Buffer dry run', 'Lists every queued post, caption line and move. Backups taken before any edit.', tags(('gate', 'dry run')), 'is-gate'),
         node('Owner GO', 'Only after the owner says GO are Buffer posts edited.', tags(('', 'owner')), 'is-owner'),
         node('Verify live', 'Live pages show the new facts (0 old values), image checksums match, Buffer re-read shows 0 differences.', tags(('gate', 'live check')), 'is-gate')],
    ])
    sites = [('HummingBeing', 'https://hummingbeing.com/', '#F5A623', [('Repo', 'technextsg/hummingbeing-website · main'), ('Hosting', 'Vercel (auto-deploy on push)'), ('Pages', 'event-*.html (.ce layout), clean URLs'), ('Data', 'events.html cards (data-start), scripts.js chatbot, llms.txt'), ('Cache', 'scripts.js?v=…')]),
             ('BHD Asia', 'https://bhdasia.com/', '#1E4691', [('Repo', 'TechNextSG/BHDasia · master'), ('Hosting', 'GitHub Pages'), ('Pages', 'event-*.html (.evt-hero)'), ('Data', 'shared.js EVENTS (countdowns, sold-out) + chatbot, llms.txt'), ('Cache', 'shared.js?v=…')]),
             ('TRE&trade; in Singapore', 'https://tre-in-singapore.com/', '#137A4A', [('Repo', 'technextmarketing/tre-singapore · main'), ('Hosting', 'GitHub Pages via Actions + nightly rebuild'), ('Pages', 'generated by _src/build.py (events/&lt;slug&gt;, packages, blog)'), ('Data', 'assets/js/events-data.js, facilitators-data.js'), ('Images', '_src/images.py: 480/960 WebP + AVIF')])]
    site_html = '<div class="sites3">' + ''.join(
        f'<div class="site" style="--c:{c}"><h3>{n}</h3><a class="u" href="{u}">{u.split("//")[1].rstrip("/")}</a><dl>'
        + ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows) + '</dl></div>' for n, u, c, rows in sites) + '</div>'
    SK = [
        ('Claude skill', 'isabelle-new-event', 'The full new-event workflow: pages on all 3 sites, then the event kit and schedule, then the coverage gate. Triggers on any new event request.'),
        ('Tool', 'event_kit.py', 'One command per event: thumbnail, poster, 4 social posts, captions, Drive delivery, 5 schedule rows, push + tracker refresh.'),
        ('Tool', 'new_event.py · social.py', 'The site-card / poster renderer and the 4:5 social post design (HummingBeing card style, cut-out trainers, partner logos).'),
        ('Gate + hook', 'event_coverage.py', 'Lists upcoming events on hummingbeing.com and fails if any has no materials or schedule. A Claude Code hook runs it after every git push.'),
        ('Tool', 'Schedule plan (fix.py · check.py · build.py)', 'Owner rules: next event daily, others weekends, max 2 a day (AM/PM). New events register in events_registry.json.'),
        ('Tool', 'swap_dates.py · patch.py', 'Change requests: dry-run sweeps across the 3 repos; in-place artwork date patches with a font-match self-check.'),
        ('Tool', 'sync_cert.py (Buffer)', 'Buffer sync with dry run, per-post backups and a re-read check. Runs only after the owner says GO.'),
        ('Tool', 'TRE _src/build.py', 'Builds every TRE page from the data files: clean URLs, search data, sitemap, image variants, blog drafts.'),
        ('Claude skills used', 'impeccable · hero-section-design · web-design-engineer', 'Design audits and page polish on the three sites (layout, contrast, clipped titles).'),
        ('Audit', 'AUDIT_BRIEF (events_list)', 'Per-site audit brief: facts vs sources, past events not selling, links, layout at 390/768/1440, SEO basics.'),
    ]
    sk = '<div class="skills">' + ''.join(f'<div class="sk"><span class="k">{k}</span><h3>{n}</h3><p>{d}</p></div>' for k, n, d in SK) + '</div>'
    body = (head('How the work runs', 'Visual pipeline for HummingBeing, BHD Asia and TRE&trade; in Singapore: from Isabelle&rsquo;s request to live pages, marketing materials and the posting schedule.', 'pipeline.html')
            + '<section class="pg-sec"><h2>New event: pages, materials and schedule</h2><p class="pg-lead">Owner rule (8 Nov 2026): every new event automatically gets its marketing materials and a posting schedule. Nothing is posted to social media without the owner&rsquo;s GO.</p>'
            + '<div class="pg-card">' + new_event + LEGEND + '</div></section>'
            + '<section class="pg-sec"><h2>Change request: dates, prices, wording</h2><p class="pg-lead">The same facts live in many places (pages, search data, chatbots, posters, social posts, Buffer). This flow keeps them identical everywhere.</p>'
            + '<div class="pg-card">' + change + LEGEND + '</div></section>'
            + '<section class="pg-sec"><h2>The three websites</h2><p class="pg-lead">Where each site lives and what drives its event listings.</p>' + site_html + '</section>'
            + '<section class="pg-sec"><h2>Claude skills and tools</h2><p class="pg-lead">What runs each step. All tools live on the TechNext work PC (ClaudeWork); the skill is in Claude Code.</p>' + sk + '</section>'
            + FOOT % dt.date.today().strftime('%d %b %Y'))
    (R / 'pipeline.html').write_text(body, encoding='utf-8')


SITE = {'hb': ('hb', 'HummingBeing'), 'bhd': ('bhd', 'BHD Asia'), 'tre': ('tre', 'TRE SG'), 'all': ('', 'All sites')}


def links():
    d = json.loads(SRC.read_text(encoding='utf-8'))
    groups = []
    for g in d['groups']:
        items = [i for i in g['items'] if 'PUBLIC' not in (i.get('note') or '')]   # internal files being taken off bhdasia.com
        if items: groups.append((g, items))
    n = sum(len(i) for _, i in groups)
    toc = '<div class="lk-toc">' + ''.join(f'<a href="#{g["id"]}">{e(g["title"].split(" (")[0])} ({len(i)})</a>' for g, i in groups) + '</div>'
    out = []
    for g, items in groups:
        li = []
        for i in items:
            u = i['url']; web = u.startswith('http')
            url = f'<a class="lk-u" href="{e(u)}" target="_blank" rel="noopener">{e(u)}</a>' if web else f'<span class="lk-u path" title="Click to copy" data-copy="{e(u)}">{e(u)}</span>'
            sc, sl = SITE.get(i.get('site', 'all'), ('', ''))
            h = i.get('http')
            hb = '' if not web or h in (None, '') else (f'<span class="ok">{h}</span>' if h == 200 else f'<span class="warn">{h}</span>')
            st = i.get('status', '')
            li.append(f'<li data-site="{i.get("site", "all")}" data-q="{e((i["title"] + " " + u + " " + (i.get("note") or "")).lower())}">'
                      f'<div class="lk-t">{e(i["title"])}<small>{e(i.get("note") or "")}</small></div>{url}'
                      f'<div class="lk-m tg">{f"<span class={chr(34)}{sc}{chr(34)}>{sl}</span>" if sl else ""}<span>{e(i.get("kind", ""))}</span>'
                      f'{f"<span>{e(st)}</span>" if st and st != "live" else ""}{hb}</div></li>')
        out.append(f'<section class="lk-grp" id="{g["id"]}"><h2>{e(g["title"])}<small>{len(items)}</small></h2><ul class="lk-list">{"".join(li)}</ul></section>')
    js = """<script>
(function(){var q=document.getElementById('lkq'),bs=document.querySelectorAll('[data-f]'),f='all';
function run(){var t=q.value.trim().toLowerCase();document.querySelectorAll('.lk-list li').forEach(function(li){
 var ok=(f==='all'||li.dataset.site===f||li.dataset.site==='all')&&(!t||li.dataset.q.indexOf(t)>-1);li.hidden=!ok;});
 document.querySelectorAll('.lk-grp').forEach(function(g){g.hidden=!g.querySelector('li:not([hidden])');});}
q.addEventListener('input',run);bs.forEach(function(b){b.addEventListener('click',function(){f=b.dataset.f;
 bs.forEach(function(x){x.setAttribute('aria-pressed',x===b);});run();});});
document.addEventListener('click',function(ev){var p=ev.target.closest('[data-copy]');if(!p)return;
 try{navigator.clipboard.writeText(p.dataset.copy);p.style.background='#E6F4EC';setTimeout(function(){p.style.background='';},700);}catch(e){}});})();
</script>"""
    bar = ('<div class="lk-bar"><input id="lkq" type="search" placeholder="Search %d links (page, event, repo, folder...)" aria-label="Search links">'
           '<button data-f="all" aria-pressed="true">All</button><button data-f="hb" aria-pressed="false">HummingBeing</button>'
           '<button data-f="bhd" aria-pressed="false">BHD Asia</button><button data-f="tre" aria-pressed="false">TRE SG</button></div>') % n
    body = (head('Every link, in one place', f'All {n} links made for Isabelle since August 2026: the 3 live sites and their pages, every event, the 2027 cohort, repositories, previews, plans, admin consoles, Drive folders and social channels. Status codes checked {d.get("generated", "")}.', 'links.html')
            + bar + toc + ''.join(out) + js + FOOT % dt.date.today().strftime('%d %b %Y'))
    (R / 'links.html').write_text(body, encoding='utf-8')
    return n


if __name__ == '__main__':
    pipeline(); print('pipeline.html'); print('links.html', links(), 'links')
