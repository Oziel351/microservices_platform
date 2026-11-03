import express, { Request, Response } from "express";
import cors from "cors";
import productsRouter from "./router/products/products.route";
import usersRouter from "./router/users/users.route";

const app = express();

app.use(cors());
app.use(express.json());

//Basic check health endpoint
app.get("/health", (req: Request, res: Response) => {
  res.status(200).json({
    status: "ok",
    service: "api-gateway",
    timeStamp: new Date().toISOString(),
  });
});

//Use per-service limiters to ensure resource management for each
//Can add more and more services, also create a file to manate all the routes instead of
app.use("/api/products", productsRouter);
app.use("/api/users", usersRouter);

export default app;
