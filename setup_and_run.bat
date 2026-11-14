@echo off
setlocal
rem Reusable setup for an oomlout_oobb_part project. Run from any folder.
set "PROJECT_ROOT=%~dp0"
set "DEPENDENCY_ROOT=%PROJECT_ROOT%.dependencies"
set "VENV=%PROJECT_ROOT%.venv"
set "OOBB_REPO=%DEPENDENCY_ROOT%\oomlout_oobb_version_5"
set "OOMP_REPO=%DEPENDENCY_ROOT%\oomlout_oomp_version_5"
where git >nul 2>nul
if errorlevel 1 (echo ERROR: Install Git for Windows first.& exit /b 1)
if not exist "%DEPENDENCY_ROOT%" mkdir "%DEPENDENCY_ROOT%"
call :clone_or_update "https://github.com/oomlout/oomlout_oobb_version_5.git" "%OOBB_REPO%"
if errorlevel 1 exit /b 1
call :clone_or_update "https://github.com/oomlout/oomlout_oomp_version_5.git" "%OOMP_REPO%"
if errorlevel 1 exit /b 1
where py >nul 2>nul
if not errorlevel 1 (py -3 -m venv "%VENV%") else (python -m venv "%VENV%")
if errorlevel 1 exit /b 1
set "PYTHON=%VENV%\Scripts\python.exe"
"%PYTHON%" -m pip install --upgrade pip || exit /b 1
if exist "%PROJECT_ROOT%requirements.txt" "%PYTHON%" -m pip install -r "%PROJECT_ROOT%requirements.txt"
if errorlevel 1 exit /b 1
if exist "%OOBB_REPO%\requirements.txt" "%PYTHON%" -m pip install -r "%OOBB_REPO%\requirements.txt"
if errorlevel 1 exit /b 1
if exist "%OOMP_REPO%\requirements.txt" "%PYTHON%" -m pip install -r "%OOMP_REPO%\requirements.txt"
if errorlevel 1 exit /b 1
set "PYTHONPATH=%OOBB_REPO%;%OOMP_REPO%;%PYTHONPATH%"
call "%VENV%\Scripts\activate.bat"
pushd "%PROJECT_ROOT%"
if exist install_oobb_components.py "%PYTHON%" install_oobb_components.py
if errorlevel 1 (popd& exit /b 1)
if exist make_all.py (
  "%PYTHON%" make_all.py %*
) else if exist generate_all.bat (
  call generate_all.bat %*
) else if exist action_generate_all_no_click.py (
  "%PYTHON%" action_generate_all_no_click.py %*
) else if exist working.py (
  "%PYTHON%" working.py %*
) else (
  echo Dependencies are ready. No recognized build entry point was found.
  popd
  exit /b 0
)
set "BUILD_RESULT=%ERRORLEVEL%"
popd
exit /b %BUILD_RESULT%
:clone_or_update
if exist "%~2\.git" (
  git -C "%~2" config core.longpaths true
  if errorlevel 1 exit /b 1
  git -C "%~2" pull --ff-only
) else (
  if exist "%~2" (echo ERROR: %~2 exists but is not a Git checkout.& exit /b 1)
  git -c core.longpaths=true clone "%~1" "%~2"
)
exit /b %ERRORLEVEL%
