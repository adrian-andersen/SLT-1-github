@echo off
echo Starter lokal webserver pa port 8080...
start "" "http://localhost:8080/presentation/index.html"
python -m http.server 8080 --directory "%~dp0"
