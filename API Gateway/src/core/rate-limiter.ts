import rateLimit, { RateLimitRequestHandler } from "express-rate-limit";

// Rate limit at top level of the microservices to manage how many requests should
// the the user can make in different services.

export interface ServiceRateLimitConfig {
  windowMs: number;
  max: number;
  message: string;
}

const WINDOW_MS = parseInt(
  process.env.RATE_LIMIT_WINDOW_MS ?? String(15 * 60 * 1000),
);

export const rateLimiterConfigs: Record<string, ServiceRateLimitConfig> = {
  global: {
    windowMs: WINDOW_MS,
    max: parseInt(process.env.RATE_LIMIT_GLOBAL ?? "500"),
    message: "Too many requests, please try again later.",
  },
  products: {
    windowMs: WINDOW_MS,
    max: parseInt(process.env.RATE_LIMIT_PRODUCTS ?? "300"),
    message:
      "Too many requests to the products service, please try again later.",
  },
  users: {
    windowMs: WINDOW_MS,
    max: parseInt(process.env.RATE_LIMIT_USERS ?? "100"),
    message: "Too many requests to the users service, please try again later.",
  },
};

export function createLimiter(
  config: ServiceRateLimitConfig,
): RateLimitRequestHandler {
  return rateLimit({
    windowMs: config.windowMs,
    max: config.max,
    message: { error: config.message },
    standardHeaders: true,
    legacyHeaders: false,
  });
}
