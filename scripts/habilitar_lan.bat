@echo off
title Enlace de Red Local (LAN) - Eden Cafe PDV
:: Solicita elevacion de privilegios de Administrador automaticamente y ejecuta el script PowerShell
powershell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File \"\"%~dp0habilitar_lan.ps1\"\"' -Verb RunAs}"
