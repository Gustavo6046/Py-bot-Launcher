@echo off
del stderr.txt >nul

echo Checking for tracebacks ...

cd code
python main.py 2> ..\stderr.txt

if exist ..\stderr.txt (echo Traceback exists!) else (echo Succesfull run!)
echo .
echo Stored traceback in stderr.txt
pause