"""Capture 960x540 thumbnails (cover + a scrolled hover shot) for every hub card.
usage: python tools/thumbs.py [slug ...]   (no args = all)"""
import json, subprocess, sys, time, base64, urllib.request, tempfile, shutil, io, pathlib
import websocket
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from hub_data import ITEMS

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, H, PORT = 1440, 810, 9347
OUT = ROOT / "assets" / "img" / "thumbs"
OUT.mkdir(parents=True, exist_ok=True)
want = set(sys.argv[1:])

prof = tempfile.mkdtemp(prefix="ihub")
p = subprocess.Popen([CHROME, "--headless=new", f"--remote-debugging-port={PORT}", f"--user-data-dir={prof}",
                      "--no-first-run", "--remote-allow-origins=*", "--hide-scrollbars", f"--window-size={W},{H}", "about:blank"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(60):
        try:
            tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json")); break
        except Exception: time.sleep(.25)
    ws = websocket.create_connection([t for t in tabs if t.get("type") == "page"][0]["webSocketDebuggerUrl"], timeout=60)
    mid = [0]
    def call(method, **params):
        mid[0] += 1; ws.send(json.dumps({"id": mid[0], "method": method, "params": params}))
        while True:
            m = json.loads(ws.recv())
            if m.get("id") == mid[0]: return m.get("result", {})
    call("Emulation.setDeviceMetricsOverride", width=W, height=H, deviceScaleFactor=1, mobile=False)
    call("Page.enable"); call("Runtime.enable")

    def save(name):
        data = base64.b64decode(call("Page.captureScreenshot", format="png")["data"])
        im = Image.open(io.BytesIO(data)).convert("RGB").resize((960, 540), Image.LANCZOS)
        im.save(OUT / name, "JPEG", quality=82, optimize=True, progressive=True)

    for it in ITEMS:
        if want and it["slug"] not in want: continue
        call("Page.navigate", url=it["url"]); time.sleep(it.get("wait", 5))
        # close cookie/intro overlays that some pages show, then capture the cover
        call("Runtime.evaluate", expression="window.scrollTo(0,0)")
        time.sleep(.8); save(f"{it['slug']}.jpg")
        call("Runtime.evaluate", expression="window.scrollTo({top:innerHeight*1.15,behavior:'instant'})")
        time.sleep(2.2); save(f"{it['slug']}-2.jpg")
        print("ok", it["slug"])
finally:
    p.kill(); time.sleep(1); shutil.rmtree(prof, ignore_errors=True)
