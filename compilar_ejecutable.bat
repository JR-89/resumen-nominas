@echo off
echo Compilando ResumenNominas.exe con archivo .spec actualizado...
pyinstaller ResumenNominas.spec
echo -------------------------------------------
echo Ejecutable compilado. Lo encontrarás en:
echo dist\ResumenNominas\ResumenNominas.exe
pause
