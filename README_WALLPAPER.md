# Ubuntu Random Wallpaper Changer

Program Python untuk mengganti wallpaper Ubuntu 24.04 secara otomatis dan random setiap 1 jam menggunakan koleksi gambar dari folder `places` dan `randoms`, termasuk subfoldernya.

## Fitur

- ✨ Mengganti wallpaper secara random dari koleksi gambar
- ⏰ Interval yang dapat disesuaikan (default: 1 jam)
- 🔄 Auto-start saat login (systemd service)
- 📝 Logging untuk monitoring
- 🌙 Support untuk dark mode
- 🎯 Menghindari wallpaper yang sama berturut-turut
- 🖼️ Support multiple format gambar (JPG, PNG, BMP, TIFF, WebP)

## Requirements

- Ubuntu 24.04 dengan GNOME desktop environment
- Python 3.6+
- `gsettings` (biasanya sudah terinstall di Ubuntu)

## Instalasi

### Instalasi Otomatis (Recommended)

1. Clone atau download repository ini
2. Buka terminal di folder `sslider`
3. Jalankan installer:

```bash
chmod +x install.sh
./install.sh
```

Installer akan:
- Menginstal program dan folder wallpaper `places` serta `randoms` ke `/opt/wallpaper-changer/`
- Membuat systemd service
- Mengaktifkan auto-start saat login
- Memulai service jika diminta

### Instalasi Manual

1. Copy file `wallpaper_changer.py` dan folder `places` serta `randoms` ke lokasi yang diinginkan
2. Buat executable:
```bash
chmod +x wallpaper_changer.py
```

## Penggunaan

### Service Mode (Otomatis)

Setelah instalasi, wallpaper changer akan berjalan otomatis sebagai service:

```bash
# Status service
sudo systemctl status wallpaper-changer

# Start/stop service
sudo systemctl start wallpaper-changer
sudo systemctl stop wallpaper-changer

# Enable/disable auto-start
sudo systemctl enable wallpaper-changer
sudo systemctl disable wallpaper-changer

# Lihat logs
sudo journalctl -u wallpaper-changer -f
```

### Manual Mode

```bash
# Ganti wallpaper sekali saja
python3 wallpaper_changer.py --once

# Jalankan dengan interval custom (dalam jam)
python3 wallpaper_changer.py --interval 0.5  # Setiap 30 menit
python3 wallpaper_changer.py --interval 2    # Setiap 2 jam

# Lihat daftar gambar yang tersedia
python3 wallpaper_changer.py --list

# Gunakan folder gambar lain
python3 wallpaper_changer.py --directory /path/to/images

# Lihat help
python3 wallpaper_changer.py --help
```

## Konfigurasi

### Menambah Gambar Baru

1. Copy file gambar ke folder `places/` atau ke subfolder di `randoms/`
2. Format yang didukung: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.webp`
3. Service akan otomatis detect gambar baru

### Mengubah Interval

Untuk mengubah interval default, edit file service:

```bash
sudo nano /etc/systemd/system/wallpaper-changer.service
```

Ubah parameter `--interval` pada baris `ExecStart`:
```
ExecStart=/usr/bin/python3 /opt/wallpaper-changer/wallpaper_changer.py --interval 2
```

Kemudian restart service:
```bash
sudo systemctl daemon-reload
sudo systemctl restart wallpaper-changer
```

## Troubleshooting

### Service tidak berjalan

1. Cek status service:
```bash
sudo systemctl status wallpaper-changer
```

2. Lihat logs untuk error:
```bash
sudo journalctl -u wallpaper-changer -n 50
```

3. Pastikan GNOME desktop environment terinstall:
```bash
gsettings --version
```

### Wallpaper tidak berubah

1. Pastikan folder `places` berisi file gambar
2. Cek permission file gambar (harus readable)
3. Cek log file: `/opt/wallpaper-changer/wallpaper_changer.log`

### Manual testing

Test wallpaper changer secara manual:
```bash
cd /opt/wallpaper-changer
python3 wallpaper_changer.py --once
```

## Uninstall

Untuk menghapus wallpaper changer sepenuhnya:

```bash
./install.sh uninstall
```

Atau manual:
```bash
sudo systemctl stop wallpaper-changer
sudo systemctl disable wallpaper-changer
sudo rm /etc/systemd/system/wallpaper-changer.service
sudo rm -rf /opt/wallpaper-changer
sudo systemctl daemon-reload
```

## File Structure

```
sslider/
├── wallpaper_changer.py    # Program utama
├── install.sh              # Script installer
├── places/                 # Folder berisi gambar wallpaper
│   ├── image1.jpg
│   ├── image2.png
│   └── ...
├── randoms/                # Gambar wallpaper tambahan, termasuk dalam subfolder kategori
│   ├── nature/
│   ├── bali/
│   └── ...
└── README_WALLPAPER.md     # Dokumentasi ini
```

Setelah instalasi:
```
/opt/wallpaper-changer/
├── wallpaper_changer.py
├── places/
│   └── (koleksi gambar)
├── randoms/
│   └── (koleksi gambar dan subfolder kategori)
└── wallpaper_changer.log   # Log file
```

## Advanced Usage

### Custom Image Directory

```bash
# Menggunakan folder gambar lain
python3 wallpaper_changer.py --directory ~/Pictures/Wallpapers
```

### Running sebagai User Service

Untuk menjalankan sebagai user service (tanpa sudo):

```bash
# Copy service file ke user directory
mkdir -p ~/.config/systemd/user
cp /etc/systemd/system/wallpaper-changer.service ~/.config/systemd/user/

# Enable untuk user
systemctl --user enable wallpaper-changer
systemctl --user start wallpaper-changer
```

### Integration dengan Cron

Alternatif menggunakan cron job:

```bash
# Edit crontab
crontab -e

# Tambahkan line untuk menjalankan setiap jam
0 * * * * /usr/bin/python3 /opt/wallpaper-changer/wallpaper_changer.py --once
```

## Tips

1. **Performance**: Program menggunakan resource minimal dan hanya aktif saat mengganti wallpaper
2. **Battery**: Interval 1 jam cukup optimal untuk laptop (tidak terlalu sering)
3. **Koleksi Gambar**: Semakin banyak gambar, semakin bervariasi wallpaper yang ditampilkan
4. **Resolution**: Gunakan gambar dengan resolusi yang sesuai dengan monitor untuk hasil terbaik

## Contributing

Kontribusi welcome! Silakan:
1. Fork repository
2. Buat branch untuk fitur baru
3. Submit pull request

## License

Open source - gunakan dan modifikasi sesuai kebutuhan.

---

**Selamat menikmati wallpaper yang selalu berubah! 🎨**
