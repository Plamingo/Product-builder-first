// functions/config.js
export async function onRequest(context) {
  const SUPABASE_URL = context.env.SUPABASE_URL || "";
  const SUPABASE_ANON_KEY = context.env.SUPABASE_ANON_KEY || "";

  // 디버깅용 서버 로그 (Cloudflare 대시보드 Real-time Logs에 출력됨)
  console.log("SUPABASE_URL:", SUPABASE_URL);

  const body = `export const SUPABASE_URL = ${JSON.stringify(SUPABASE_URL)};
export const SUPABASE_ANON_KEY = ${JSON.stringify(SUPABASE_ANON_KEY)};`;

  return new Response(body, {
    headers: {
      "Content-Type": "application/javascript; charset=utf-8",
      "Cache-Control": "no-store, no-cache, must-revalidate",
    },
  });
}
