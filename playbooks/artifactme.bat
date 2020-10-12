@echo off
7za x Investigation.zip -o"%*" -y
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& '.\Investigation\scripts\artifact.ps1' %*"
7za a -r -tzip "%*\investigation\%COMPUTERNAME%_artifacts.zip" "%*\investigation\results"