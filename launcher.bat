@echo off
:: OptiWindows Launcher - Lance avec droits administrateur
:: Vérifie si le script est exécuté en tant qu'administrateur

title OptiWindows - Launcher

:: Vérification des droits administrateur
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Droits administrateur detectes
    goto :runPython
) else (
    echo.
    echo ========================================
    echo   OptiWindows necessite les droits
    echo   administrateur pour fonctionner
    echo ========================================
    echo.
    echo Relancement avec elevation...
    
    :: Relance le script avec élévation
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:runPython
echo.
echo ========================================
echo        Lancement d'OptiWindows
echo ========================================
echo.

:: Vérification de Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERREUR] Python n'est pas installe ou non disponible dans PATH
    echo.
    echo Veuillez installer Python depuis https://www.python.org/downloads/
    echo Cochez "Add Python to PATH" lors de l'installation
    pause
    exit /b 1
)

:: Vérification des dépendances
if not exist "requirements.txt" (
    echo [ERREUR] requirements.txt introuvable
    pause
    exit /b 1
)

echo Verification des dependances Python...
python -m pip install -q -r requirements.txt

if %errorLevel% neq 0 (
    echo.
    echo [ERREUR] Echec de l'installation des dependances
    echo Tentative avec upgrade...
    python -m pip install --upgrade -r requirements.txt
)

:: Lancement de l'application
echo.
echo Lancement de l'application...
python main.py

if %errorLevel% neq 0 (
    echo.
    echo [ERREUR] L'application s'est terminee avec une erreur
    pause
)
