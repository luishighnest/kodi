# Kodi Repo di Luigi

Repository Kodi ospitato su GitHub Pages.

## Installazione

1. In Kodi: `Impostazioni -> Sistema -> Componenti aggiuntivi -> Abilita sorgenti sconosciute`
2. `File Manager -> Aggiungi sorgente -> https://luishighnest.github.io/kodi/`
3. `Componenti aggiuntivi -> Installa da file zip -> kodi -> zips/repository.luishighnest/repository.luishighnest-1.0.0.zip`
4. `Installa da repository -> Luigi Repo` oppure installa lo zip del plugin direttamente.

## Struttura

- `plugin.video.kodiakso/` - il plugin video
- `repository.luishighnest/` - l'addon repository
- `zips/` - archivi degli addon
- `addons.xml` / `addons.xml.md5` - indice richiesto da Kodi

## Aggiornare un addon

1. Incrementa la versione in `addon.xml`
2. Ricrea lo zip in `zips/<id>/<id>-<version>.zip`
3. Rigenera `addons.xml` e `addons.xml.md5`
4. Push su `main`