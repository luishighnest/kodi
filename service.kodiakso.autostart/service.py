# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import zipfile
import xbmc
import xbmcaddon
import urllib.request
import urllib.error

ADDON = xbmcaddon.Addon('service.kodiakso.autostart')
TARGET = 'plugin.video.kodiakso'
REPO_ID = 'repository.luishighnest'
REPO_URL = 'https://luishighnest.github.io/kodi'

REPO_REFRESH_S = 4
POLL_MAX_S = 30

_installed_cache = {'ver': None}


def _setting_bool(key, default=True):
    try:
        return ADDON.getSettingBool(key)
    except Exception:
        pass
    try:
        v = ADDON.getSetting(key)
        if v in ('true', 'false'):
            return v == 'true'
    except Exception:
        pass
    return default


def _translate_path(path):
    for fn in ('xbmcvfs', 'xbmc'):
        try:
            mod = __import__(fn)
            tr = getattr(mod, 'translatePath', None)
            if tr:
                return tr(path)
        except Exception:
            pass
    return None


def _addon_xml_path(aid=TARGET):
    p = _translate_path('special://home/addons/%s/addon.xml' % aid)
    return p if p and os.path.exists(p) else None


def _addons_dir():
    return _translate_path('special://home/addons')


def _packages_dir():
    p = _translate_path('special://home/addons/packages')
    if p and not os.path.exists(p):
        try:
            os.makedirs(p, exist_ok=True)
        except Exception:
            pass
    return p


def _installed_version():
    """Versione realmente presente su disco, letta dal file addon.xml."""
    p = _addon_xml_path(TARGET)
    if p:
        try:
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                txt = f.read(4096)
            m = re.search(r'<addon[^>]*?\sid="%s"[^>]*?\sversion="([^"]+)"' % TARGET.replace('.', r'\.'), txt)
            if not m:
                m = re.search(r'<addon[^>]*?\sversion="([^"]+)"', txt)
            if m:
                return m.group(1)
        except Exception:
            pass
    try:
        v = xbmcaddon.Addon(TARGET).getAddonInfo('version')
        if v:
            return v
    except Exception:
        pass
    return _installed_cache['ver'] or '0'


def _ver_tuple(s):
    try:
        return tuple(int(x) for x in re.findall(r'\d+', str(s)) or ['0'])
    except Exception:
        return (0,)


def _http_get(url, timeout=10):
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Kodi-PZ8',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        xbmc.log('[PZ8 Autostart] HTTP GET ERR (%s): %s' % (url, e), xbmc.LOGWARNING)
        return None


def _latest_version():
    """Ultima versione pubblicata nel repository (addons.xml su GitHub Pages)."""
    xml_txt = _http_get('%s/addons.xml?_=%d' % (REPO_URL, int(time.time())))
    if not xml_txt:
        return None
    m = re.search(r'<addon\b[^>]*?\bid="%s"[^>]*?\bversion="([^"]+)"' % TARGET.replace('.', r'\.'), xml_txt)
    return m.group(1) if m else None


def _wait(monitor, seconds):
    steps = int(seconds * 2)
    for _ in range(max(steps, 1)):
        if monitor.waitForAbort(0.5):
            return False
    return True


def _direct_zip_update(version):
    """Fallback garantito: scarica ed estrae direttamente lo zip di PZ8 se l'installazione nativa fallisce."""
    zip_url = '%s/zips/%s/%s-%s.zip' % (REPO_URL, TARGET, TARGET, version)
    pkg_dir = _packages_dir()
    if not pkg_dir:
        return False
    local_zip = os.path.join(pkg_dir, '%s-%s.zip' % (TARGET, version))
    try:
        xbmc.log('[PZ8 Autostart] Download diretto fallback: %s' % zip_url, xbmc.LOGINFO)
        req = urllib.request.Request(zip_url, headers={'User-Agent': 'Mozilla/5.0 Kodi-PZ8'})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        with open(local_zip, 'wb') as f:
            f.write(data)

        # Estrai nella cartella addons
        addons_path = _addons_dir()
        with zipfile.ZipFile(local_zip, 'r') as zf:
            zf.extractall(addons_path)

        xbmc.executebuiltin('UpdateLocalAddons')
        xbmc.log('[PZ8 Autostart] Estrazione zip diretta completata per v%s' % version, xbmc.LOGINFO)
        return True
    except Exception as e:
        xbmc.log('[PZ8 Autostart] Errore direct zip update: %s' % e, xbmc.LOGERROR)
        return False


