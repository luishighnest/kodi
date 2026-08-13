import sys, re, json, base64, urllib.parse, urllib.request, traceback
from datetime import datetime, timedelta
import xbmc, xbmcgui, xbmcplugin

HANDLE = int(sys.argv[1])
BASE = "plugin://plugin.video.dazn206/"
ICON = ""

API = "https://test34344.herokuapp.com/filter.php"
SECRET = "my_secret_key"
API_UA = "Kodi/19.0 (Windows NT 10.0; Win64; x64) App_Bitness/64 Version/19.0-Matrix"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
HOST = "https://www.nowtv.it"

def log(m):
    xbmc.log("DAZN206: " + m, xbmc.LOGINFO)

def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": API_UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")

def xor_decrypt(b64data):
    data = base64.b64decode(b64data)
    key = SECRET.encode("utf-8")
    out = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    return out.decode("utf-8")

def strip_color(txt):
    txt = re.sub(r'\[COLOR.*?\]', '', txt, flags=re.IGNORECASE)
    txt = re.sub(r'\[/COLOR\]', '', txt, flags=re.IGNORECASE)
    return txt.strip()

def sky_channels():
    channels = []
    seen = set()
    try:
        data = json.loads(http_get(API + "?numTest=A1A260"))
        for it in (data.get('items', data) if isinstance(data, dict) else data):
            mr = it.get('myresolve', '') or ''
            if mr.startswith('sky@@'):
                cid = mr.split('@@', 1)[1]
                if cid not in seen:
                    seen.add(cid)
                    channels.append((strip_color(it.get('title', cid)), cid))
    except Exception as e:
        log("sky A1A260 fetch fail: " + str(e))
    try:
        data = json.loads(http_get(API + "?numTest=A1A122"))
        for it in (data.get('items', data) if isinstance(data, dict) else data):
            title = it.get('title', '')
            if 'Sky' in title and ('IT:' in title or 'IT ' in title):
                clean = strip_color(title).replace('IT:', '').replace('IT', '').strip().replace('  ', ' ')
                cid = clean.replace(' ', '').lower()
                if cid == "skytg24":
                    cid = "tg24"
                if cid not in seen:
                    seen.add(cid)
                    channels.append((clean, cid))
    except Exception as e:
        log("sky A1A122 fetch fail: " + str(e))
    if not channels:
        fallback = [("Sky Sport Uno", "skysportuno"), ("Sky Sport 24", "skysport24"),
                    ("Sky Sport Arena", "skysportarena"), ("Sky Sport Calcio", "skysportcalcio"),
                    ("Sky Sport F1", "skysportf1"), ("Sky Sport Golf", "skysportgolf"),
                    ("Sky Sport Legend", "skysportlegend"), ("Sky Sport Max", "skysportmax"),
                    ("Sky Sport Mix", "skysportmix"), ("Sky Sport MotoGP", "skysportmotogp"),
                    ("Sky Sport Tennis", "skysporttennis"), ("Sky Sport Basket", "skysportbasket"),
                    ("Sky TG 24", "tg24"), ("Sky Uno", "skyuno"), ("Sky Uno +1", "skyunoplus"),
                    ("Sky Atlantic", "skyatlantic"), ("Sky Serie", "skyserie"),
                    ("Sky Collection", "skycollection"), ("Sky Investigation", "skyinvestigation"),
                    ("Sky Adventure", "skyadventure"), ("Sky Crime", "skycrime"),
                    ("Sky Documentaries", "skydocumentaries"), ("Sky Nature", "skynature"),
                    ("History", "historychannel"), ("Comedy Central", "comedycentral"),
                    ("Sky Arte", "skyarte"), ("MTV", "mtv")]
        for t, c in fallback:
            channels.append((t, c))
    for n in range(251, 260):
        cid = "skysport%d" % n
        if cid not in seen:
            seen.add(cid)
            channels.append(("Sky Sport %d" % n, cid))
    return channels

