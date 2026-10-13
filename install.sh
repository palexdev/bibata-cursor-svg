#!/bin/sh
set -eu

repo="palexdev/bibata-cursor-svg"
theme="${1:-Bibata-Modern-Ice}"
dest="${XDG_DATA_HOME:-$HOME/.local/share}/icons"

case "$theme" in
    */* | *.*)
        echo "Invalid theme name: $theme" >&2
        exit 1
        ;;
    Bibata-Modern-* | Bibata-Original-*) ;;
    *)
        echo "Unknown theme: $theme" >&2
        exit 1
        ;;
esac

archive="$(mktemp)"
trap 'rm -f "$archive"' EXIT

curl -fL --progress-bar -o "$archive" \
    "https://github.com/$repo/releases/latest/download/$theme.tar.xz"

mkdir -p "$dest"
rm -rf "${dest:?}/$theme"
tar -xJf "$archive" -C "$dest"

if command -v gsettings >/dev/null 2>&1; then
    gsettings reset org.gnome.desktop.interface cursor-theme
    gsettings set org.gnome.desktop.interface cursor-theme "$theme"
fi

echo "Installed $theme to $dest/$theme"
