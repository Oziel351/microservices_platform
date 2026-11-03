import { Router, Response, Request } from "express";
import { services } from "../services";

const router = Router();

router.get("/", async (req: Request, res: Response) => {
  try {
    const { data } = await services.users.get("/users");
    res.status(200).json(data);
  } catch (err) {
    res.status(500).json({ error: "Error fetching users" });
  }
});

router.get("/:id", async (req: Request, res: Response) => {
  try {
    const { data } = await services.users.get(`/users/${req.params.id}`);
    res.status(200).json(data);
  } catch (err) {
    res.status(500).json({ error: "Error fetching user" });
  }
});

router.post("/", async (req: Request, res: Response) => {
  try {
    const { data } = await services.users.post("/users", req.body);
    res.status(201).json(data);
  } catch (err) {
    res.status(500).json({ error: "Error creating user" });
  }
});

router.put("/:id", async (req: Request, res: Response) => {
  try {
    const { data } = await services.users.put(
      `/users/${req.params.id}`,
      req.body,
    );
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: "Error updating user" });
  }
});

router.delete("/:id", async (req: Request, res: Response) => {
  try {
    await services.users.delete(`/users/${req.params.id}`);
    res.status(204).send();
  } catch (err) {
    res.status(500).json({ error: "Error deleting user" });
  }
});

export default router;