def _auto_update():
    """Controlla il repository e aggiorna PZ8 all'avvio di Kodi."""
    if not _setting_bool('update_auto', True):
        xbmc.log('[PZ8 Autostart] aggiornamento automatico disattivato - skip', xbmc.LOGINFO)
        return False

    cur = _installed_version()
    _installed_cache['ver'] = cur
    new = _latest_version()
    if not new:
        return False
    if _ver_tuple(new) <= _ver_tuple(cur):
        xbmc.log('[PZ8 Autostart] PZ8 già aggiornato (v%s)' % cur, xbmc.LOGINFO)
        return False

    monitor = xbmc.Monitor()
    xbmc.log('[PZ8 Autostart] Trovato aggiornamento PZ8: v%s -> v%s' % (cur, new), xbmc.LOGINFO)

    # 1. Prova metodo nativo Kodi
    has_repo = xbmc.getCondVisibility('System.HasAddon(%s)' % REPO_ID)
    updated = False

    if has_repo:
        try:
            xbmc.executebuiltin('UpdateAddonRepos')
            _wait(monitor, REPO_REFRESH_S)
            xbmc.executebuiltin('InstallAddon(%s)' % TARGET)

            # Polling per verificare se Kodi ha completato
            deadline = time.time() + 15
            while time.time() < deadline:
                if _installed_version() == new:
                    updated = True
                    break
                if monitor.abortRequested():
                    return False
                monitor.waitForAbort(0.5)
        except Exception as e:
            xbmc.log('[PZ8 Autostart] Metodo nativo fallito: %s' % e, xbmc.LOGWARNING)

    # 2. Se non c'è il repo o il metodo nativo non ha scritto su disco entro 15s -> direct zip update
    if not updated and _installed_version() != new:
        xbmc.log('[PZ8 Autostart] Avvio aggiornamento diretto via ZIP...', xbmc.LOGINFO)
        if _direct_zip_update(new):
            updated = True

    if updated or _installed_version() == new:
        _installed_cache['ver'] = new
        xbmc.log('[PZ8 Autostart] PZ8 aggiornato con successo alla v%s' % new, xbmc.LOGINFO)
        xbmcgui_notify(new)
        return True
    else:
        xbmc.log('[PZ8 Autostart] Impossibile confermare aggiornamento alla v%s' % new, xbmc.LOGWARNING)
        return False


def xbmcgui_notify(version):
    try:
        import xbmcgui
        xbmcgui.Dialog().notification('PZ8', 'Aggiornato alla v%s' % version, xbmcgui.NOTIFICATION_INFO, 5000)
    except Exception:
        pass


def autostart_once():
    # 0) Controllo e aggiornamento automatico PRIMA di aprire l'addon
    try:
        _auto_update()
    except Exception as e:
        xbmc.log('[PZ8 Autostart] Errore in _auto_update: %s' % e, xbmc.LOGERROR)

    # 1) Verifica se abilitato avvio automatico GUI
    if not _setting_bool('enabled', True):
        xbmc.log('[PZ8 Autostart] Avvio automatico disabilitato - skip apertura PZ8', xbmc.LOGINFO)
        return

    # 2) Verifica se target è installato
    if not xbmc.getCondVisibility('System.HasAddon(%s)' % TARGET) and not _addon_xml_path(TARGET):
        xbmc.log('[PZ8 Autostart] %s non installato - skip apertura' % TARGET, xbmc.LOGWARNING)
        return

    # 3) Delay configurabile
    try:
        delay = ADDON.getSettingInt('delay')
    except Exception:
        try:
            delay = int(ADDON.getSetting('delay') or '0')
        except Exception:
            delay = 0

    # 4) Aspetta che la finestra Home sia pronta
    monitor = xbmc.Monitor()
    waited = 0
    while not monitor.abortRequested() and waited < 30000:
        if xbmc.getCondVisibility('Window.IsActive(home)'):
            break
        if monitor.waitForAbort(0.5):
            return
        waited += 500

    if delay > 0 and monitor.waitForAbort(delay):
        return

    if not _setting_bool('enabled', True):
        return

    xbmc.log('[PZ8 Autostart] Apertura PZ8 (%s, delay=%ds)' % (TARGET, delay), xbmc.LOGINFO)
    xbmc.executebuiltin('RunAddon(%s)' % TARGET)


if __name__ == '__main__':
    autostart_once()
    monitor = xbmc.Monitor()
    monitor.waitForAbort()
