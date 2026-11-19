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
- `random_image.php` - Mengembalikan URL gambar acak berdasarkan keyword
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

### Mengambil URL gambar berdasarkan keyword

Memerlukan PHP dengan ekstensi PDO SQLite (`pdo_sqlite`).

Jika `../config.base.php` tersedia dan menetapkan `SQLITE_BALICANDRA_DB` sebagai konstanta atau variabel, path tersebut digunakan. Jika tidak, program memakai `balicandra.db` di folder skrip.

Jalankan dari terminal:

```bash
php random_image.php bali
```

Jika keyword tidak diberikan, program otomatis memakai `bali`:

```bash
php random_image.php
```

Atau jalankan sebagai endpoint HTTP:

```bash
php -S 127.0.0.1:8000
curl 'http://127.0.0.1:8000/random_image.php?q=bali'
curl 'http://127.0.0.1:8000/random_image.php?q=bali%2C%20mantra'
curl 'http://127.0.0.1:8000/random_image.php'  # default: bali
```

Pisahkan beberapa keyword dengan koma. Program memilih acak dari gambar yang cocok dengan salah satu keyword. Pencocokan tepat dan tidak membedakan huruf besar/kecil; tanda hubung diperlakukan sebagai spasi. URL dikembalikan sebagai teks biasa.

---

## Original Project SSlider

Koleksi gambar wallpaper untuk Ubuntu desktop.
