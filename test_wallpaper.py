#!/usr/bin/env python3
"""
Test script untuk memverifikasi instalasi Ubuntu Wallpaper Changer
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_status(message, status="INFO"):
    colors = {
        "INFO": "\033[0;34m",
        "SUCCESS": "\033[0;32m",
        "WARNING": "\033[1;33m",
        "ERROR": "\033[0;31m",
        "NC": "\033[0m"
    }
    print(f"{colors.get(status, '')}[{status}]{colors['NC']} {message}")

def check_python_version():
    """Cek versi Python"""
    print_status("Memeriksa versi Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} ✓", "SUCCESS")
        return True
    else:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - Memerlukan Python 3.6+", "ERROR")
        return False

def check_gsettings():
    """Cek ketersediaan gsettings"""
    print_status("Memeriksa gsettings...")
    try:
        result = subprocess.run(['gsettings', '--version'],
                              capture_output=True, text=True, check=True)
        print_status(f"gsettings tersedia - {result.stdout.strip()} ✓", "SUCCESS")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_status("gsettings tidak ditemukan - GNOME desktop environment diperlukan", "ERROR")
        return False

def check_desktop_environment():
    """Cek desktop environment"""
    print_status("Memeriksa desktop environment...")

    # Cek environment variables
    desktop = os.environ.get('XDG_CURRENT_DESKTOP', '')
    session = os.environ.get('DESKTOP_SESSION', '')

    if 'GNOME' in desktop or 'gnome' in session:
        print_status(f"Desktop: {desktop} ✓", "SUCCESS")
        return True
    else:
        print_status(f"Desktop: {desktop} - GNOME direkomendasikan", "WARNING")
        return True  # Still allow, might work

def check_image_directory():
    """Cek ketersediaan folder gambar"""
    print_status("Memeriksa folder gambar...")

    script_dir = Path(__file__).parent
    places_dir = script_dir / "places"

    if not places_dir.exists():
        print_status("Folder 'places' tidak ditemukan", "ERROR")
        return False

    # Hitung file gambar
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    image_files = []

    for file_path in places_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_formats:
            image_files.append(file_path)

    if len(image_files) == 0:
        print_status("Tidak ada file gambar yang ditemukan dalam folder 'places'", "ERROR")
        return False

    print_status(f"Ditemukan {len(image_files)} file gambar ✓", "SUCCESS")

    # Tampilkan beberapa contoh
    print_status("Contoh file gambar:")
    for i, img in enumerate(image_files[:5]):
        print(f"  - {img.name}")
    if len(image_files) > 5:
        print(f"  ... dan {len(image_files) - 5} file lainnya")

    return True

def test_wallpaper_script():
    """Test script wallpaper_changer.py"""
    print_status("Testing wallpaper script...")

    script_path = Path(__file__).parent / "wallpaper_changer.py"

    if not script_path.exists():
        print_status("wallpaper_changer.py tidak ditemukan", "ERROR")
        return False

    # Test --help
    try:
        result = subprocess.run([sys.executable, str(script_path), '--help'],
                              capture_output=True, text=True, check=True, timeout=10)
        print_status("Script dapat dijalankan ✓", "SUCCESS")
    except subprocess.TimeoutExpired:
        print_status("Script timeout", "ERROR")
        return False
    except subprocess.CalledProcessError as e:
        print_status(f"Script error: {e}", "ERROR")
        return False

    # Test --list
    try:
        result = subprocess.run([sys.executable, str(script_path), '--list'],
                              capture_output=True, text=True, check=True, timeout=10)
        print_status("Fungsi --list berhasil ✓", "SUCCESS")
    except Exception as e:
        print_status(f"Fungsi --list gagal: {e}", "WARNING")

    return True

def test_current_wallpaper():
    """Test mendapatkan wallpaper saat ini"""
    print_status("Testing akses ke wallpaper settings...")

    try:
        # Get current wallpaper
        result = subprocess.run([
            'gsettings', 'get', 'org.gnome.desktop.background', 'picture-uri'
        ], capture_output=True, text=True, check=True)

        current_wallpaper = result.stdout.strip().strip("'\"")
        print_status(f"Wallpaper saat ini: {current_wallpaper} ✓", "SUCCESS")

        return True
    except subprocess.CalledProcessError as e:
        print_status(f"Gagal mendapatkan wallpaper: {e}", "ERROR")
        return False

def check_installation():
    """Cek apakah sudah terinstall"""
    print_status("Memeriksa instalasi...")

    install_dir = Path("/opt/wallpaper-changer")
    service_file = Path("/etc/systemd/system/wallpaper-changer.service")

    if install_dir.exists() and service_file.exists():
        print_status("Wallpaper changer sudah terinstall ✓", "SUCCESS")

        # Cek status service
        try:
            result = subprocess.run(['systemctl', 'is-active', 'wallpaper-changer'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print_status("Service berjalan ✓", "SUCCESS")
            else:
                print_status("Service tidak berjalan", "WARNING")
        except:
            print_status("Tidak dapat cek status service", "WARNING")

        return True
    else:
        print_status("Belum terinstall - jalankan ./install.sh untuk menginstall", "INFO")
        return False

def run_quick_test():
    """Test cepat dengan mengganti wallpaper sekali"""
    print_status("Menjalankan test cepat...")

    script_path = Path(__file__).parent / "wallpaper_changer.py"

    try:
        print_status("Mencoba mengganti wallpaper...")
        result = subprocess.run([sys.executable, str(script_path), '--once'],
                              capture_output=True, text=True, check=True, timeout=30)

        print_status("Test berhasil! Wallpaper telah diganti ✓", "SUCCESS")
        return True

    except subprocess.TimeoutExpired:
        print_status("Test timeout - mungkin ada masalah dengan gsettings", "ERROR")
        return False
    except subprocess.CalledProcessError as e:
        print_status(f"Test gagal: {e.stderr}", "ERROR")
        return False
    except Exception as e:
        print_status(f"Unexpected error: {e}", "ERROR")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("Ubuntu Random Wallpaper Changer - Test Script")
    print("=" * 60)
    print()

    tests = [
        ("Python Version", check_python_version),
        ("gsettings Availability", check_gsettings),
        ("Desktop Environment", check_desktop_environment),
        ("Image Directory", check_image_directory),
        ("Wallpaper Script", test_wallpaper_script),
        ("Current Wallpaper Access", test_current_wallpaper),
        ("Installation Status", check_installation),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_status(f"Test error: {e}", "ERROR")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        color = "SUCCESS" if result else "ERROR"
        print_status(f"{test_name:<30} {status}", color)
        if result:
            passed += 1

    print()
    print_status(f"Total: {passed}/{total} tests passed",
                "SUCCESS" if passed == total else "WARNING")

    # Recommendations
    print("\n" + "=" * 60)
    print("REKOMENDASI")
    print("=" * 60)

    if passed == total:
        print_status("Semua test berhasil! Sistem siap digunakan", "SUCCESS")

        # Ask for quick test
        try:
            response = input("\nApakah Anda ingin menjalankan test cepat (mengganti wallpaper sekali)? (y/n): ")
            if response.lower() in ['y', 'yes']:
                run_quick_test()
        except KeyboardInterrupt:
            print("\nTest dibatalkan")

    else:
        failed_tests = [name for name, result in results if not result]
        print_status("Beberapa test gagal. Perbaiki masalah berikut:", "WARNING")
        for test in failed_tests:
            print(f"  - {test}")

        print()
        print_status("Setelah memperbaiki masalah, jalankan test lagi", "INFO")

    print("\nUntuk menginstall: ./install.sh")
    print("Untuk bantuan: ./wpc help")

if __name__ == "__main__":
    main()
