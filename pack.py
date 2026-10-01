import os
import hashlib
import zipfile
import re
from pathlib import Path

addon_xml = Path("plugin.video.kodiakso/addon.xml")
if not addon_xml.exists():
    print("ERRORE: addon.xml non trovato")
    exit(1)

xml_txt = addon_xml.read_text(encoding="utf-8")
m = re.search(r'id="plugin\.video\.kodiakso"[^>]*version="([^"]+)"', xml_txt)
if not m:
    print("ERRORE: versione non trovata in addon.xml")
    exit(1)

ver = m.group(1)
print(f"[pack] Versione rilevata da addon.xml: {ver}")

addon_dir = 'plugin.video.kodiakso'
zip_dir = os.path.join('zips', addon_dir)
os.makedirs(zip_dir, exist_ok=True)
zip_filename = f'plugin.video.kodiakso-{ver}.zip'
zip_path = os.path.join(zip_dir, zip_filename)

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(addon_dir):
        for file in files:
            full_path = os.path.join(root, file)
            z.write(full_path, full_path)

print('[pack] Zip creato:', zip_path)

# Copia dello zip anche direttamente in zips/ per download diretto o link rapido
zips_root_zip = os.path.join('zips', zip_filename)
with open(zip_path, 'rb') as f_in, open(zips_root_zip, 'wb') as f_out:
    f_out.write(f_in.read())
print('[pack] Copia creata in:', zips_root_zip)

# Aggiorna index.html in zips/plugin.video.kodiakso/
sub_index = Path(zip_dir) / "index.html"
sub_index.write_text(f'<!DOCTYPE html>\n<html>\n<body>\n<a href="{zip_filename}">{zip_filename}</a><br>\n</body>\n</html>\n', encoding="utf-8")

# Aggiorna index.html in zips/
main_index = Path("zips/index.html")
main_index.write_text(f'<!DOCTYPE html>\n<html>\n<body>\n<a href="plugin.video.kodiakso/">plugin.video.kodiakso/</a><br>\n<a href="repository.luishighnest/">repository.luishighnest/</a><br>\n<a href="{zip_filename}">{zip_filename}</a><br>\n<a href="service.kodiakso.autostart-1.0.1.zip">service.kodiakso.autostart-1.0.1.zip</a><br>\n</body>\n</html>\n', encoding="utf-8")

with open('addons.xml', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'id="plugin\.video\.kodiakso" name="PZ8" version="[^"]+"', f'id="plugin.video.kodiakso" name="PZ8" version="{ver}"', content)
with open('addons.xml', 'w', encoding='utf-8') as f:
    f.write(content)

md5 = hashlib.md5(open('addons.xml', 'rb').read()).hexdigest()
with open('addons.xml.md5', 'w', encoding='utf-8') as f:
    f.write(md5)

print('[pack] addons.xml e md5 aggiornati:', md5)
