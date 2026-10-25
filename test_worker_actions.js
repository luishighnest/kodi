/**
 * Cloudflare Worker Test Actions per nxtbox.uk
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

async function doHandshake() {
  const hsUrl = `${PORTAL_BASE}/server/load.php?type=stb&action=handshake&JsHttpRequest=1-xml`;
  const hsResp = await fetch(hsUrl, {
    headers: {
      ...STB_HEADERS,
      "Cookie": `mac=${encodeURIComponent(MAC_ADDRESS)}; timezone=${encodeURIComponent(TIMEZONE)}`
    }
  });
  const hsData = await hsResp.json();
  const token = hsData?.js?.token;

  // get_profile
  const profUrl = `${PORTAL_BASE}/server/load.php?type=stb&action=get_profile&JsHttpRequest=1-xml`;
  const profResp = await fetch(profUrl, {
    headers: {
      ...STB_HEADERS,
      "Cookie": `mac=${encodeURIComponent(MAC_ADDRESS)}; stb_lang=en; timezone=${encodeURIComponent(TIMEZONE)}`,
      "Authorization": `Bearer ${token}`
    }
  });
  const profData = await profResp.json();

  return { token, profile: profData?.js };
}

async function testAction(action, extraParams = "") {
  const { token, profile } = await doHandshake();
  const url = `${PORTAL_BASE}/server/load.php?type=itv&action=${action}${extraParams}&JsHttpRequest=1-xml`;
  const resp = await fetch(url, {
    headers: {
      ...STB_HEADERS,
      "Cookie": `mac=${encodeURIComponent(MAC_ADDRESS)}; stb_lang=en; timezone=${encodeURIComponent(TIMEZONE)}`,
      "Authorization": `Bearer ${token}`
    }
  });
  const data = await resp.json();
  return { action, data: data?.js, profile };
}

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === "/test_genres") {
      const res = await testAction("get_genres");
      return new Response(JSON.stringify(res, null, 2), { headers: { "Content-Type": "application/json" } });
    }

    if (url.pathname === "/test_profile") {
      const res = await doHandshake();
      return new Response(JSON.stringify(res, null, 2), { headers: { "Content-Type": "application/json" } });
    }

    if (url.pathname === "/test_all") {
      const res = await testAction("get_all_channels");
      return new Response(JSON.stringify(res, null, 2), { headers: { "Content-Type": "application/json" } });
    }

    if (url.pathname === "/test_ordered") {
      const res = await testAction("get_ordered_list", "&genre=1&force_ch_link_check=0&fav=0&sortby=number");
      return new Response(JSON.stringify(res, null, 2), { headers: { "Content-Type": "application/json" } });
    }

    return new Response("Usa /test_profile, /test_genres, /test_all, /test_ordered");
  }
};