def play_dazn():
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InV1aWRfMSJ9.eyJwYXRocyI6WyIvZGFzaC9kYXpuLWxpbmVhci0yMDYiXSwiZXhjIjpbXSwiaGVhZGVycyI6WyJ1c2VyLWFnZW50Il0sImNvIjp0cnVlLCJpcCI6ZmFsc2UsImFzbiI6WyIxMzMzNSJdLCJpbnRzaWciOiJzZEN3RC1yazlMOVlBbzMzMmM5S0tLU2VyNU5rOHR2X3BfS3JwYi0zb1VFIiwiaWF0IjoxNzg0OTIzMjQ2LCJleHAiOjE3ODUwMDk2NDZ9.Z2jkpJIOMqt5k0hsSawlq9zz5Oq3F7Xe1GE65DC4TSg"
    KID = "6164a0abaa7c53c6875fa1e7fe0bb463"
    KEY = "271510d3e1259571dcc568a232e397eb"
    dazn_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0"
    MPD_URL = "https://dct-ac-live.cdn.indazn.com/dash/dazn-linear-206/stream.mpd?p=web&dazn-token=" + urllib.parse.quote(TOKEN, safe="")
    hdrs = {"User-Agent": dazn_ua, "Referer": "https://www.dazn.com/", "Origin": "https://www.dazn.com", "dazn-token": TOKEN}
    shdrs = urllib.parse.urlencode(hdrs, quote_via=urllib.parse.quote, safe="")
    li = xbmcgui.ListItem(path=MPD_URL)
    li.setProperty("inputstreamaddon", "inputstream.adaptive")
    li.setProperty("inputstream.adaptive.manifest_type", "mpd")
    li.setProperty("inputstream.adaptive.drm_legacy", "org.w3.clearkey|" + KID + ":" + KEY)
    li.setProperty("inputstream.adaptive.manifest_headers", shdrs)
    li.setProperty("inputstream.adaptive.stream_headers", shdrs)
    xbmcplugin.setResolvedUrl(HANDLE, True, li)

def play_sky(parIn, title):
    url = API + "?numTest=A1A159&id=" + urllib.parse.quote(parIn)
    resp = json.loads(http_get(url))
    data = json.loads(xor_decrypt(resp["data"]))
    manifest = data["manifest"]
    kid = data["kid"]
    key = data["key"]
    fine = data.get("fine", "")
    if "EXPIRE" not in fine:
        try:
            exp = datetime.strptime(fine, "%d/%m/%Y %H:%M:%S") + timedelta(hours=2)
            if exp < datetime.now():
                xbmcgui.Dialog().notification(title or parIn, "Link scaduto " + exp.strftime("%d/%m/%Y %H:%M:%S"), xbmcgui.NOTIFICATION_ERROR, 5000)
        except Exception:
            pass
    li = xbmcgui.ListItem(path=manifest, offscreen=True)
    li.setContentLookup(False)
    li.setProperty("inputstream", "inputstream.adaptive")
    li.setProperty("inputstream.adaptive.drm_legacy", "org.w3.clearkey|" + kid + ":" + key)
    hdrs = "User-Agent=" + UA + "&Referer=" + HOST + "/&Origin=" + HOST + "&verifypeer=false"
    li.setProperty("inputstream.adaptive.stream_headers", hdrs)
    li.setProperty("inputstream.adaptive.manifest_headers", hdrs)
    xbmcplugin.setResolvedUrl(HANDLE, True, li)

def build_root():
    li = xbmcgui.ListItem(label="DAZN 1")
    li.setProperty("IsPlayable", "true")
    xbmcplugin.addDirectoryItem(HANDLE, BASE + "?action=dazn1", li, isFolder=False)
    sky = xbmcgui.ListItem(label="Sky")
    xbmcplugin.addDirectoryItem(HANDLE, BASE + "?action=sky", sky, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)

def build_sky_list():
    for title, cid in sky_channels():
        li = xbmcgui.ListItem(label=title)
        li.setProperty("IsPlayable", "true")
        xbmcplugin.addDirectoryItem(HANDLE, BASE + "?action=skyplay&id=" + urllib.parse.quote(cid) + "&t=" + urllib.parse.quote(title), li, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)

try:
    params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
    action = params.get("action", "")
    if action == "sky":
        build_sky_list()
    elif action == "skyplay":
        play_sky(params.get("id", ""), params.get("t", ""))
    else:
        build_root()
except Exception as e:
    xbmc.log("DAZN206 ER: " + traceback.format_exc(), xbmc.LOGERROR)
    xbmcgui.Dialog().ok("DAZN 206 Error", str(e))