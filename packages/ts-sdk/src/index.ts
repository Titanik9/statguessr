export type MagicLinkRequest = {
  email: string;
  workspace_slug?: string;
};

export type MagicLinkResponse = {
  message: string;
  expires_at: string;
  preview_url?: string | null;
};

export type SessionResponse = {
  session_token: string;
  expires_at: string;
  user: {
    id: string;
    email: string;
    display_name?: string | null;
  };
};

export type WorkspaceMember = {
  id: string;
  role: string;
  user: {
    id: string;
    email: string;
    display_name?: string | null;
  };
  workspace: {
    id: string;
    name: string;
    slug: string;
    plan_tier: string;
  };
};

export type CreateWorkspaceRequest = {
  name: string;
  slug: string;
};

export type CreateApiKeyRequest = {
  label: string;
  scopes?: string[];
  expires_at?: string | null;
};

export type CreateApiKeyResponse = {
  api_key: {
    id: string;
    label: string;
    key_prefix: string;
    created_at: string;
    revoked_at?: string | null;
  };
  secret: string;
};

type ClientOptions = {
  baseUrl: string;
  sessionToken?: string;
  apiKey?: string;
};

export class RelayClient {
  private readonly baseUrl: string;
  private readonly sessionToken?: string;
  private readonly apiKey?: string;

  constructor(options: ClientOptions) {
    this.baseUrl = options.baseUrl.replace(/\/$/, "");
    this.sessionToken = options.sessionToken;
    this.apiKey = options.apiKey;
  }

  private async request<T>(path: string, init: RequestInit = {}): Promise<T> {
    const headers = new Headers(init.headers);
    headers.set("content-type", "application/json");
    if (this.sessionToken) {
      headers.set("authorization", `Bearer ${this.sessionToken}`);
    }
    if (this.apiKey) {
      headers.set("x-relay-key", this.apiKey);
    }

    const response = await fetch(`${this.baseUrl}${path}`, {
      ...init,
      headers,
    });

    if (!response.ok) {
      const payload = (await response.json().catch(() => ({}))) as { detail?: string };
      throw new Error(payload.detail ?? `Request failed with status ${response.status}`);
    }

    return response.json() as Promise<T>;
  }

  requestMagicLink(payload: MagicLinkRequest) {
    return this.request<MagicLinkResponse>("/auth/magic-links/request", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  verifyMagicLink(token: string) {
    return this.request<SessionResponse>("/auth/magic-links/verify", {
      method: "POST",
      body: JSON.stringify({ token }),
    });
  }

  listWorkspaces() {
    return this.request<{ items: WorkspaceMember[] }>("/workspaces");
  }

  createWorkspace(payload: CreateWorkspaceRequest) {
    return this.request<WorkspaceMember>("/workspaces", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  createApiKey(workspaceId: string, payload: CreateApiKeyRequest) {
    return this.request<CreateApiKeyResponse>(`/workspaces/${workspaceId}/api-keys`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }
}
