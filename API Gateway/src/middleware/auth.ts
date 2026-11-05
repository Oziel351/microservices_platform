import { Response, NextFunction, Request } from "express";
import jwt from "jsonwebtoken";
import config from "../config";
import { isAuthPayload } from "../types/auth";

export function authToken(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers["authorization"];

  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return res.status(401).json({ error: "Missing or malformed token" });
  }

  const token = authHeader.split(" ")[1];

  if (!token) {
    return res.status(401).json({ error: "No token in request" });
  }

  try {
    const decoded = jwt.verify(token, config.jwtToken, {
      algorithms: ["HS256"],
    });

    // A valid signature does not guarantee the payload has the shape we expect.
    if (!isAuthPayload(decoded)) {
      return res.status(401).json({ error: "Invalid token" });
    }

    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: "Invalid token" });
  }
}
