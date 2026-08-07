param(
  [Parameter(ValueFromRemainingArguments=$true)]
  [string[]]$ArgsList
)
$ErrorActionPreference = "Stop"
if ($env:LNM_HOME) { $RuntimeHome = $env:LNM_HOME }
elseif ($env:LOCALAPPDATA) { $RuntimeHome = Join-Path $env:LOCALAPPDATA "locution-narrative-map" }
else { $RuntimeHome = Join-Path $HOME ".locution-narrative-map" }
$Python = Join-Path $RuntimeHome "venv\Scripts\python.exe"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path $Python)) {
  & (Join-Path $ScriptDir "bootstrap.ps1")
}
& $Python (Join-Path $ScriptDir "cli.py") --home $RuntimeHome @ArgsList
exit $LASTEXITCODE
