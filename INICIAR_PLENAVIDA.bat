@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
title PlenaVida - Configuração inicial

echo ==========================================
echo          PLENAVIDA - CONFIGURACAO
echo ==========================================
echo.

set "PY="
where py >nul 2>nul
if not errorlevel 1 set "PY=py"
if not defined PY (
  where python >nul 2>nul
  if not errorlevel 1 set "PY=python"
)

if not defined PY (
  echo Python nao foi encontrado neste computador.
  echo Vou abrir a pagina oficial para instalar.
  start "" "https://www.python.org/downloads/windows/"
  echo.
  echo Na instalacao, marque a opcao ADD PYTHON TO PATH.
  echo Depois de instalar, feche esta janela e abra este arquivo novamente.
  pause
  exit /b 1
)

echo Python encontrado:
%PY% --version
if errorlevel 1 goto erro

echo.
echo Preparando o instalador de pacotes...
%PY% -m ensurepip --upgrade

echo.
echo Instalando as dependencias do PlenaVida...
%PY% -m pip install --upgrade pip
%PY% -m pip install -r requirements.txt
if errorlevel 1 goto erro

echo.
echo Agora vamos cadastrar o primeiro funcionario.
echo Preencha os dados solicitados no terminal.
%PY% -m flask --app app criar-funcionario
if errorlevel 1 goto erro

echo.
echo Configuracao concluida! Abrindo o PlenaVida...
echo Quando quiser encerrar, volte a esta janela e pressione Ctrl+C.
echo Depois acesse http://127.0.0.1:5000 no navegador.
echo.
%PY% app.py
pause
exit /b 0

:erro
echo.
echo Ocorreu um erro durante a configuracao.
echo Tire uma foto desta tela e envie aqui para eu te ajudar.
pause
exit /b 1
