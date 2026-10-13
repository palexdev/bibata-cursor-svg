#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import tarfile
import tomllib
import urllib.request
from pathlib import Path

UPSTREAM = "https://github.com/ful1e5/Bibata_Cursor"
UPSTREAM_TAG = "v2.0.7"
CANVAS = 256
EXTRA_ALIASES = {"all-resize": "move"}

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / ".cache" / UPSTREAM_TAG
BUILD = ROOT / "build"
DIST = ROOT / "dist"


def download(url, target):
    if target.exists():
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + ".part")
    with urllib.request.urlopen(url) as response, open(partial, "wb") as file:
        shutil.copyfileobj(response, file)
    partial.rename(target)
    return target


def extract(archive, target):
    with tarfile.open(archive) as tar:
        tar.extractall(target, filter="data")


def fetch_sources():
    sources = CACHE / "sources"
    if sources.exists():
        return sources
    archive = download(
        f"{UPSTREAM}/archive/refs/tags/{UPSTREAM_TAG}.tar.gz",
        CACHE / "sources.tar.gz",
    )
    staging = CACHE / "sources.tmp"
    shutil.rmtree(staging, ignore_errors=True)
    extract(archive, staging)
    next(staging.iterdir()).rename(sources)
    staging.rmdir()
    return sources


def generate_scalable(sources, theme, target):
    render = json.loads((sources / "render.json").read_text())[theme]
    svg_dir = sources / render["dir"]
    colors = [(color["match"], color["replace"]) for color in render["colors"]]

    variant = "right" if "Right" in theme else "normal"
    config = sources / "configs" / variant / "x.build.toml"
    cursors = tomllib.loads(config.read_text())["cursors"]
    fallback = cursors.pop("fallback_settings")

    def recolor(text):
        for match, replace in colors:
            text = text.replace(match.upper(), replace).replace(match.lower(), replace)
        return text

    target.mkdir(parents=True)
    aliases = {}
    for entry in cursors.values():
        name = entry["x11_name"]
        stem = entry["png"].removesuffix(".png")
        if stem.endswith("-*"):
            frames = sorted((svg_dir / stem[:-2]).glob("*.svg"))
        else:
            frames = [svg_dir / f"{stem}.svg"]
        if not frames:
            raise FileNotFoundError(f"{theme}: no SVG frames for {name}")

        cursor_dir = target / name
        cursor_dir.mkdir()
        metadata = []
        for frame in frames:
            (cursor_dir / frame.name).write_text(recolor(frame.read_text()))
            item = {"filename": frame.name}
            if len(frames) > 1:
                item["delay"] = entry.get("x11_delay", fallback["x11_delay"])
            item["hotspot_x"] = entry.get("x_hotspot", fallback["x_hotspot"])
            item["hotspot_y"] = entry.get("y_hotspot", fallback["y_hotspot"])
            item["nominal_size"] = CANVAS
            metadata.append(item)
        (cursor_dir / "metadata.json").write_text(json.dumps(metadata, indent=4) + "\n")

        for alias in entry.get("x11_symlinks", []):
            aliases.setdefault(alias, name)

    for alias, name in EXTRA_ALIASES.items():
        aliases.setdefault(alias, name)

    for alias, name in aliases.items():
        link = target / alias
        if not link.exists() and not link.is_symlink():
            os.symlink(name, link)


def reset_owner(info):
    info.uid = info.gid = 0
    info.uname = info.gname = "root"
    return info


def build_theme(sources, theme):
    archive = download(
        f"{UPSTREAM}/releases/download/{UPSTREAM_TAG}/{theme}.tar.xz",
        CACHE / f"{theme}.tar.xz",
    )
    theme_dir = BUILD / theme
    shutil.rmtree(theme_dir, ignore_errors=True)
    extract(archive, BUILD)

    generate_scalable(sources, theme, theme_dir / "cursors_scalable")
    shutil.copy(sources / "LICENSE", theme_dir / "LICENSE")

    DIST.mkdir(exist_ok=True)
    package = DIST / f"{theme}.tar.xz"
    with tarfile.open(package, "w:xz") as tar:
        tar.add(theme_dir, arcname=theme, filter=reset_owner)
    return package


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("themes", nargs="*")
    args = parser.parse_args()

    sources = fetch_sources()
    available = list(json.loads((sources / "render.json").read_text()))
    themes = args.themes or available
    for theme in themes:
        if theme not in available:
            parser.error(f"unknown theme {theme}, available: {', '.join(available)}")

    for theme in themes:
        print(build_theme(sources, theme).relative_to(ROOT))


if __name__ == "__main__":
    main()
