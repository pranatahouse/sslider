#!/bin/bash

# Ubuntu Wallpaper Changer Installer
# Script untuk menginstal dan mengatur wallpaper changer sebagai service

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="wallpaper-changer"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
INSTALL_DIR="/opt/wallpaper-changer"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    print_info "Memeriksa requirements..."

    # Check if running on Ubuntu/GNOME
    if ! command -v gsettings &> /dev/null; then
        print_error "gsettings tidak ditemukan. Program ini memerlukan GNOME desktop environment."
        exit 1
    fi

    # Check Python 3
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 tidak ditemukan. Silakan install Python 3 terlebih dahulu."
        exit 1
    fi

    print_success "Requirements terpenuhi"
}

install_files() {
    print_info "Menginstal file..."

    # Create install directory
    sudo mkdir -p "$INSTALL_DIR"

    # Copy files
    sudo cp "$SCRIPT_DIR/wallpaper_changer.py" "$INSTALL_DIR/"
    sudo cp -r "$SCRIPT_DIR/places" "$INSTALL_DIR/"

    # Make executable
    sudo chmod +x "$INSTALL_DIR/wallpaper_changer.py"

    print_success "File berhasil diinstal ke $INSTALL_DIR"
}

create_service() {
    print_info "Membuat systemd service..."

    # Get current user
    CURRENT_USER=$(whoami)
    USER_HOME=$(eval echo ~$CURRENT_USER)

    # Create service file
    sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Random Wallpaper Changer for Ubuntu
After=graphical-session.target

[Service]
Type=simple
User=$CURRENT_USER
Environment=DISPLAY=:0
Environment=XDG_RUNTIME_DIR=/run/user/$(id -u $CURRENT_USER)
Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u $CURRENT_USER)/bus
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 $INSTALL_DIR/wallpaper_changer.py --interval 1
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

    print_success "Service file dibuat: $SERVICE_FILE"
}

setup_service() {
    print_info "Mengatur systemd service..."

    # Reload systemd
    sudo systemctl daemon-reload

    # Enable service untuk user session
    systemctl --user enable "$SERVICE_NAME"

    print_success "Service berhasil diaktifkan"
}

show_usage() {
    echo ""
    echo "=== Ubuntu Wallpaper Changer ==="
    echo ""
    echo "Perintah yang tersedia:"
    echo "  sudo systemctl start $SERVICE_NAME    - Mulai service"
    echo "  sudo systemctl stop $SERVICE_NAME     - Hentikan service"
    echo "  sudo systemctl status $SERVICE_NAME   - Cek status service"
    echo "  sudo systemctl enable $SERVICE_NAME   - Aktifkan auto-start"
    echo "  sudo systemctl disable $SERVICE_NAME  - Nonaktifkan auto-start"
    echo ""
    echo "Atau jalankan manual:"
    echo "  python3 $INSTALL_DIR/wallpaper_changer.py --help"
    echo "  python3 $INSTALL_DIR/wallpaper_changer.py --once        # Ganti wallpaper sekali"
    echo "  python3 $INSTALL_DIR/wallpaper_changer.py --interval 0.5 # Setiap 30 menit"
    echo ""
    echo "Log file tersimpan di: $INSTALL_DIR/wallpaper_changer.log"
    echo ""
}

uninstall() {
    print_info "Menghapus wallpaper changer..."

    # Stop and disable service
    sudo systemctl stop "$SERVICE_NAME" 2>/dev/null || true
    sudo systemctl disable "$SERVICE_NAME" 2>/dev/null || true
    systemctl --user disable "$SERVICE_NAME" 2>/dev/null || true

    # Remove service file
    sudo rm -f "$SERVICE_FILE"

    # Remove install directory
    sudo rm -rf "$INSTALL_DIR"

    # Reload systemd
    sudo systemctl daemon-reload

    print_success "Wallpaper changer berhasil dihapus"
}

# Main installation function
install() {
    echo ""
    echo "=== Ubuntu Random Wallpaper Changer Installer ==="
    echo ""

    check_requirements
    install_files
    create_service
    setup_service

    echo ""
    print_success "Instalasi berhasil!"
    print_info "Service telah diaktifkan dan akan berjalan otomatis saat login."

    # Ask if user wants to start service now
    read -p "Apakah Anda ingin memulai service sekarang? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo systemctl start "$SERVICE_NAME"
        print_success "Service dimulai!"

        # Show status
        sleep 2
        print_info "Status service:"
        sudo systemctl status "$SERVICE_NAME" --no-pager -l
    fi

    show_usage
}

# Parse command line arguments
case "${1:-install}" in
    "install")
        install
        ;;
    "uninstall")
        uninstall
        ;;
    "status")
        sudo systemctl status "$SERVICE_NAME"
        ;;
    "start")
        sudo systemctl start "$SERVICE_NAME"
        print_success "Service dimulai"
        ;;
    "stop")
        sudo systemctl stop "$SERVICE_NAME"
        print_success "Service dihentikan"
        ;;
    "restart")
        sudo systemctl restart "$SERVICE_NAME"
        print_success "Service direstart"
        ;;
    "logs")
        echo "=== Service Logs ==="
        sudo journalctl -u "$SERVICE_NAME" -f
        ;;
    "help"|"--help"|"-h")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  install    - Install wallpaper changer (default)"
        echo "  uninstall  - Remove wallpaper changer"
        echo "  start      - Start service"
        echo "  stop       - Stop service"
        echo "  restart    - Restart service"
        echo "  status     - Show service status"
        echo "  logs       - Show service logs"
        echo "  help       - Show this help"
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
