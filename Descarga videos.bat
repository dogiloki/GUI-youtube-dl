@echo off
set carpeta=%date:~0,2%-%date:~3,2%-%date:~6,4%
set fecha=%Time:~0,2%.%Time:~3,2%.%Time:~6,2%
md logs
cd logs
md %carpeta%
cd..
python gui.py > "logs/%carpeta%/%fecha%.log"