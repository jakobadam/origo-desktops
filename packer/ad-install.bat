@echo off
powershell -ExecutionPolicy bypass -File %~dp0install-ad.ps1
powershell -ExecutionPolicy bypass -File %~dp0ad-add-forest.ps1
