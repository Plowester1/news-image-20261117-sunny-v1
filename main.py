"""news-image-20261117 entry (sunny variant): copy the bundled image to
/output/entry.png.

Deterministic: a pure file copy, no network, no randomness — both runs
write the same bytes. The image (entry.png, beside this file) is a
1024x1024 infographic summing up Tuesday 17 November 2026's world news
in eight stories, composed programmatically with PIL (see build_image.py).
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    dst = os.path.join(DST_DIR, "entry.png")
    shutil.copyfile(SRC, dst)
    # Fail loudly instead of submitting a truncated or corrupt copy:
    # the competition runs this program twice and both runs must write
    # the same bytes, so verify the output is byte-identical to the
    # source and still within the 1 MiB size limit.
    if _sha256(dst) != _sha256(SRC):
        raise SystemExit("entry.png copy mismatch: output differs from source")
    if os.path.getsize(dst) > 1 << 20:
        raise SystemExit("entry.png exceeds the 1 MiB limit")


if __name__ == "__main__":
    main()
