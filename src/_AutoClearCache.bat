@echo off

echo Python Cache Auto Cleaning
echo.

echo.>>clear.log

if exist "__pycache__" del /s /q "__pycache__" >> clear.log
if exist "__pycache__" rmdir /s /q "__pycache__" >> clear.log

for /d /r %%i in (*.*) do if exist "%%i\__pycache__" del /s /q "%%i\__pycache__" >> clear.log
for /d /r %%i in (*.*) do if exist "%%i\__pycache__" rmdir /s /q "%%i\__pycache__" >> clear.log

pause
