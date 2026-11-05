"""Download one file to data/raw/ and print its size and SHA-256."""
import hashlib
import sys
import urllib.request
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"


def download(url, name):
    RAW.mkdir(parents=True, exist_ok=True)
    dest = RAW / name
    # An honest agent, with no contact details. HDX challenged a browser-style one.
    req = urllib.request.Request(url, headers={"User-Agent": "causal-atlas-fetch/0.1"})
    digest = hashlib.sha256()
    with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as out:
        while chunk := resp.read(1 << 20):
            digest.update(chunk)
            out.write(chunk)
    # A challenge page can answer 202 with no body; an empty file must never pass.
    if dest.stat().st_size == 0:
        dest.unlink()
        raise RuntimeError(f"{url} returned an empty body")
    print(f"{name} {dest.stat().st_size} sha256:{digest.hexdigest()}", file=sys.stdout, flush=True)
    return dest
