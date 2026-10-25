import hashlib
import os
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ZIPS = ROOT / 'zips'
SITE = 'https://luishighnest.github.io/kodi'

SKIP_DIRS = {'zips', '.git', '__pycache__', 'sportzx_apk', 'sportzx_smali'}
SKIP_EXT = {'.pyc', '.bak', '.orig', '.log'}

# ---------------------------------------------------------------- scoperta addon
addons = []
for d in sorted(ROOT.iterdir()):
    if not d.is_dir() or d.name in SKIP_DIRS:
        continue
    ax = d / 'addon.xml'
    if not ax.exists():
        continue

    txt = ax.read_text(encoding='utf-8')
    m = re.search(r'<addon\b[^>]*?\bid="([^"]+)"', txt)
    m2 = re.search(r'<addon\b[^>]*?\bversion="([^"]+)"', txt)
    if not m or not m2:
        print('[pack] SALTO %s: id/versione non leggibili in addon.xml' % d.name)
        continue

    aid, ver = m.group(1), m2.group(1)
    if aid != d.name:
        print('[pack] ATTENZIONE: cartella %s ma id addon %s' % (d.name, aid))

    addons.append({'dir': d, 'id': aid, 'ver': ver, 'xml': txt})

if not addons:
    print('[pack] ERRORE: nessun addon trovato')
    raise SystemExit(1)

print('[pack] Addon trovati:')
for a in addons:
    print('       - %-28s v%s' % (a['id'], a['ver']))


# ---------------------------------------------------------------------- packing
def build_zip(a):
    out_dir = ZIPS / a['id']
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / ('%s-%s.zip' % (a['id'], a['ver']))

    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(str(a['dir'])):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
            for fn in files:
                if Path(fn).suffix.lower() in SKIP_EXT:
                    continue
                full = os.path.join(root, fn)
                # lo zip contiene i file con il prefisso <id>/ come da convenzione Kodi
                arc = os.path.join(a['id'], os.path.relpath(full, a['dir']))
                z.write(full, arc.replace(os.sep, '/'))

    print('[pack] Zip creato: %s (%d B)' % (out.relative_to(ROOT), out.stat().st_size))

    # copia in zips/ per il download diretto dal browser
    flat = ZIPS / out.name
    if flat.resolve() != out.resolve():
        flat.write_bytes(out.read_bytes())
        print('[pack] Copia in zips/%s' % out.name)
    return out


for a in addons:
    build_zip(a)


# ------------------------------------------------------------------- addons.xml
# Formato atteso da Kodi: radice <addons> con <addon> figli.
# CAddonMgr::AddonsFromRepoXML rifiuta il file intero ("Malformed") se la radice
# non si chiama "addons", quindi non basta mettere un solo <addon> a radice.
DECL = re.compile(r'^\s*<\?xml[^>]*\?>\s*', re.S)
body = []
for a in addons:
    b = DECL.sub('', a['xml']).strip()
    if not b.startswith('<addon'):
        print('[pack] SALTO %s da addons.xml: non inizia con <addon>' % a['id'])
        continue
    body.append(b)

out_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<addons>',
]
for b in body:
    out_lines.extend('    ' + ln if ln.strip() else ln for ln in b.split('\n'))
out_lines.append('</addons>')

# LF obbligatorio: .gitattributes forza eol=lf, quindi git pubblica la versione LF.
# Se venisse scritto in CRLF (default su Windows) il md5 non corrisponderebbe mai
# a quello servito da GitHub Pages e Kodi rifiuterebbe il file per checksum errato.
addons_xml = '\n'.join(out_lines) + '\n'
(ROOT / 'addons.xml').write_text(addons_xml, encoding='utf-8', newline='\n')

digest = hashlib.md5(addons_xml.encode('utf-8')).hexdigest()
(ROOT / 'addons.xml.md5').write_text(digest + '\n', encoding='utf-8', newline='\n')
print('[pack] addons.xml scritto (%d B, %d addon) md5=%s'
      % (len(addons_xml.encode('utf-8')), len(body), digest))


# ------------------------------------------------------------------ index.html
for a in addons:
    idx = ZIPS / a['id'] / 'index.html'
    idx.write_text(
        '<!DOCTYPE html>\n<html>\n<body>\n'
        '<a href="%s-%s.zip">%s-%s.zip</a><br>\n'
        '</body>\n</html>\n' % (a['id'], a['ver'], a['id'], a['ver']),
        encoding='utf-8', newline='\n')

links = ''.join('<a href="%s/">%s/</a><br>\n' % (a['id'], a['id']) for a in addons)
links += ''.join('<a href="%s-%s.zip">%s-%s.zip</a><br>\n'
                 % (a['id'], a['ver'], a['id'], a['ver']) for a in addons)
(ZIPS / 'index.html').write_text(
    '<!DOCTYPE html>\n<html>\n<body>\n' + links + '</body>\n</html>\n',
    encoding='utf-8', newline='\n')
print('[pack] index.html aggiornati')
