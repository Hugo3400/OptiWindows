@echo off
:: Script d'installation rapide pour OptiWindows
title OptiWindows - Installation

echo.
echo ========================================
echo    OptiWindows - Installation
echo ========================================
echo.

:: Vérification de Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERREUR] Python n'est pas installe
    echo.
    echo Telechargement de Python recommande...
    echo Voulez-vous ouvrir la page de telechargement ? (O/N)
    choice /c ON /n
    if errorlevel 2 goto :noPython
    if errorlevel 1 start https://www.python.org/downloads/
    :noPython
    echo.
    echo Apres installation de Python, relancez ce script
    pause
    exit /b 1
)

echo [OK] Python detecte
python --version

:: Mise à jour de pip
echo.
echo Mise a jour de pip...
python -m pip install --upgrade pip

:: Installation des dépendances
echo.
echo Installation des dependances...
python -m pip install -r requirements.txt

if %errorLevel% neq 0 (
    echo.
    echo [ERREUR] Echec de l'installation des dependances
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installation terminee avec succes !
echo ========================================
echo.
echo Vous pouvez maintenant lancer OptiWindows avec:
echo   - launcher.bat
echo   - launcher.ps1
echo.
pause
