/**
 * Cloudflare Worker Debugger per capire cosa risponde nxtbox.uk
 */

const PORTAL_BASE = "http://nxtbox.uk";
const MAC_ADDRESS = "00:1A:79:11:8B:A8";
const TIMEZONE = "Europe/Rome";

const STB_HEADERS = {
  "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG250 stbapp ver: 2 rev: 250 Safari/533.3",
  "X-User-Agent": "Model: MAG250; Link: Ethernet",
  "Referer": `${PORTAL_BASE}/c/`,
  "Accept": "*/*"
};

export default {
  async fetch(request) {
    const url = new URL(request.url);

    // Endpoint di debug per vedere la risposta di nxtbox
    if (url.pathname === "/debug") {
      try {
        const u = `${PORTAL_BASE}/server/load.php?type=stb&action=handshake&JsHttpRequest=1-xml`;
        const resp = await fetch(u, {
          headers: {
            ...STB_HEADERS,
            "Cookie": `mac=${encodeURIComponent(MAC_ADDRESS)}; timezone=${encodeURIComponent(TIMEZONE)}`
          }
        });
        const status = resp.status;
        const text = await resp.text();
        return new Response(JSON.stringify({ status, text }), {
          headers: { "Content-Type": "application/json" }
        });
      } catch (e) {
        return new Response(JSON.stringify({ error: e.message }), { status: 500 });
      }
    }

    return new Response("Debug worker attivo. Chiama /debug per testare nxtbox.");
  }
};
