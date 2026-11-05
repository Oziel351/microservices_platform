import { Router, Response, Request } from "express";
import { services } from "../services";
import { authToken } from "../../middleware/auth";
import { handleProxyError } from "../../utils/handleProxyError";

const router = Router();
const PREFIX = "/products";

router.get("/", authToken, async (req: Request, res: Response) => {
  try {
    const { data } = await services.products.get(PREFIX);
    res.status(200).json(data);
  } catch (err) {
    handleProxyError(res, err, "Error fetching products");
  }
});

router.get("/:id", authToken, async (req: Request, res: Response) => {
  try {
    const { data } = await services.products.get(
      `${PREFIX}/${encodeURIComponent(req.params.id as string)}`,
    );
    res.status(200).json(data);
  } catch (err) {
    handleProxyError(res, err, "Error fetching product");
  }
});

router.post("/", authToken, async (req: Request, res: Response) => {
  try {
    const { data } = await services.products.post(PREFIX, req.body);
    res.status(201).json(data);
  } catch (err) {
    handleProxyError(res, err, "Error creating product");
  }
});

router.put("/:id", authToken, async (req: Request, res: Response) => {
  try {
    const { data } = await services.products.put(
      `${PREFIX}/${encodeURIComponent(req.params.id as string)}`,
      req.body,
    );
    res.status(200).json(data);
  } catch (err) {
    handleProxyError(res, err, "Error updating product");
  }
});

router.delete("/:id", authToken, async (req: Request, res: Response) => {
  try {
    await services.products.delete(
      `${PREFIX}/${encodeURIComponent(req.params.id as string)}`,
    );
    res.status(204).send();
  } catch (err) {
    handleProxyError(res, err, "Error deleting product");
  }
});

export default router;
