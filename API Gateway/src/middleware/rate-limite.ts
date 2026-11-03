import { createLimiter, rateLimiterConfigs } from "../core/rate-limiter";

export const globalLimiter = createLimiter(rateLimiterConfigs.global);
export const productsLimiter = createLimiter(rateLimiterConfigs.products);
export const usersLimiter = createLimiter(rateLimiterConfigs.users);
