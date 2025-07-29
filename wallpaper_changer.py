#!/usr/bin/env python3
"""
Ubuntu Wallpaper Changer
Mengganti wallpaper Ubuntu secara random setiap 1 jam menggunakan gambar dari folder places
"""

import os
import random
import subprocess
import time
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wallpaper_changer.log'),
        logging.StreamHandler()
    ]
)

class WallpaperChanger:
    def __init__(self, images_directory="places"):
        self.images_dir = Path(__file__).parent / images_directory
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        self.current_wallpaper = None

    def get_image_files(self):
        """Mendapatkan daftar semua file gambar yang didukung"""
        try:
            image_files = []
            if not self.images_dir.exists():
                logging.error(f"Directory {self.images_dir} tidak ditemukan!")
                return []

            for file_path in self.images_dir.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                    image_files.append(file_path.absolute())

            logging.info(f"Ditemukan {len(image_files)} file gambar")
            return image_files

        except Exception as e:
            logging.error(f"Error saat membaca directory: {e}")
            return []

    def set_wallpaper(self, image_path):
        """Mengatur wallpaper menggunakan gsettings"""
        try:
            # Untuk GNOME (Ubuntu default)
            subprocess.run([
                'gsettings', 'set', 'org.gnome.desktop.background',
                'picture-uri', f'file://{image_path}'
            ], check=True)

            # Untuk dark mode juga
            subprocess.run([
                'gsettings', 'set', 'org.gnome.desktop.background',
                'picture-uri-dark', f'file://{image_path}'
            ], check=True)

            logging.info(f"Wallpaper berhasil diubah ke: {image_path.name}")
            self.current_wallpaper = image_path
            return True

        except subprocess.CalledProcessError as e:
            logging.error(f"Error saat mengatur wallpaper: {e}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return False

    def change_wallpaper_random(self):
        """Mengganti wallpaper secara random"""
        image_files = self.get_image_files()

        if not image_files:
            logging.error("Tidak ada file gambar yang ditemukan!")
            return False

        # Pilih gambar random (hindari gambar yang sama dengan sebelumnya jika memungkinkan)
        available_images = image_files.copy()
        if len(available_images) > 1 and self.current_wallpaper in available_images:
            available_images.remove(self.current_wallpaper)

        selected_image = random.choice(available_images)
        return self.set_wallpaper(selected_image)

    def run_daemon(self, interval_hours=1):
        """Menjalankan program sebagai daemon yang mengganti wallpaper setiap interval tertentu"""
        logging.info(f"Memulai wallpaper changer daemon (interval: {interval_hours} jam)")

        # Ganti wallpaper pertama kali
        self.change_wallpaper_random()

        # Loop untuk mengganti wallpaper setiap interval
        interval_seconds = interval_hours * 3600  # Convert jam ke detik

        try:
            while True:
                time.sleep(interval_seconds)
                logging.info("Waktunya mengganti wallpaper...")
                self.change_wallpaper_random()

        except KeyboardInterrupt:
            logging.info("Program dihentikan oleh user")
        except Exception as e:
            logging.error(f"Error dalam daemon loop: {e}")

def main():
    """Fungsi utama"""
    import argparse

    parser = argparse.ArgumentParser(description='Ubuntu Random Wallpaper Changer')
    parser.add_argument('--directory', '-d', default='places',
                       help='Directory berisi file gambar (default: places)')
    parser.add_argument('--interval', '-i', type=float, default=1.0,
                       help='Interval dalam jam untuk mengganti wallpaper (default: 1.0)')
    parser.add_argument('--once', action='store_true',
                       help='Ganti wallpaper sekali saja (tidak running sebagai daemon)')
    parser.add_argument('--list', action='store_true',
                       help='Tampilkan daftar file gambar yang ditemukan')

    args = parser.parse_args()

    # Inisialisasi wallpaper changer
    changer = WallpaperChanger(args.directory)

    if args.list:
        # Tampilkan daftar file gambar
        images = changer.get_image_files()
        print(f"\nDitemukan {len(images)} file gambar:")
        for img in images:
            print(f"  - {img.name}")
        return

    if args.once:
        # Ganti wallpaper sekali saja
        print("Mengganti wallpaper...")
        success = changer.change_wallpaper_random()
        if success:
            print("Wallpaper berhasil diganti!")
        else:
            print("Gagal mengganti wallpaper!")
        return

    # Running sebagai daemon
    try:
        changer.run_daemon(args.interval)
    except KeyboardInterrupt:
        print("\nProgram dihentikan.")

if __name__ == "__main__":
    main()
