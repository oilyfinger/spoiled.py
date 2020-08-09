@echo off

echo __ContentName__ 자동화 도구
echo.
set /p sampleInput=테스트 입력: 
echo.

py at__ContentName__.py %sampleInput%
pause
