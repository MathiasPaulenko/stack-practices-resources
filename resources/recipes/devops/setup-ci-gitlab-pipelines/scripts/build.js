import { mkdirSync, copyFileSync, writeFileSync } from "node:fs";

mkdirSync("dist", { recursive: true });
copyFileSync("src/index.js", "dist/index.js");
writeFileSync(
  "dist/build-meta.json",
  JSON.stringify(
    {
      builtAt: new Date().toISOString(),
      pipeline: process.env.CI_PIPELINE_IID ?? "local",
      commit: process.env.CI_COMMIT_SHORT_SHA ?? "local"
    },
    null,
    2
  )
);
console.log("Built dist/index.js and dist/build-meta.json");
