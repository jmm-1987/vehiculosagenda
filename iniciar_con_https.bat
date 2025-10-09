@echo off
echo ========================================
echo   INICIANDO SERVIDOR CON HTTPS
echo ========================================
echo.
echo Cerrando procesos Python anteriores...
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul
echo.
echo Iniciando servidor Flask con SSL...
echo.
python main.py
pause

