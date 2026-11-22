import express from "express";
import cors from "cors";
import { askRoute } from "./routes/ask";

const app = express();

app.use(cors({ origin: process.env.WEB_ORIGIN ?? "http://localhost:5173" }));
app.use(express.json());

app.use("/api", askRoute);

app.listen(process.env.PORT ?? 4000, () => {
  console.log(`API running on port ${process.env.PORT ?? 4000}`);
});