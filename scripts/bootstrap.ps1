param(
  [switch]$DryRun
)
$ErrorActionPreference = "Stop"

if ($env:LNM_HOME) {
  $RuntimeHome = $env:LNM_HOME
} elseif ($env:LOCALAPPDATA) {
  $RuntimeHome = Join-Path $env:LOCALAPPDATA "locution-narrative-map"
} else {
  $RuntimeHome = Join-Path $HOME ".locution-narrative-map"
}

$UvDir = Join-Path $RuntimeHome "uv"
$UvBin = Join-Path $UvDir "uv.exe"
$Venv = Join-Path $RuntimeHome "venv"
$PythonDir = Join-Path $RuntimeHome "python"
$CacheDir = Join-Path $RuntimeHome "cache"
$BinDir = Join-Path $RuntimeHome "bin"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
New-Item -ItemType Directory -Force -Path $UvDir,$PythonDir,$CacheDir,$BinDir | Out-Null

$env:UV_PYTHON_INSTALL_DIR = $PythonDir
$env:UV_CACHE_DIR = Join-Path $CacheDir "uv"
$env:HF_HOME = Join-Path $CacheDir "huggingface"
$env:XDG_CACHE_HOME = Join-Path $CacheDir "xdg"
$env:UV_NO_MODIFY_PATH = "1"

if ($DryRun) {
  Write-Output "runtime_home=$RuntimeHome"
  Write-Output "platform=Windows arch=$env:PROCESSOR_ARCHITECTURE"
  Write-Output "would_install_uv=$UvBin"
  Write-Output "would_create_venv=$Venv"
  Write-Output "backend=faster-whisper"
  exit 0
}

$Python = Join-Path $Venv "Scripts\python.exe"
$Manifest = Join-Path $RuntimeHome "runtime.json"
if ((Test-Path $Python) -and (Test-Path $Manifest)) {
  & $Python (Join-Path $ScriptDir "doctor.py") --home $RuntimeHome *> $null
  if ($LASTEXITCODE -eq 0) {
    Write-Output "Locution Narrative Map runtime: OK"
    exit 0
  }
}

if (-not (Test-Path $UvBin)) {
  Write-Output "Preparing local runtime..."
  $env:UV_UNMANAGED_INSTALL = $UvDir
  $env:UV_NO_MODIFY_PATH = "1"
  Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
}

& $UvBin venv --python 3.12 $Venv
$Python = Join-Path $Venv "Scripts\python.exe"
& $UvBin pip install --python $Python "imageio-ffmpeg==0.6.0" "numpy>=1.26,<3" "sherpa-onnx==1.13.4" "sherpa-onnx-bin==1.13.4" "faster-whisper==1.2.1"
& $Python (Join-Path $ScriptDir "configure_runtime.py") --home $RuntimeHome --backend "faster-whisper"
& $Python (Join-Path $ScriptDir "doctor.py") --home $RuntimeHome
