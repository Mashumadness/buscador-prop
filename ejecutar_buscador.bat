@echo off
chcp 65001 > nul
title Buscador de PHs - Zona Oeste
cls
echo ==========================================================
echo   BUSCADOR DE PHs - RAMOS MEJIA / HAEDO / VILLA SARMIENTO
echo ==========================================================
echo.
echo Iniciando rastreo de propiedades independientes...
echo.

cd /d "%~dp0"
python main.py

echo.
echo ==========================================================
echo   Busqueda finalizada. Podes cerrar esta ventana.
echo ==========================================================
pause
