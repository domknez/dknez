/**
 * Visitor counter for knez.dev.
 *
 *   POST /hit    called by the page; counts one visitor per day, ignores bots
 *   GET  /count  { total, today }
 *
 * No cookies. A visitor is identified for one day only, by
 * sha256(secret | date | ip | user-agent) — unreadable, unlinkable across days,
 * and deleted after 48 hours.
 */

const BOT_UA = /bot|crawl|spider|slurp|fetch|monitor|preview|headless|lighthouse|pingdom|uptime|scan|curl|wget|python-requests|httpclient|facebookexternalhit|whatsapp|telegram|discord|slack|embedly/i;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const origin = request.headers.get("Origin") || "";
    const allowed = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim());
    const cors = {
      "Access-Control-Allow-Origin": allowed.includes(origin) ? origin : allowed[0],
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Max-Age": "86400",
      "Cache-Control": "no-store",
      "Content-Type": "application/json; charset=utf-8",
      Vary: "Origin",
    };

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });

    if (url.pathname === "/count" && request.method === "GET") {
      return json(await totals(env), cors);
    }

    if (url.pathname === "/hit" && request.method === "POST") {
      // only the site itself may count; anything else just reads
      if (!allowed.includes(origin) || isBot(request)) {
        return json({ ...(await totals(env)), counted: false }, cors);
      }
      const counted = await recordVisit(request, env);
      ctx.waitUntil(purgeOld(env));
      return json({ ...(await totals(env)), counted }, cors);
    }

    return new Response("not found", { status: 404, headers: { "Cache-Control": "no-store" } });
  },
};

function isBot(request) {
  const ua = request.headers.get("User-Agent") || "";
  if (!ua || BOT_UA.test(ua)) return true;
  // Cloudflare's own verified-crawler list: Googlebot, Bingbot, GPTBot, ClaudeBot…
  // Verified by IP range, not by the string they send. Available on every plan.
  const cf = request.cf || {};
  if (cf.verifiedBotCategory) return true;
  if (cf.botManagement && cf.botManagement.verifiedBot) return true;
  return false;
}

async function recordVisit(request, env) {
  const ip = request.headers.get("CF-Connecting-IP") || "";
  const ua = request.headers.get("User-Agent") || "";
  const day = new Date().toISOString().slice(0, 10);
  const h = await sha256(`${env.SALT}|${day}|${ip}|${ua}`);

  const ins = await env.DB.prepare("INSERT OR IGNORE INTO seen (h, day) VALUES (?, ?)").bind(h, day).run();
  if (!ins.meta.changes) return false; // already counted today

  await env.DB.batch([
    env.DB.prepare("INSERT INTO counters (k, n) VALUES ('total', 1) ON CONFLICT(k) DO UPDATE SET n = n + 1"),
    env.DB.prepare("INSERT INTO counters (k, n) VALUES (?, 1) ON CONFLICT(k) DO UPDATE SET n = n + 1").bind(`day:${day}`),
  ]);
  return true;
}

async function totals(env) {
  const day = new Date().toISOString().slice(0, 10);
  const rows = await env.DB.prepare("SELECT k, n FROM counters WHERE k IN ('total', ?)").bind(`day:${day}`).all();
  const out = { total: 0, today: 0 };
  for (const r of rows.results) {
    if (r.k === "total") out.total = r.n;
    else out.today = r.n;
  }
  return out;
}

async function purgeOld(env) {
  // run at most a few times a day; cheap either way
  if (Math.random() > 0.05) return;
  const cutoff = new Date(Date.now() - 2 * 86400e3).toISOString().slice(0, 10);
  await env.DB.prepare("DELETE FROM seen WHERE day < ?").bind(cutoff).run();
}

async function sha256(s) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function json(obj, headers) {
  return new Response(JSON.stringify(obj), { status: 200, headers });
}
