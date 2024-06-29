
import { fileURLToPath } from "url";
import path from "path";
import { globSync } from "glob";
import fs from "fs";
import { execSync } from "child_process";


const __dirname = path.dirname(fileURLToPath(import.meta.url));
const distDir = path.join(path.dirname(path.dirname(__dirname)), "dist");

// clear mac cache files from distDir
for (var macTempFile of globSync(path.join(distDir, "**/._*"))) {
    fs.rmSync(macTempFile);
}
// clear python cache folders from distDir
for (var pyCacheDir of globSync(path.join(distDir, "**/__pycache__"))) {
    fs.rmSync(pyCacheDir, { recursive: true });
}

// create __init__.py file
fs.writeFileSync(path.join(distDir, "__init__.py"), "# -*- coding: utf-8 -*-\n");

// create qrc file
const qrcFileElements = [];
for (var qrcFilePath of globSync(path.join(distDir, "**/*.*"))) {
    const qrcFilePathName = path.basename(qrcFilePath);
    if (![ "svelte_dist.qrc", "svelte_dist.py", "__init__.py" ].includes(qrcFilePathName)) {
        qrcFileElements.push(`<file>${qrcFilePath.replace(distDir + path.sep, "")}</file>`);
    }
}
const qrcFile = path.join(distDir, "svelte_dist.qrc");
fs.writeFileSync(qrcFile, `<!DOCTYPE RCC>
<RCC version="1.0">
    <qresource>
        ${qrcFileElements.join("\n        ")}
    </qresource>
</RCC>`,
{ encoding: "utf-8" });

// compile qrc file
execSync(`pyside6-rcc ${qrcFile} -o ${path.join(distDir, "svelte_dist.py")}`);
