/**
 * Diagnostic Worker per analizzare tutte le chiamate Stalker su nxtbox.uk
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

async function rawReq(url, token = null) {
  const headers = {
    ...STB_HEADERS,
    "Cookie": `mac=${encodeURIComponent(MAC_ADDRESS)}; stb_lang=en; timezone=${encodeURIComponent(TIMEZONE)}`
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const r = await fetch(url, { headers });
  const text = await r.text();
  try {
    return { status: r.status, json: JSON.parse(text) };
  } catch (e) {
    return { status: r.status, raw_text: text.slice(0, 300) };
  }
}

export default {
  async fetch(request) {
    // 1. Handshake
    const hs = await rawReq(`${PORTAL_BASE}/server/load.php?type=stb&action=handshake&JsHttpRequest=1-xml`);
    const token = hs?.json?.js?.token;

    // 2. Profile
    const prof = await rawReq(`${PORTAL_BASE}/server/load.php?type=stb&action=get_profile&JsHttpRequest=1-xml`, token);

    // 3. Genres
    const genres = await rawReq(`${PORTAL_BASE}/server/load.php?type=itv&action=get_genres&JsHttpRequest=1-xml`, token);

    // 4. All channels
    const all = await rawReq(`${PORTAL_BASE}/server/load.php?type=itv&action=get_all_channels&JsHttpRequest=1-xml`, token);

    // 5. Ordered list page 1
    const ord = await rawReq(`${PORTAL_BASE}/server/load.php?type=itv&action=get_ordered_list&genre=*&force_ch_link_check=0&fav=0&sortby=number&p=1&JsHttpRequest=1-xml`, token);

    return new Response(JSON.stringify({
      token,
      profile: prof,
      genres: genres,
      all_channels: all,
      ordered_list: ord
    }, null, 2), {
      headers: { "Content-Type": "application/json" }
    });
  }
};
