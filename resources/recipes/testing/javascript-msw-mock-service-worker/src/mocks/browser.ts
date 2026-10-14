import { setupWorker } from "msw/browser";
import { handlers } from "./handlers";

// Run `npx msw init public/ --save` once to generate mockServiceWorker.js
export const worker = setupWorker(...handlers);
