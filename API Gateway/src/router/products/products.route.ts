import { Router, Response, Request } from "express";
import { services } from "../services";

const router = Router();
const PREFIX = "/products";

router.get("/", async (req: Request, res: Response) => {
  try {
    const { data } = await services.products.get(PREFIX);
    res.status(200).json(data);
  } catch (err) {
    res.status(500).json({ error: "Error fetching products" });
  }
});

router.get("/:id", async (req: Request, res: Response) => {
  try {
    const { data } = await services.products.get(`${PREFIX}/${req.params.id}`);
    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: "Error fetching product" });
  }
});

router.post("/", async (req: Request, res: Response) => {
  try {
    const { data } = await services.products.post(PREFIX, req.body);
    res.status(201).json(data);
  } catch (err) {
    res.status(500).json({ error: "Error creating product" });
  }
});

router.put("/:id", async (req: Request, res: Response) => {
  try {
    const { data } = await services.products.put(
      `${PREFIX}/${req.params.id}`,
      req.body,
    );
    res.status(200).json(data);
  } catch (err) {
    res.status(500).json({ erro: "Error updating product" });
  }
});

router.delete("/:id", async (req: Request, res: Response) => {
  try {
    await services.products.delete(`${PREFIX}/${req.params.id}`);

    res.status(204).send();
  } catch (err) {
    res.status(500).json({ error: "Error deleting product" });
  }
});

export default router;
