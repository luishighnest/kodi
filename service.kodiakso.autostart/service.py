# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon('service.kodiakso.autostart')
TARGET = 'plugin.video.kodiakso'


def autostart_once():
    # 1) check impostazione enabled
    try:
        enabled = ADDON.getSettingBool('enabled')
    except Exception:
        enabled = ADDON.getSetting('enabled') == 'true'
    if not enabled:
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
    # aspetta massimo 30s che la Window Home sia caricata (evita RunAddon troppo presto)
    waited = 0
    while not monitor.abortRequested() and waited < 30000:
        if xbmc.getCondVisibility('Window.IsActive(home)'):
            break
        if monitor.waitForAbort(0.5):
            return
        waited += 500

    # delay aggiuntivo dopo home pronta
    if delay > 0:
        # waitForAbort interrompibile
        if monitor.waitForAbort(delay):
            return

    # 5) doppio controllo enabled (utente potrebbe averlo disattivato nel frattempo)
    try:
        enabled2 = ADDON.getSettingBool('enabled')
    except Exception:
        enabled2 = ADDON.getSetting('enabled') == 'true'
    if not enabled2:
        return

    xbmc.log('[PZ8 Autostart] apro %s (delay=%ds)' % (TARGET, delay), xbmc.LOGINFO)
    xbmc.executebuiltin('RunAddon(%s)' % TARGET)


if __name__ == '__main__':
    autostart_once()
    # service resta in vita per log ma non fa loop: Kodi lo tiene attivo fino a waitForAbort
    # se vuoi che rimanga attivo per future esecuzioni, usa Monitor.waitForAbort in loop
    monitor = xbmc.Monitor()
    monitor.waitForAbort()
