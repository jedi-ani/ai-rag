import { Router } from "express";
import { z } from "zod";

export const askRoute = Router();

const AskSchema = z.object({
  question: z.string().min(1).max(1000),
  temperature: z.number().min(0).max(2).default(0.2),
  top_k: z.number().int().min(1).max(20).default(6),
});

askRoute.post("/ask", async (req, res) => {
  const parsed = AskSchema.safeParse(req.body);

  if (!parsed.success) {
    return res.status(400).json({ error: "Invalid request" });
  }

  const response = await fetch(
    `${process.env.PYTHON_API_URL ?? "http://localhost:8000"}/ask`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(parsed.data),
    }
  );

  if (!response.ok) {
    return res.status(502).json({ error: "RAG service unavailable" });
  }

  return res.json(await response.json());
});