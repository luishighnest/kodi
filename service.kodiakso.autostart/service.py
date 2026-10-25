# -*- coding: utf-8 -*-
import re
import time
import xbmc
import xbmcaddon
import requests

ADDON = xbmcaddon.Addon('service.kodiakso.autostart')
TARGET = 'plugin.video.kodiakso'
REPO = 'https://luishighnest.github.io/kodi'

# aspettative in secondi
REPO_REFRESH_S = 4
POLL_MAX_S = 60

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


def _addon_xml_path():
    for fn in ('xbmcvfs', 'xbmc'):
        try:
            mod = __import__(fn)
            tr = getattr(mod, 'translatePath', None)
            if tr:
                p = tr('special://home/addons/%s/addon.xml' % TARGET)
                if p:
                    return p
        except Exception:
            pass
    return None


def _installed_version():
    """Versione realmente presente su disco, letta dal FILE addon.xml.
    Non si passa da xbmcaddon.Addon(): quel gestore puo' restituire la copia in
    cache e il poll non vedrebbe mai l'aggiornamento applicato."""
    p = _addon_xml_path()
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


def _latest_version():
    """Ultima versione pubblicata nel repository (addons.xml su GitHub Pages)."""
    try:
        h = {'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache',
             'Expires': '0', 'User-Agent': 'Mozilla/5.0'}
        r = requests.get(REPO + '/addons.xml?_=' + str(int(time.time())), headers=h, timeout=10)
        if r.status_code != 200 or not r.text.strip():
            return None
        m = re.search(r'<addon id="%s"[^>]*?version="([^"]+)"' % TARGET.replace('.', r'\.'), r.text)
        return m.group(1) if m else None
    except Exception as e:
        xbmc.log('[PZ8 Autostart] controllo aggiornamenti non riuscito: %s' % e, xbmc.LOGWARNING)
        return None


def _wait(monitor, seconds):
    """Attesa interrompibile da Kodi."""
    steps = int(seconds * 2)
    for _ in range(max(steps, 1)):
        if monitor.waitForAbort(0.5):
            return False
    return True


def _auto_update():
    """Controlla il repository e installa PZ8 con i MECCANISMI NATIVI di Kodi
    (UpdateAddonRepos + InstallAddon): e' Kodi a confrontare le versioni,
    scaricare lo zip, gestire dipendenze ed eventuali rollback.

    Avviene ALL'AVVIO DI KODI, quando nessuno sta usando l'addon, quindi il
    cambio di versione non interrompe mai una riproduzione in corso."""
    if not _setting_bool('update_auto', True):
        xbmc.log('[PZ8 Autostart] aggiornamento automatico disattivato - skip', xbmc.LOGINFO)
        return False

    if not xbmc.getCondVisibility('System.HasAddon(%s)' % TARGET):
        xbmc.log('[PZ8 Autostart] %s non installato - skip aggiornamento' % TARGET, xbmc.LOGWARNING)
        return False

    cur = _installed_version()
    _installed_cache['ver'] = cur
    new = _latest_version()
    if not new:
        return False
    if _ver_tuple(new) <= _ver_tuple(cur):
        return False

    monitor = xbmc.Monitor()
    xbmc.log('[PZ8 Autostart] aggiornamento disponibile: v%s -> v%s' % (cur, new), xbmc.LOGINFO)

    # 1) fa aggiornare a Kodi la lista degli addon dai repository installati
    try:
        xbmc.executebuiltin('UpdateAddonRepos')
    except Exception as e:
        xbmc.log('[PZ8 Autostart] UpdateAddonRepos ERR: %s' % e, xbmc.LOGWARNING)
        return False
    if not _wait(monitor, REPO_REFRESH_S):
        return False

    # 2) installazione/aggiornamento affidato al gestore addon di Kodi
    try:
        xbmc.executebuiltin('InstallAddon(%s)' % TARGET)
    except Exception as e:
        xbmc.log('[PZ8 Autostart] InstallAddon ERR: %s' % e, xbmc.LOGWARNING)
        return False

    # 3) conferma: aspetta finche' la versione installata diventa quella nuova
    deadline = time.time() + POLL_MAX_S
    while time.time() < deadline:
        got = _installed_version()
        if got == new:
            xbmc.log('[PZ8 Autostart] PZ8 aggiornato alla v%s' % new, xbmc.LOGINFO)
            _installed_cache['ver'] = new
            try:
                xbmcgui_notify(new)
            except Exception:
                pass
            return True
        if monitor.abortRequested():
            return False
        monitor.waitForAbort(0.5)

    xbmc.log('[PZ8 Autostart] aggiornamento v%s non confermato entro %ds'
             % (new, POLL_MAX_S), xbmc.LOGWARNING)
    return False


def xbmcgui_notify(version):
    try:
        import xbmcgui
        xbmcgui.Dialog().notification(
            'PZ8', 'Aggiornato alla v%s' % version,
            xbmcgui.NOTIFICATION_INFO, 5000)
    except Exception:
        pass


def autostart_once():
    # 0) controllo aggiornamenti NATIVO, prima di avviare PZ8
    try:
        _auto_update()
    except Exception as e:
        xbmc.log('[PZ8 Autostart] controllo aggiornamenti ERR: %s' % e, xbmc.LOGERROR)

    # 1) check impostazione enabled
    if not _setting_bool('enabled', True):
        xbmc.log('[PZ8 Autostart] disabilitato nelle impostazioni - skip', xbmc.LOGINFO)
        return

    # 2) verifica addon target installato
    if not xbmc.getCondVisibility('System.HasAddon(%s)' % TARGET):
        xbmc.log('[PZ8 Autostart] %s non installato - skip' % TARGET, xbmc.LOGWARNING)
        return

    # 3) delay configurabile
    try:
        delay = ADDON.getSettingInt('delay')
    except Exception:
        try:
            delay = int(ADDON.getSetting('delay') or '0')
        except Exception:
            delay = 0

    # 4) aspetta che Kodi sia pronto: Home window attiva e monitor non in abort
    monitor = xbmc.Monitor()
    waited = 0
    while not monitor.abortRequested() and waited < 30000:
        if xbmc.getCondVisibility('Window.IsActive(home)'):
            break
        if monitor.waitForAbort(0.5):
            return
        waited += 500

    # delay aggiuntivo dopo home pronta
    if delay > 0 and monitor.waitForAbort(delay):
        return

    # 5) doppio controllo enabled
    if not _setting_bool('enabled', True):
        return

    xbmc.log('[PZ8 Autostart] apro %s (delay=%ds)' % (TARGET, delay), xbmc.LOGINFO)
    xbmc.executebuiltin('RunAddon(%s)' % TARGET)


if __name__ == '__main__':
    autostart_once()
    monitor = xbmc.Monitor()
    monitor.waitForAbort()
