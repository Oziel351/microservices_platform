export interface AuthPayload {
  id: string;
  email: string;
  /**To be defined */
  role: string;
}

/**
 * Runtime check for the shape of a verified JWT payload that I need.
 */
export function isAuthPayload(value: unknown): value is AuthPayload {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const payload = value as Record<string, unknown>;

  return (
    typeof payload.id === "string" &&
    typeof payload.email === "string" &&
    typeof payload.role === "string"
  );
}
