# Quick Start Guide - Ubuntu Wallpaper Changer

Panduan cepat untuk menginstall dan menggunakan Ubuntu Random Wallpaper Changer.

## 🚀 Instalasi Cepat (3 Langkah)

### 1. Download & Persiapan
```bash
# Masuk ke folder sslider
cd sslider

# Pastikan semua script executable
chmod +x *.py *.sh wpc
```

### 2. Test Sistem
```bash
# Jalankan test untuk memastikan sistem kompatibel
./test_wallpaper.py
```

### 3. Install
```bash
# Install wallpaper changer
./install.sh
```

**Selesai!** Wallpaper akan berubah otomatis setiap 1 jam.

## 🎯 Penggunaan Cepat

### Perintah Dasar
```bash
# Lihat status
./wpc status

# Ganti wallpaper sekarang
./wpc now

# Lihat daftar gambar
./wpc list
```

### Kontrol Service
```bash
# Start/stop service
./wpc start
./wpc stop
./wpc restart

# Enable/disable auto-start
./wpc enable
./wpc disable
```

### Kustomisasi
```bash
# Ubah interval (dalam jam)
./wpc interval 0.5    # Setiap 30 menit
./wpc interval 2      # Setiap 2 jam

# Tambah gambar dari folder lain
./wpc add ~/Pictures/Wallpapers

# Lihat logs
./wpc logs
```

## 📁 Struktur File

```
sslider/
├── wallpaper_changer.py    # Program utama
├── install.sh              # Installer
├── wpc                     # Control script
├── test_wallpaper.py       # Test script
├── places/                 # Folder gambar (600+ gambar)
└── README_WALLPAPER.md     # Dokumentasi lengkap
```

## 🔧 Troubleshooting Cepat

### Service tidak jalan?
```bash
./wpc status
sudo journalctl -u wallpaper-changer -n 20
```

### Wallpaper tidak berubah?
```bash
./wpc now    # Test manual
./wpc list   # Cek ada gambar atau tidak
```

### Uninstall
```bash
./install.sh uninstall
```

## 📋 Checklist

- [ ] Ubuntu 24.04 dengan GNOME
- [ ] Python 3.6+
- [ ] Folder `places` berisi gambar
- [ ] Test berhasil: `./test_wallpaper.py`
- [ ] Install berhasil: `./install.sh`
- [ ] Service running: `./wpc status`

## 🆘 Bantuan

- **Full Documentation**: `README_WALLPAPER.md`
- **Command Help**: `./wpc help`
- **Test System**: `./test_wallpaper.py`

---
**Happy wallpaper changing! 🎨**