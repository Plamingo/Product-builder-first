// functions/config.js
export async function onRequest(context) {
  const SUPABASE_URL = context.env.SUPABASE_URL || "";
  const SUPABASE_ANON_KEY = context.env.SUPABASE_ANON_KEY || "";
  const TABLE_NAME = context.env.TABLE_NAME || "";

  const body = `export const SUPABASE_URL = ${JSON.stringify(SUPABASE_URL)};
export const SUPABASE_ANON_KEY = ${JSON.stringify(SUPABASE_ANON_KEY)};
export const TABLE_NAME = ${JSON.stringify(TABLE_NAME)};`;

  return new Response(body, {
    headers: {
      "Content-Type": "application/javascript; charset=utf-8",
      "Cache-Control": "no-store, no-cache, must-revalidate",
    },
  });
}
