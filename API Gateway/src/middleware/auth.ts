import { Response, NextFunction, Request } from "express";
import jwt from "jsonwebtoken";
import config from "../config";

export function authToken(req: Request, res: Response, next: NextFunction) {
  //Get token from request
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1];

  if (!token) {
    return res.status(401).json({ error: "No token in request" });
  }

  //Verify token and populate user
  jwt.verify(token, config.jwt, (err, user) => {
    if (err) {
      return res.status(403).json({ error: "Token invalido" });
    }
    const decoded = jwt.verify(token, config.jwt);

    req.user = decoded;
    next();
  });
}
