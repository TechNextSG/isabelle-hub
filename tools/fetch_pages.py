"""Read each live site's sitemap and every page's <title> -> tools/pages.json."""
import json, re, urllib.request, html, pathlib, concurrent.futures as cf

SITES = {"hb": "https://hummingbeing.com/sitemap.xml",
         "bhd": "https://bhdasia.com/sitemap.xml",
         "tre": "https://tre-in-singapore.com/sitemap.xml"}
UA = {"User-Agent": "Mozilla/5.0 isabelle-hub"}

def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read().decode("utf-8", "replace")

def title(u):
    try:
        m = re.search(r"<title>(.*?)</title>", get(u), re.S | re.I)
        return html.unescape(m.group(1)).strip() if m else ""
    except Exception as e:
        return "ERR " + str(e)

out = {}
for k, sm in SITES.items():
    locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", get(sm))
    with cf.ThreadPoolExecutor(8) as ex:
        titles = list(ex.map(title, locs))
    out[k] = [{"url": u, "title": t} for u, t in zip(locs, titles)]
    print(k, len(locs))
p = pathlib.Path(__file__).with_name("pages.json")
p.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
