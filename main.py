#!/usr/bin/env python3
"""news-23 b84 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import binascii
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_NAME = "entry.png"
MAX_BYTES = 1024 * 1024
MIN_BYTES = 10000


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def parse_png(data):
    """Validate the PNG header and chunk structure; return (width, height)."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG (bad signature)")
    if len(data) < 33:
        raise ValueError("file too short for IHDR")
    if data[12:16] != b"IHDR":
        raise ValueError("first chunk is not IHDR")
    w, h, bit_depth, color_type = struct.unpack(">IIBB", data[16:26])
    if (w, h) != (1024, 1024):
        raise ValueError("expected 1024x1024, got %dx%d" % (w, h))
    if bit_depth != 8:
        raise ValueError("expected bit depth 8, got %d" % bit_depth)
    if color_type not in (2, 6):
        raise ValueError("expected colour type 2 or 6, got %d" % color_type)
    # Walk chunks, verifying CRCs; require a non-empty IDAT and a well-formed IEND.
    off = 8
    seen_idat = False
    seen_iend = False
    while off + 8 <= len(data):
        length = struct.unpack(">I", data[off:off + 4])[0]
        ctype = data[off + 4:off + 8]
        if off + 12 + length > len(data):
            raise ValueError("truncated chunk %r" % ctype)
        stored_crc = struct.unpack(">I", data[off + 8 + length:off + 12 + length])[0]
        calc_crc = binascii.crc32(ctype + data[off + 8:off + 8 + length]) & 0xFFFFFFFF
        if stored_crc != calc_crc:
            raise ValueError("CRC mismatch in chunk %r" % ctype)
        if ctype == b"IDAT":
            if length == 0:
                raise ValueError("empty IDAT chunk")
            seen_idat = True
        if ctype == b"IEND":
            if length != 0:
                raise ValueError("IEND must have length 0")
            if off + 12 != len(data):
                raise ValueError("trailing data after IEND")
            seen_iend = True
            break
        off += 12 + length
    if not seen_idat:
        raise ValueError("no IDAT chunk found")
    if not seen_iend:
        raise ValueError("no IEND chunk found")
    return w, h


def main():
    src = os.path.join(HERE, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(HERE)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if not os.path.isfile(src):
        return fail("source %s missing" % src)
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        return fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if len(data) < MIN_BYTES:
        return fail("entry.png is suspiciously small (%d bytes)" % len(data))
    try:
        w, h = parse_png(data)
    except ValueError as e:
        return fail(str(e))
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, SRC_NAME)
    # Never clobber the source itself (e.g. MAKEFUN_OUTPUT_DIR pointing at HERE).
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output path would overwrite the source entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        return fail("output does not match source byte-for-byte")
    print("ok: wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (dst, w, h, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
