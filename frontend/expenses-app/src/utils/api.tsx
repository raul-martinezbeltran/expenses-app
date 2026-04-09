import {
  saveAuthTokens,
  type LoginResponse,
  authFetch,
  clearAuthTokens,
} from "./auth";

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export type SignupPayload = {
  username: string;
  email: string;
  full_name: string;
  password: string;
};

export type CreateExpensePayload = {
  name: string;
  amount: string;
};

export type UserResponse = {
  user_id: number;
  username: string;
  email: string;
  full_name: string;
  disabled: boolean;
};

type ApiError = {
  detail?: string;
  message?: string;
};

async function parseJsonSafe(response: Response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

export async function signupUser(payload: SignupPayload) {
  const formData = new FormData();
  formData.append("username", payload.username);
  formData.append("email", payload.email);
  formData.append("full_name", payload.full_name);
  formData.append("password", payload.password);

  const response = await fetch(`${API_BASE_URL}/users/signup`, {
    method: "POST",
    body: formData,
  });

  const data = await parseJsonSafe(response);

  if (!response.ok) {
    throw new Error(data?.detail || "Signup failed");
  }

  return data;
}

export async function loginUser(username: string, password: string) {
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);

  const response = await fetch(`${API_BASE_URL}/users/token`, {
    method: "POST",
    body: formData,
  });

  const data = (await parseJsonSafe(response)) as
    | LoginResponse
    | ApiError
    | null;

  if (!response.ok || !data || !("access_token" in data)) {
    throw new Error((data as ApiError)?.detail || "Login failed");
  }

  saveAuthTokens(data);
  return data;
}

export async function signupAndLogin(payload: SignupPayload) {
  await signupUser(payload);
  return loginUser(payload.username, payload.password);
}

export async function getCurrentUser(): Promise<UserResponse> {
  const response = await authFetch(`${API_BASE_URL}/users/me`, {
    method: "GET",
  });

  const data = await parseJsonSafe(response);

  if (!response.ok) {
    if (response.status === 401) {
      clearAuthTokens();
    }
    throw new Error(data?.detail || "Failed to fetch current user");
  }

  return data as UserResponse;
}

export async function createExpense(payload: CreateExpensePayload) {
  const formData = new FormData();
  formData.append("name", payload.name);
  formData.append("amount", payload.amount);

  const response = await authFetch(`${API_BASE_URL}/expenses/create_expense`, {
    method: "POST",
    body: formData,
  });

  const data = await parseJsonSafe(response);

  if (!response.ok) {
    if (response.status === 401) {
      clearAuthTokens();
    }
    throw new Error(
      data?.detail || data?.message || "Failed to create expense",
    );
  }

  return data;
}
