#!/usr/bin/env python3
"""Rebuild index.json from the files in lyrics/ (run from the repository root: python scripts/build_index.py).

File name convention: `<artist>[,<artist>...] - <title>.lrc` (several artists are separated by a comma; the first
" - " splits artists from the title, so a title may contain " - ").
Duration (`durationMs`, otherwise null): `durations.json` in the repository root maps a lyrics file name to its length as
"m:ss" (for example {"x - y.lrc": "3:28"}); a `[length:mm:ss]` tag inside the LRC is used when the file is not listed.
The app (MoeMusicPlayer) reads index.json to find a song by title and artist.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LYRICS = ROOT / "lyrics"
LENGTH = re.compile(r"^\[length:\s*(\d+):(\d{1,2})(?:\.(\d+))?\s*\]", re.MULTILINE)


def parse_m_ss(value):
    match = re.fullmatch(r"\s*(\d+):(\d{1,2})(?:\.(\d+))?\s*", str(value))
    if not match:
        return None
    minutes, seconds, fraction = int(match.group(1)), int(match.group(2)), match.group(3) or "0"
    return (minutes * 60 + seconds) * 1000 + int((fraction + "000")[:3])


def load_durations():
    path = ROOT / "durations.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def duration_ms(text):
    match = LENGTH.search(text)
    if not match:
        return None
    minutes, seconds, fraction = int(match.group(1)), int(match.group(2)), match.group(3) or "0"
    return (minutes * 60 + seconds) * 1000 + int((fraction + "000")[:3])


def main():
    songs = []
    durations = load_durations()
    for path in sorted(LYRICS.glob("*.lrc")):
        stem = path.stem
        if " - " not in stem:
            print(f"skip (no ' - '): {path.name}", file=sys.stderr)
            continue
        artist_part, title = stem.split(" - ", 1)
        artists = [name.strip() for name in artist_part.split(",") if name.strip()]
        title = title.strip()
        if not artists or not title:
            print(f"skip (empty artist or title): {path.name}", file=sys.stderr)
            continue
        text = path.read_text(encoding="utf-8-sig")
        songs.append({
            "title": title,
            "artists": artists,
            "album": None,
            "durationMs": parse_m_ss(durations[path.name]) if path.name in durations else duration_ms(text),
            "file": f"lyrics/{path.name}",
        })
    index = {"version": 1, "songs": songs}
    (ROOT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"index.json: {len(songs)} songs")


if __name__ == "__main__":
    main()
