#!/usr/bin/env python3
"""Update index.json from the files in lyrics/ (run from the repository root: python scripts/build_index.py).

- A lyrics file that is not in index.json yet gets a new entry made from its file name:
  `<artist>[,<artist>...] - <title>.lrc` (several artists are separated by a comma; the first " - " splits the artists
  from the title, so a title may contain " - "). Its `album` and `durationMs` start as null.
- An entry whose file is still there is kept exactly as it is, so you can edit `title`, `artists`, `album` and
  `durationMs` (milliseconds) by hand in index.json and they are not overwritten.
- An entry whose file is gone is removed.
- The top-level `name` is the source name MoeMusicPlayer shows for these lyrics; it is kept as it is (edit it by hand).
The app (MoeMusicPlayer) reads index.json to find a song by title and artist.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LYRICS = ROOT / "lyrics"
INDEX = ROOT / "index.json"


def load_index():
    if not INDEX.exists():
        return None, {}
    data = json.loads(INDEX.read_text(encoding="utf-8-sig"))
    songs = {song["file"]: song for song in data.get("songs", []) if isinstance(song, dict) and "file" in song}
    return data.get("name"), songs


def entry_from_name(path):
    stem = path.stem
    if " - " not in stem:
        print(f"skip (no ' - '): {path.name}", file=sys.stderr)
        return None
    artist_part, title = stem.split(" - ", 1)
    artists = [name.strip() for name in artist_part.split(",") if name.strip()]
    title = title.strip()
    if not artists or not title:
        print(f"skip (empty artist or title): {path.name}", file=sys.stderr)
        return None
    return {"title": title, "artists": artists, "album": None, "durationMs": None, "file": f"lyrics/{path.name}"}


def main():
    name, existing = load_index()
    songs = []
    added = 0
    for path in sorted(LYRICS.glob("*.lrc")):
        file = f"lyrics/{path.name}"
        if file in existing:
            songs.append(existing[file])
            continue
        entry = entry_from_name(path)
        if entry:
            songs.append(entry)
            added += 1
    removed = len(set(existing) - {song["file"] for song in songs})
    INDEX.write_text(json.dumps({"version": 1, "name": name, "songs": songs} if name else {"version": 1, "songs": songs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"index.json: {len(songs)} songs ({added} added, {removed} removed)")


if __name__ == "__main__":
    main()
