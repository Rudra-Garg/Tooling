@echo off
:: Minecraft Mod Updater - Batch File Launcher
:: This batch file helps run the Minecraft Mod Updater script with common options

echo Minecraft Mod Updater (Modrinth Only) - FABRIC VERSION
echo ----------------------------------------

:: Always use Fabric loader
set ARGS=--loader fabric

:MENU
echo.
echo Select an option:
echo 1. Run with default settings
echo 2. Specify Minecraft version
echo 3. Specify mods directory
echo 4. Skip backups
echo 5. Advanced options (specify all parameters)
echo 6. Exit
echo.

set /p CHOICE="Enter your choice (1-6): "

if "%CHOICE%"=="1" goto RUN
if "%CHOICE%"=="2" goto VERSION
if "%CHOICE%"=="3" goto MODS_DIR
if "%CHOICE%"=="4" goto SKIP_BACKUP
if "%CHOICE%"=="5" goto ADVANCED
if "%CHOICE%"=="6" goto END

echo Invalid choice. Please try again.
goto MENU

:VERSION
set /p MC_VERSION="Enter Minecraft version (e.g., 1.20.1): "
set ARGS=%ARGS% --minecraft-version "%MC_VERSION%"
goto RUN

:MODS_DIR
set /p MODS_PATH="Enter path to mods directory: "
set ARGS=%ARGS% --mods-dir "%MODS_PATH%"
goto RUN

:SKIP_BACKUP
set ARGS=%ARGS% --no-backup
goto RUN

:ADVANCED
set /p MC_VERSION="Enter Minecraft version (leave blank to skip): "
if not "%MC_VERSION%"=="" set ARGS=%ARGS% --minecraft-version "%MC_VERSION%"

set /p MODS_PATH="Enter path to mods directory (leave blank for default): "
if not "%MODS_PATH%"=="" set ARGS=%ARGS% --mods-dir "%MODS_PATH%"

set /p BACKUP_PATH="Enter backup directory (leave blank for default): "
if not "%BACKUP_PATH%"=="" set ARGS=%ARGS% --backup-dir "%BACKUP_PATH%"

set /p NO_BACKUP="Skip backups? (y/n): "
if /i "%NO_BACKUP%"=="y" set ARGS=%ARGS% --no-backup

goto RUN

:RUN
echo.
echo Running Minecraft Mod Updater with the following settings:
echo Using FABRIC loader for all mods
echo python "%~dp0minecraft_mod_updater.py" %ARGS%
echo.
python "%~dp0minecraft_mod_updater.py" %ARGS%

:END
echo.
echo Press any key to exit...
pause >nul