from pathlib import Path
from collections import defaultdict
import shutil

ROOT = Path(".").resolve()
DD = ROOT / "dd"
DD.mkdir(exist_ok=True)

files_by_stem = defaultdict(list)

# collect all files
for f in ROOT.rglob("*"):
    if not f.is_file():
        continue

    # don't scan destination folder itself
    if DD in f.parents:
        continue

    files_by_stem[f.stem.lower()].append(f)

moved = 0

for stem, files in files_by_stem.items():
    exts = {f.suffix.lower() for f in files}

    if ".jpg" in exts or ".jpeg" in exts:
        if ".webp" in exts:
            for f in files:
                if f.suffix.lower() in {".jpg", ".jpeg"}:
                    target = DD / f.name

                    # avoid overwrite
                    if target.exists():
                        n = 1
                        while True:
                            target = DD / f"{f.stem}_{n}{f.suffix}"
                            if not target.exists():
                                break
                            n += 1

                    print(f"Move: {f} -> {target}")
                    shutil.move(str(f), str(target))
                    moved += 1

print(f"\nMoved {moved} jpg/jpeg files.")