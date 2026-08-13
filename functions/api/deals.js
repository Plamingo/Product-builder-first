// functions/api/deals.js
export async function onRequest(context) {
  const SUPABASE_URL = context.env.SUPABASE_URL;
  const SUPABASE_ANON_KEY = context.env.SUPABASE_ANON_KEY;

  if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
    return new Response(JSON.stringify({ error: "Supabase environment variables are missing on Cloudflare." }), {
      status: 500,
      headers: { "Content-Type": "application/json; charset=utf-8" },
    });
  }

  // Parse query parameters from request URL
  const requestUrl = new URL(context.request.url);
  const sggCd = requestUrl.searchParams.get("sggCd");
  const dealYear = requestUrl.searchParams.get("dealYear");

  // Construct Supabase PostgREST query
  let supabaseApiUrl = `${SUPABASE_URL.replace(/\/$/, '')}/rest/v1/apartment_deals?select=*&order=id.asc`;

  if (sggCd) {
    supabaseApiUrl += `&sggCd=eq.${encodeURIComponent(sggCd)}`;
  }

  if (dealYear && dealYear !== "ALL") {
    supabaseApiUrl += `&dealYear=eq.${encodeURIComponent(dealYear)}`;
  }

  try {
    const response = await fetch(supabaseApiUrl, {
      method: "GET",
      headers: {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": `Bearer ${SUPABASE_ANON_KEY}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      return new Response(JSON.stringify({ error: errorText }), {
        status: response.status,
        headers: { "Content-Type": "application/json; charset=utf-8" },
      });
    }

    const data = await response.json();
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-store",
      },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { "Content-Type": "application/json; charset=utf-8" },
    });
  }
}
