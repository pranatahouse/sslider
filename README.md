# Project SSlider

## Ubuntu Random Wallpaper Changer

Program Python untuk mengganti wallpaper Ubuntu 24.04 secara otomatis dan random setiap 1 jam menggunakan koleksi gambar dari folder `places` dan `randoms`, termasuk subfoldernya.

### 🚀 Quick Start

```bash
# Test sistem
./test_wallpaper.py

# Install
./install.sh

# Kontrol wallpaper
./wpc status     # Lihat status
./wpc now        # Ganti wallpaper sekarang
./wpc interval 0.5  # Ubah interval ke 30 menit
```

### 📁 File Penting

- `wallpaper_changer.py` - Program utama
- `install.sh` - Installer dan uninstaller
- `wpc` - Script kontrol wallpaper
- `test_wallpaper.py` - Test sistem
- `places/` - Folder berisi 600+ gambar wallpaper
- `randoms/` - Koleksi wallpaper tambahan dalam subfolder kategori
- `README_WALLPAPER.md` - Dokumentasi lengkap
- `QUICKSTART.md` - Panduan cepat

### ✨ Fitur

- ✅ Auto-start saat login (systemd service)
- ✅ Interval yang dapat disesuaikan
- ✅ Support multiple format gambar
- ✅ Logging dan monitoring
- ✅ Dark mode support
- ✅ Easy management dengan `wpc` command

### 📖 Dokumentasi

- **Quick Start**: `QUICKSTART.md`
- **Full Documentation**: `README_WALLPAPER.md`
- **Help**: `./wpc help`

---

## Original Project SSlider

Koleksi gambar wallpaper untuk Ubuntu desktop.
