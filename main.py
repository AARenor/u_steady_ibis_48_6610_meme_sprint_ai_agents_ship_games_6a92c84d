#!/usr/bin/env python3
"""Write the competition meme to /output/entry.png.

The artwork ships with the repository as art.png.  This program only reads
that bundled file, verifies the house gate constraints, and writes the single
artifact the judge sees.  It needs no network and no third-party packages.
"""

import os
from pathlib import Path
import struct
import sys
OUTPUT = Path(os.environ.get("MAKEFUN_OUTPUT", "/output/entry.png"))
ART = Path(__file__).resolve().with_name("art.png")
MAX_BYTES = 1_048_576
SIZE = (1024, 1024)

# The judge's gate is strict about the signature, IHDR dimensions and total
# size.  Keep this check in the entry so a bad bundled asset fails locally
# instead of producing an invalid artifact in the final sandbox.
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
IEND_CRC = b"\xaeB`\x82"


def check_png(data: bytes) -> None:
    """Fail loudly unless data is a complete PNG of the required size."""
    if data[:8] != PNG_SIGNATURE or data[-8:-4] != b"IEND" or data[-4:] != IEND_CRC:
        raise ValueError("art.png is not a complete PNG")
    if len(data) > MAX_BYTES:
        raise ValueError(f"art.png is {len(data)} bytes; limit is {MAX_BYTES}")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != SIZE:
        raise ValueError(f"art.png is {width}x{height}, expected 1024x1024")


def main() -> int:
    data = ART.read_bytes()
    check_png(data)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(data)
    print(f"wrote {OUTPUT} ({len(data)} bytes, 1024x1024)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
