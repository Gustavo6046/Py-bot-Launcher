@echo off
cd code
echo Testing execution speed of script... > profiler
python -m cProfile -s cumtime main.py > ..\profilerlog.txt
echo .
echo ==============
echo .
echo Done testing! In case of traceback,
echo email the author:
echo .
echo gugurehermann@gmail.com
pause > nul