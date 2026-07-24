import { NextRequest, NextResponse } from "next/server";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "http://127.0.0.1:55321";
const publishableKey = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? "";

export async function proxy(request: NextRequest) {
  const accessToken = request.cookies.get("oslo_access_token")?.value;
  const refreshToken = request.cookies.get("oslo_refresh_token")?.value;
  if (accessToken || !refreshToken) return NextResponse.next();

  const refresh = await fetch(`${supabaseUrl}/auth/v1/token?grant_type=refresh_token`, {
    method: "POST",
    headers: { apikey: publishableKey, "content-type": "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });
  if (!refresh.ok) {
    const response = NextResponse.redirect(new URL("/login", request.url));
    response.cookies.delete("oslo_access_token");
    response.cookies.delete("oslo_refresh_token");
    return response;
  }

  const session = await refresh.json();
  const requestHeaders = new Headers(request.headers);
  const requestCookies = request.cookies;
  requestCookies.set("oslo_access_token", session.access_token);
  requestCookies.set("oslo_refresh_token", session.refresh_token);
  requestHeaders.set("cookie", requestCookies.toString());
  const response = NextResponse.next({ request: { headers: requestHeaders } });
  const common = {
    httpOnly: true,
    sameSite: "lax" as const,
    secure: process.env.NODE_ENV === "production",
    path: "/",
  };
  response.cookies.set("oslo_access_token", session.access_token, {
    ...common,
    maxAge: session.expires_in,
  });
  response.cookies.set("oslo_refresh_token", session.refresh_token, {
    ...common,
    maxAge: Number(request.cookies.get("oslo_session_lifetime")?.value) || 60 * 60 * 24,
  });
  return response;
}

export const config = {
  matcher: [
    "/admin/:path*",
    "/welcome",
    "/intake",
    "/projects/:path*",
    "/api/analysis-runs/:path*",
    "/api/projects/:path*",
    "/api/orientation",
  ],
};
