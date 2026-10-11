#!/usr/bin/env node
// 读入 JSON: {"items":[{"id":0,"tex":"...","display":false}, ...]}
// 输出 JSON: {"0":"<svg .../>", ...}   —— 用 MathJax 把 LaTeX 转成自包含 SVG
const fs = require('fs');
const { mathjax } = require('mathjax-full/js/mathjax.js');
const { TeX } = require('mathjax-full/js/input/tex.js');
const { SVG } = require('mathjax-full/js/output/svg.js');
const { liteAdaptor } = require('mathjax-full/js/adaptors/liteAdaptor.js');
const { RegisterHTMLHandler } = require('mathjax-full/js/handlers/html.js');
const { AllPackages } = require('mathjax-full/js/input/tex/AllPackages.js');

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const tex = new TeX({ packages: AllPackages });
const svg = new SVG({ fontCache: 'local' });
const doc = mathjax.document('', { InputJax: tex, OutputJax: svg });

const input = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = {};
for (const it of input.items) {
  try {
    const node = doc.convert(it.tex, { display: !!it.display });
    let html = adaptor.outerHTML(node);
    // 清理：去掉 <mjx-container> 包装，只保留 <svg>
    const m = html.match(/<svg[\s\S]*<\/svg>/);
    out[it.id] = m ? m[0] : '';
    if (!m) out[it.id] = '';
  } catch (e) {
    out[it.id] = '';   // 渲染失败 -> 留空，由 Python 侧回退为纯文本
  }
}
fs.writeFileSync(process.argv[3], JSON.stringify(out));
