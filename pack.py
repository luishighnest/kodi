import os
import hashlib
import zipfile
import re

addon_dir = 'plugin.video.kodiakso'
zip_dir = os.path.join('zips', addon_dir)
os.makedirs(zip_dir, exist_ok=True)
zip_path = os.path.join(zip_dir, 'plugin.video.kodiakso-1.11.76.zip')

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(addon_dir):
        for file in files:
            full_path = os.path.join(root, file)
            z.write(full_path, full_path)

print('Zip created:', zip_path)

with open('addons.xml', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'id="plugin\.video\.kodiakso" name="PZ8" version="[^"]+"', 'id="plugin.video.kodiakso" name="PZ8" version="1.11.76"', content)
with open('addons.xml', 'w', encoding='utf-8') as f:
    f.write(content)

md5 = hashlib.md5(open('addons.xml', 'rb').read()).hexdigest()
with open('addons.xml.md5', 'w', encoding='utf-8') as f:
    f.write(md5)

print('addons.xml and md5 updated:', md5)
