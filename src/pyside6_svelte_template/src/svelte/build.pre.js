
import { fileURLToPath } from "url";
import path from "path";
import fs from "fs";


const __dirname = path.dirname(fileURLToPath(import.meta.url));
fs.rmSync(path.join(path.dirname(path.dirname(__dirname)), "dist"), { recursive: true });
