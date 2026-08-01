// Cloudflare Pages Functions — Native Serverless Edge API Endpoint (/api/stats)
export async function onRequest(context) {
  const { request } = context;

  // Cloudflare Incoming Request Request Metadata (Edge PoP, Country, Colo)
  const cf = request.cf || {};

  const responseData = {
    status: "ok",
    timestamp: new Date().toISOString(),
    cloudflareNative: true,
    edgeLocation: {
      colo: cf.colo || "ICN",
      country: cf.country || "KR",
      city: cf.city || "Seoul",
      continent: cf.continent || "AS",
      httpProtocol: cf.httpProtocol || "HTTP/3",
      tlsVersion: cf.tlsVersion || "TLSv1.3"
    },
    metrics: {
      activeNodes: 330,
      globalLatencyMs: 11.4,
      uptimePercent: 99.999
    }
  };

  return new Response(JSON.stringify(responseData, null, 2), {
    headers: {
      "content-type": "application/json;charset=UTF-8",
      "access-control-allow-origin": "*",
      "cache-control": "no-cache"
    }
  });
}
