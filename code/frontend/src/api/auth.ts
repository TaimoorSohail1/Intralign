import axios, { type InternalAxiosRequestConfig } from "axios";

const TOKEN_STORAGE_KEY = "oslo.demo.accessToken";
const DEMO_EMAIL = "admin@oslo.com";
const DEMO_PASSWORD = "oslo123456";

let pendingToken: Promise<string> | null = null;

type LoginResponse = {
  access_token?: string;
  token_type?: string;
};

function shouldAttachAuth(config: InternalAxiosRequestConfig): boolean {
  const url = config.url ?? "";
  return url.startsWith("/v1/");
}

async function fetchDemoToken(): Promise<string> {
  const cached = window.localStorage.getItem(TOKEN_STORAGE_KEY);
  if (cached) return cached;

  pendingToken ??= axios
    .post<LoginResponse>("/auth/login", {
      email: DEMO_EMAIL,
      password: DEMO_PASSWORD,
    })
    .then((response) => {
      const token = response.data.access_token;
      if (!token) {
        throw new Error("OSLO login did not return an access token");
      }
      window.localStorage.setItem(TOKEN_STORAGE_KEY, token);
      return token;
    })
    .finally(() => {
      pendingToken = null;
    });

  return pendingToken;
}

export function configureApiAuth(): void {
  axios.interceptors.request.use(async (config) => {
    if (!shouldAttachAuth(config)) return config;

    const token = await fetchDemoToken();
    config.headers.Authorization = `Bearer ${token}`;
    return config;
  });

  axios.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error?.response?.status === 401) {
        window.localStorage.removeItem(TOKEN_STORAGE_KEY);
      }
      return Promise.reject(error);
    },
  );
}
