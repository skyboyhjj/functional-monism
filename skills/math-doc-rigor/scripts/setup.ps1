# 环境准备（Windows）：Python 依赖（markdown2 / weasyprint）+ MathJax（node）
$ErrorActionPreference = "Stop"
$HERE = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "[1/3] Python 依赖 markdown2 / weasyprint ..."
python -m pip install --quiet markdown2 weasyprint
if ($LASTEXITCODE -ne 0) { py -m pip install --quiet markdown2 weasyprint }

Write-Host "[2/3] 校验 weasyprint 可导入 ..."
python -c "import weasyprint" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [!] weasyprint 导入失败：通常缺 GTK3 运行时 (libgobject-2.0-0.dll)。"
    Write-Host "      安装 MSYS2 后执行: pacman -S mingw-w64-x86_64-gtk3"
    Write-Host "      或将 PATH 指向已安装的 GTK 库目录；也可改用 WSL/Linux 环境导出 PDF。"
}

Write-Host "[3/3] MathJax (node) ..."
if (-not (Test-Path "$HERE\node_modules\mathjax-full")) {
    Push-Location $HERE
    try {
        npm init -y *> $null
        npm install --silent mathjax-full
    } finally { Pop-Location }
}

Write-Host ""
Write-Host "完成。导出 PDF 时用："
Write-Host "  set MATHJAX_NODE_PATH=$HERE\node_modules"
Write-Host "  python $HERE\md2pdf.py --outdir pdf 文档.md"