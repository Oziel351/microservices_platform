import { JwtPayload } from "jsonwebtoken";

//By default the type of Request doesn't include user prop so we extended.
declare global {
  namespace Express {
    interface Request {
      user?: string | JwtPayload;
    }
  }
}
