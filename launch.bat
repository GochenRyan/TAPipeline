@echo off
setlocal enabledelayedexpansion

rem ============================================================
rem TAPipeline launcher for Maya 2026
rem  1. Reads config\maya2026_env.ini (KEY=VALUE, # comments)
rem  2. Sets MAYA_MODULE_PATH so Maya finds TAPipeline.mod
rem  3. Syncs Python dependencies into toolkit\Maya2026\python\3.11
rem  4. Launches maya.exe
rem ============================================================

set "REPO_ROOT=%~dp0"
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

set "ENV_INI=%REPO_ROOT%\config\maya2026_env.ini"
set "TOOLKIT_ROOT=%REPO_ROOT%\toolkit\Maya2026"
set "PY_SITE=%TOOLKIT_ROOT%\python\3.11"
set "REQS=%TOOLKIT_ROOT%\requirements.txt"

if not exist "%ENV_INI%" (
    echo [TAPipeline] ERROR: Missing config file: %ENV_INI%
    pause
    exit /b 1
)

rem --- Load KEY=VALUE pairs from the ini ---
for /f "usebackq eol=# tokens=1,* delims==" %%A in ("%ENV_INI%") do (
    if not "%%A"=="" set "%%A=%%B"
)

if not defined MAYA_LOCATION (
    echo [TAPipeline] ERROR: MAYA_LOCATION not set in %ENV_INI%
    pause
    exit /b 1
)

if not exist "%MAYA_LOCATION%\bin\maya.exe" (
    echo [TAPipeline] ERROR: maya.exe not found under "%MAYA_LOCATION%\bin"
    echo                Edit MAYA_LOCATION in %ENV_INI%.
    pause
    exit /b 1
)

set "MAYA_MODULE_PATH=%TOOLKIT_ROOT%"

rem --- Sync third-party Python deps on every launch ---
if exist "%REQS%" (
    if not exist "%PY_SITE%" mkdir "%PY_SITE%"
    if exist "%MAYA_LOCATION%\bin\mayapy.exe" (
        echo [TAPipeline] Syncing Python dependencies into "%PY_SITE%"...
        "%MAYA_LOCATION%\bin\mayapy.exe" -m pip install ^
            -r "%REQS%" ^
            -t "%PY_SITE%" ^
            --upgrade ^
            --disable-pip-version-check ^
            --quiet
        if errorlevel 1 (
            echo [TAPipeline] WARN: dependency sync failed; launching anyway.
        ) else (
            echo [TAPipeline] Dependencies up to date.
        )
    ) else (
        echo [TAPipeline] WARN: mayapy.exe not found; skipping dependency sync.
    )
)

echo [TAPipeline] MAYA_MODULE_PATH=%MAYA_MODULE_PATH%
echo [TAPipeline] Launching Maya 2026...
"%MAYA_LOCATION%\bin\maya.exe" %*

endlocal
