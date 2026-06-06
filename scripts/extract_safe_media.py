#!/usr/bin/env python3
import csv
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = ROOT / "data" / "source" / "uploads.zip"
OUT_DIR = ROOT / "public" / "wp-content" / "uploads"
REPORT_DIR = ROOT / "data" / "site"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

SAFE_EXTENSIONS = {
    ".apng",
    ".avif",
    ".gif",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".svg",
    ".webp",
}


def safe_zip_member(name):
    path = Path(name)
    if path.is_absolute() or ".." in path.parts:
        return False
    if name.startswith("__MACOSX/"):
        return False
    if not re.match(r"^uploads/[0-9]{4}/[0-9]{2}/[^/]+$", name):
        return False
    return path.suffix.lower() in SAFE_EXTENSIONS


def main():
    if not ZIP_PATH.exists():
        existing = list(OUT_DIR.glob("**/*")) if OUT_DIR.exists() else []
        files = [path for path in existing if path.is_file()]
        print(json.dumps({
            "safe_media_files": len(files),
            "source": "existing-public-media",
            "note": "uploads.zip ontbreekt; bestaande public media gebruikt."
        }, ensure_ascii=False))
        return

    rows = []
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH) as archive:
        for info in archive.infolist():
            if info.is_dir() or not safe_zip_member(info.filename):
                continue
            relative = Path(info.filename).relative_to("uploads")
            target = OUT_DIR / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as source, target.open("wb") as dest:
                dest.write(source.read())
            rows.append({
                "source": info.filename,
                "target": f"/wp-content/uploads/{relative.as_posix()}",
                "size": info.file_size,
                "extension": target.suffix.lower()
            })

    with (REPORT_DIR / "safe-media.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "size", "extension"])
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "safe_media_files": len(rows),
        "extensions": {}
    }
    for row in rows:
        summary["extensions"][row["extension"]] = summary["extensions"].get(row["extension"], 0) + 1
    (REPORT_DIR / "safe-media-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
