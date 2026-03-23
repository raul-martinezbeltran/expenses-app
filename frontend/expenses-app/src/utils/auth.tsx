const ACCESS_TOKEN_KEY = "access_token";
const TOKEN_TYPE_KEY = "token_type";

export type LoginResponse = {
  access_token: string;
  token_type: string;
};

export function saveAuthTokens(tokenData: LoginResponse) {
  localStorage.setItem(ACCESS_TOKEN_KEY, tokenData.access_token);
  localStorage.setItem(TOKEN_TYPE_KEY, tokenData.token_type);
}

export function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getTokenType(): string {
  return localStorage.getItem(TOKEN_TYPE_KEY) || "bearer";
}

export function clearAuthTokens() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(TOKEN_TYPE_KEY);
}

export function isAuthenticated(): boolean {
  return !!localStorage.getItem("access_token");
}

export function getAuthHeader(): HeadersInit {
  const token = getAccessToken();
  const tokenType = getTokenType();

  if (!token) {
    return {};
  }

  return {
    Authorization: `${tokenType} ${token}`,
  };
}

export async function authFetch(
  url: string,
  options: RequestInit = {},
): Promise<Response> {
  const headers = new Headers(options.headers || {});
  const authHeaders = getAuthHeader();

  Object.entries(authHeaders).forEach(([key, value]) => {
    headers.set(key, value);
  });

  return fetch(url, {
    ...options,
    headers,
  });
}
