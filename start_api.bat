@echo off
chcp 65001 >nul

echo ======================================
echo          一键启动前后端项目
echo ======================================
echo.
pause
echo.

echo 正在启动 MiniCode（前后端一体）...
cd /d "%~dp0backend"
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
minicode

exit /b 0
