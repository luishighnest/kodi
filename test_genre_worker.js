/**
 * Test canali per genere specifico (es. IT - Sport: 10122, IT - Italia: 10120)
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
  async fetch() {
    const hs = await rawReq(`${PORTAL_BASE}/server/load.php?type=stb&action=handshake&JsHttpRequest=1-xml`);
    const token = hs?.json?.js?.token;

    // get_profile
    await rawReq(`${PORTAL_BASE}/server/load.php?type=stb&action=get_profile&JsHttpRequest=1-xml`, token);

    // Test IT - Sport (genre: 10122)
    const itSport = await rawReq(`${PORTAL_BASE}/server/load.php?type=itv&action=get_ordered_list&genre=10122&force_ch_link_check=0&fav=0&sortby=number&p=1&JsHttpRequest=1-xml`, token);

    // Test IT - Italia (genre: 10120)
    const itItalia = await rawReq(`${PORTAL_BASE}/server/load.php?type=itv&action=get_ordered_list&genre=10120&force_ch_link_check=0&fav=0&sortby=number&p=1&JsHttpRequest=1-xml`, token);

    return new Response(JSON.stringify({
      token,
      it_sport_channels: itSport,
      it_italia_channels: itItalia
    }, null, 2), {
      headers: { "Content-Type": "application/json" }
    });
  }
};
