#!/usr/bin/env bash
# Aktualizacja i instalacja Chromium + ChromeDriver
apt-get update
apt-get install -y chromium-browser chromium-chromedriver

# Ustaw ścieżkę do Chrome i ChromeDriver
export PATH=$PATH:/usr/bin
export CHROME_BIN=/usr/bin/chromium-browser
export CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Uruchom bota
python3 main.py
