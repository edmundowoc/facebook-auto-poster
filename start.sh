#!/usr/bin/env bash
# Instalacja Chrome i ChromeDrivera w środowisku Render
apt-get update
apt-get install -y chromium-browser chromium-chromedriver

# Ustawienia ścieżek
export PATH=$PATH:/usr/bin
export CHROME_BIN=/usr/bin/chromium-browser
export CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Uruchomienie bota
python3 main.py
