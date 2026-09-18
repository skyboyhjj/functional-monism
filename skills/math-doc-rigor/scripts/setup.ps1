# 环境准备（Windows PowerShell）：Python 依赖（markdown2 / weasyprint）+ MathJax
# 用法：在 scripts 目录下执行  powershell -ExecutionPolicy Bypass -File setup.ps1

$HERE = Split-Path -Parent $MyInvocation.MyCommand.Path

function Get-PyCmd {
    if (Get-Command py -ErrorAction SilentlyContinue) { return "py" }
    return "python"
}
$PY = Get-PyCmd

Write-Host "[1/3] 检查 Python / Node ..."
& $PY --version
node --version

Write-Host "`n[2/3] Python 依赖 markdown2 / weasyprint / fonttools ...（若失败见下方说明）"
& $PY -m pip install --quiet --disable-pip-version-check markdown2 weasyprint fonttools

Write-Host "`n[3/3] MathJax (node) ..."
$mj = Join-Path $HERE "node_modules\mathjax-full"
if (-not (Test-Path $mj)) {
    Push-Location $HERE
    npm init -y | Out-Null
    npm install --silent mathjax-full
    Pop-Location
}

Write-Host "`n---- 自检 ----"
& $PY -c "import markdown2; print('markdown2 : OK')"

& $PY -c "import weasyprint; print('weasyprint: OK')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "weasyprint: 不可用（Windows 上通常缺 GTK3 运行库，报 libgobject-2.0-0.dll 找不到）"
    Write-Host ""
    Write-Host "  两种处理方式："
    Write-Host "   A) 直接不管 —— md2pdf.py 会自动回退到 headless Edge/Chrome 导出 PDF（无需 GTK）；"
    Write-Host "   B) 想用 weasyprint —— 先安装 GTK3 运行库（如 tschoonj/GTK-for-Windows-Runtime-Environment-Installer），再重跑本脚本。"
} else {
    Write-Host "weasyprint: OK"
}

Write-Host "`n---- 完成 ----"
Write-Host "导出 PDF："
Write-Host "  `$env:MATHJAX_NODE_PATH = `"$HERE\node_modules`""
Write-Host "  & `"$PY`" `"$HERE\md2pdf.py`" --outdir pdf 文档.md"
