<#
run_migrations.ps1

Usage:
  1. Open PowerShell in the project folder:
     C:\Users\Enimofe Toyosi\OneDrive\Documents\altclan-brands-api-1.1

  2. If your ExecutionPolicy blocks scripts, this script will set CurrentUser policy to RemoteSigned (safe for local development).

  3. Run the script:
     .\run_migrations.ps1

What it does:
  - Ensures a virtualenv exists (.venv preferred, falls back to venv)
  - Sets ExecutionPolicy for CurrentUser to RemoteSigned (so Activate.ps1 can run)
  - Activates the venv in the current session (dot-sourcing the Activate.ps1)
  - Upgrades pip and installs requirements.txt (falls back to installing Django if requirements fail)
  - Loads environment variables from a .env file in the project root (if present)
  - Prompts to confirm that you have a DB backup
  - Runs `python manage.py makemigrations` and `python manage.py migrate` and `python manage.py collectstatic` (collectstatic optional)

Important:
  - DO NOT run this against production without a DB backup.
  - This script does not contain any secrets. Use a .env file to provide SECRET_KEY, DATABASE_URL, REDIS_URL, etc.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "Running migration helper script..." -ForegroundColor Cyan

# Determine project root (script location)
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location -Path $projectRoot

# Choose venv folder name
$venvNames = @('.venv','venv')
$venvPath = $null
foreach ($n in $venvNames) {
    if (Test-Path (Join-Path $projectRoot $n)) { $venvPath = Join-Path $projectRoot $n; break }
}

if (-not $venvPath) {
    # create .venv by default
    $venvPath = Join-Path $projectRoot '.venv'
    Write-Host "Creating virtual environment at: $venvPath" -ForegroundColor Yellow
    python -m venv $venvPath
}
else {
    Write-Host "Found existing virtualenv at: $venvPath" -ForegroundColor Green
}

# Ensure ExecutionPolicy allows running local activation scripts (CurrentUser only)
try {
    $currentPolicy = Get-ExecutionPolicy -Scope CurrentUser -ErrorAction SilentlyContinue
    if ($currentPolicy -ne 'RemoteSigned' -and $currentPolicy -ne 'Unrestricted') {
        Write-Host "Setting ExecutionPolicy for CurrentUser to RemoteSigned (allows local activation scripts)" -ForegroundColor Yellow
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    } else {
        Write-Host "ExecutionPolicy for CurrentUser is $currentPolicy" -ForegroundColor Green
    }
} catch {
    Write-Warning "Could not set ExecutionPolicy automatically. If activation fails, run PowerShell as Administrator or set the policy manually: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned"
}

# Activate the venv in the current session (dot-source the Activate.ps1)
$activateScript = Join-Path $venvPath 'Scripts\Activate.ps1'
if (-not (Test-Path $activateScript)) {
    Write-Error "Activate script not found at $activateScript. Virtualenv may not have been created correctly.";
    exit 1
}

Write-Host "Activating virtualenv: $activateScript" -ForegroundColor Cyan
. $activateScript

# Helper: run a command and show output
function Run-Command($exe, $args) {
    Write-Host "Running: $exe $args" -ForegroundColor DarkCyan
    & $exe $args
}

# Upgrade pip
try {
    Write-Host "Upgrading pip..." -ForegroundColor Cyan
    Run-Command python "-m pip install --upgrade pip"
} catch {
    Write-Warning "Failed to upgrade pip: $_"
}

# Install requirements if file exists
$requirements = Join-Path $projectRoot 'requirements.txt'
$requirementsInstalled = $false
if (Test-Path $requirements) {
    try {
        Write-Host "Installing requirements from requirements.txt (this may take several minutes)..." -ForegroundColor Cyan
        Run-Command python "-m pip install -r `"$requirements`""
        $requirementsInstalled = $true
    } catch {
        Write-Warning "Installing requirements failed: $_"
        Write-Warning "Falling back to installing Django only (you may need to install additional packages manually)."
    }
} else {
    Write-Host "No requirements.txt found — installing Django only." -ForegroundColor Yellow
}

if (-not $requirementsInstalled) {
    try {
        Run-Command python "-m pip install Django"
    } catch {
        Write-Error "Failed to install Django. Resolve pip/build errors (for example install Visual C++ Build Tools) and re-run this script.";
        exit 1
    }
}

# Load .env into current process environment (if exists)
$envFile = Join-Path $projectRoot '.env'
if (Test-Path $envFile) {
    Write-Host "Found .env file — loading environment variables into session (will not persist to system)." -ForegroundColor Cyan
    Get-Content $envFile | ForEach-Object {
        $line = $_.Trim()
        if ($line -eq '' -or $line.StartsWith('#')) { return }
        if ($line -match '^(.*?)=(.*)$') {
            $k = $matches[1].Trim()
            $v = $matches[2].Trim() -replace '(^\"|\"$)','' -replace "(^')|('$)",''
            # Expand variables like ${VAR}
            $v = $v -replace '\$\{([^}]+)\}', { param($m) $env:$($m.Groups[1].Value) }
            Write-Host "Setting env $k" -ForegroundColor DarkGray
            $env:$k = $v
        }
    }
} else {
    Write-Host "No .env file found. Ensure SECRET_KEY, DATABASE_URL, and other env vars are available in the environment before running migrations." -ForegroundColor Yellow
}

# Confirm DB backup
$confirm = Read-Host "Have you backed up your database (required). Type 'yes' to continue"
if ($confirm -ne 'yes') {
    Write-Host "Migration aborted. Please backup your DB and re-run this script once ready." -ForegroundColor Red
    exit 1
}

# Run Django makemigrations/migrate
try {
    Write-Host "Running makemigrations..." -ForegroundColor Cyan
    Run-Command python "manage.py makemigrations"
} catch {
    Write-Warning "makemigrations failed or there are no changes: $_"
}

try {
    Write-Host "Running migrate..." -ForegroundColor Cyan
    Run-Command python "manage.py migrate"
} catch {
    Write-Error "migrate failed: $_"
    exit 1
}

# Optionally collect static files
$collect = Read-Host "Run collectstatic now? Type 'yes' to run, anything else to skip"
if ($collect -eq 'yes') {
    try {
        Write-Host "Running collectstatic..." -ForegroundColor Cyan
        Run-Command python "manage.py collectstatic --noinput"
    } catch {
        Write-Warning "collectstatic failed: $_"
    }
}

Write-Host "Migrations completed successfully (or exited with warnings). Verify your application and run tests as needed." -ForegroundColor Green
Write-Host "If you ran this in VS Code integrated terminal, you may need to restart the terminal/session for env changes to persist in new shells." -ForegroundColor Yellow
