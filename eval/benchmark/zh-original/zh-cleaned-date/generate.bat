@echo off
cls

FOR /L %%G IN (10,1,60) DO type nul >> %%G.txt

pause
