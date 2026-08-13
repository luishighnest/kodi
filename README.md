# Kodi Repo di Luigi

Repository Kodi ospitato su GitHub Pages.

## Struttura

- `playlist.m3u` - la playlist dei canali (modifica QUESTO file per aggiornare i canali)
- `plugin.video.kodiakso/` - il plugin video
- `repository.luishighnest/` - l'addon repository
- `zips/` - archivi degli addon
- `addons.xml` / `addons.xml.md5` - indice richiesto da Kodi

## Installazione (UNA SOLA VOLTA)

1. In Kodi: `Impostazioni -> Sistema -> Componenti aggiuntivi -> Abilita sorgenti sconosciute`
2. `File Manager -> Aggiungi sorgente -> https://luishighnest.github.io/kodi/`
3. `Componenti aggiuntivi -> Installa da file zip -> kodi -> zips/repository.luishighnest/repository.luishighnest-1.0.0.zip`
4. `Installa da repository -> Luigi Repo -> Kodi Akso` (oppure installa lo zip del plugin direttamente)
5. Apri l'addon: i canali compaiono raggruppati per categoria.

## Aggiornare i canali (SENZA reinstallare)

1. Modifica `playlist.m3u` su GitHub (o aggiorna il file locale e fai push)
2. Ricarica l'addon in Kodi (aprilo di nuovo) - la playlist viene riscaricata a ogni apertura

L'addon scarica la playlist da `https://luishighnest.github.io/kodi/playlist.m3u` a ogni avvio. Il percorso è configurabile nelle impostazioni dell'addon (`Playlist URL`).

## Aggiornare il codice dell'addon

1. Incrementa la versione in `addon.xml`
2. Ricrea lo zip in `zips/<id>/<id>-<version>.zip`
3. Rigenera `addons.xml` e `addons.xml.md5`
4. Push su `main`