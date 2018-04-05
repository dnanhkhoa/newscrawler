cd ..
for /d /r %%a in (__pycache__\) do if exist "%%a" rmdir /s /q "%%a"
pause