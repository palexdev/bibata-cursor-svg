# Bibata Cursor SVG

The [Bibata](https://github.com/ful1e5/Bibata_Cursor) cursor themes with a scalable SVG cursor set added, for desktops that no longer draw the pointer from bitmaps.

GNOME 51 renders the pointer from SVG files and ignores classic XCursor bitmaps. Bibata only ships bitmaps, so on GNOME 51 the pointer silently falls back to Adwaita. The themes published here are the official Bibata v2.0.7 themes plus the missing SVG set, generated from Bibata's own SVG sources. The bitmaps are left untouched, so applications that still load XCursor files look exactly the same.

This is an unofficial repackaging. All design credit goes to Bibata and its author. The upstream request for official SVG builds is [ful1e5/Bibata_Cursor#188](https://github.com/ful1e5/Bibata_Cursor/issues/188).

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/palexdev/bibata-cursor-svg/main/install.sh | sh -s -- Bibata-Modern-Ice
```

Replace `Bibata-Modern-Ice` with any style from the table below. The script downloads that theme from the latest release, installs it to `~/.local/share/icons` and, when `gsettings` is available, selects it. A folder with the same name already in `~/.local/share/icons` is replaced.

## Styles

|          | Amber                   | Classic                   | Ice                   |
| -------- | ----------------------- | ------------------------- | --------------------- |
| Modern   | `Bibata-Modern-Amber`   | `Bibata-Modern-Classic`   | `Bibata-Modern-Ice`   |
| Original | `Bibata-Original-Amber` | `Bibata-Original-Classic` | `Bibata-Original-Ice` |

Every style also has a mirrored variant with a `-Right` suffix, for example `Bibata-Modern-Ice-Right`.

## Manual install

Download the archive for your style from the [releases page](https://github.com/palexdev/bibata-cursor-svg/releases/latest), then extract and select it:

```sh
tar -xJf Bibata-Modern-Ice.tar.xz -C ~/.local/share/icons
gsettings set org.gnome.desktop.interface cursor-theme Bibata-Modern-Ice
```

The location matters. GNOME 51 looks for SVG cursors in `~/.local/share/icons` and in the system icon directories such as `/usr/share/icons`, but not in `~/.icons`.

If the theme was already selected before you installed it, switch to another cursor theme and back, or log out and in, so the shell reloads it.

## Uninstall

```sh
rm -r ~/.local/share/icons/Bibata-Modern-Ice
```

## Build

Requires Python 3.12 or newer and nothing else.

```sh
python3 build.py
```

This builds every style. Pass one or more style names to build only those:

```sh
python3 build.py Bibata-Modern-Ice Bibata-Original-Classic
```

The script downloads the Bibata sources and official themes for the pinned upstream version into `.cache/` and writes one archive per style to `dist/`.

## How it works

Each theme gains a `cursors_scalable` directory next to the usual `cursors` one. Inside it, every cursor has its own folder holding the SVG frames and a `metadata.json` that lists them with their hotspot, nominal size and, for animated cursors, frame delay. Alternative cursor names are symlinks, the same way XCursor themes do it.

The SVG files are Bibata's sources with the colours of the chosen style applied. Hotspots and frame delays come from Bibata's own build configuration, so the SVG cursors line up with the bitmaps. Bibata has no `all-resize` cursor, so that name is an alias of `move`.

## Compatibility

Tested on GNOME Shell 51 on Wayland. KDE Plasma reads the same `cursors_scalable` layout for its SVG cursors, but the themes have not been tested there.

## Versioning

Releases carry the version of the Bibata release they are built from.

## License

GPL-3.0, the same as Bibata. Cursor designs are by Abdulkaiz Khatri and the Bibata contributors.
