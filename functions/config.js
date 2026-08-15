// functions/config.js

export async function onRequest(context) {
  // Cloudflare 대시보드에서 설정한 환경변수 객체 (context.env)
  const { SUPABASE_URL, SUPABASE_ANON_KEY } = context.env;

  // 클라이언트에 전달할 환경변수 데이터 객체 구성
  const configData = {
    SUPABASE_URL: SUPABASE_URL || "",
    SUPABASE_ANON_KEY: SUPABASE_ANON_KEY || "",
  };

  // JSON 형식으로 응답 반환
  return new Response(JSON.stringify(configData), {
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
      // 필요에 따라 CORS 헤더 추가 (필요시 도메인 제한 가능)
      "Access-Control-Allow-Origin": "*",
    },
  });
}

// export async function onRequest(context) {
//   const SUPABASE_URL = context.env.SUPABASE_URL || "";
//   const SUPABASE_ANON_KEY = context.env.SUPABASE_ANON_KEY || "";
//   const TABLE_NAME = context.env.TABLE_NAME || "";

//   const body = `export const SUPABASE_URL = ${JSON.stringify(SUPABASE_URL)};
// export const SUPABASE_ANON_KEY = ${JSON.stringify(SUPABASE_ANON_KEY)};
// export const TABLE_NAME = ${JSON.stringify(TABLE_NAME)};`;

//   return new Response(body, {
//     headers: {
//       "Content-Type": "application/javascript; charset=utf-8",
//       "Cache-Control": "no-store, no-cache, must-revalidate",
//     },
//   });
// }
