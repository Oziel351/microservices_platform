import { Response } from "express";
import { isAxiosError } from "axios";

/**
 * Translates an error thrown while calling a downstream service
 * into the right HTTP response for the gateway's client.
 *
 * - The service answered with an error (404, 422, ...): forward it as-is.
 * - The service timed out: 504 Gateway Timeout.
 * - The service is unreachable (down, connection refused): 503 Service Unavailable.
 * - Anything else is a bug in the gateway itself: 500.
 */
export function handleProxyError(
  res: Response,
  error: unknown,
  fallbackMessage: string,
) {
  if (isAxiosError(error)) {
    if (error.response) {
      return res.status(error.response.status).json(error.response.data);
    }

    if (error.code === "ECONNABORTED" || error.code === "ETIMEDOUT") {
      return res.status(504).json({ error: "Upstream service timed out" });
    }

    return res.status(503).json({ error: "Upstream service unavailable" });
  }

  console.error(fallbackMessage, error);
  return res.status(500).json({ error: fallbackMessage });
}
