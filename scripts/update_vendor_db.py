#!/usr/bin/env python3
"""Update the vendor OUI database from Wireshark's manuf file.

Downloads (or reads a local copy of) the Wireshark manufacturer database and
produces a normalised JSON mapping used at runtime by VendorRegistry.

Usage:
    python scripts/update_vendor_db.py                         # download latest
    python scripts/update_vendor_db.py --input manuf.txt       # use local file
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import ssl
import urllib.request
from collections import defaultdict

MANUF_URL = "https://www.wireshark.org/download/automated/data/manuf"
OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "macspoofer",
    "data",
    "vendors.json",
)

# Maps truncated Wireshark short names to a canonical display name.
# Only needed when the short name is ambiguous or ugly.
VENDOR_ALIASES: dict[str, str] = {
    "HuaweiTechno": "Huawei",
    "HuaweiDevice": "Huawei",
    "SamsungElect": "Samsung",
    "TexasInstrum": "Texas Instruments",
    "HewlettPacka": "HP",
    "XiaomiCommun": "Xiaomi",
    "FiberhomeTel": "Fiberhome",
    "SagemcomBroa": "Sagemcom",
    "JuniperNetwo": "Juniper",
    "AmazonTechno": "Amazon",
    "OppoMobileTe": "OPPO",
    "TpLinkTechno": "TP-Link",
    "vivoMobileCo": "Vivo",
    "HonHaiPrecis": "Hon Hai / Foxconn",
    "SiliconLabor": "Silicon Labs",
    "MotorolaMobi": "Motorola",
    "NewH3CTechno": "New H3C",
    "LGElectronic": "LG",
    "SuZhouNewLan": "New Land",
    "IeeeRegistra": "IEEE Registration Authority",
    "ArrisSolutio": "Arris",
    "Super Micro": "Supermicro",
    "SuperMicroCo": "Supermicro",
    "AzureWaveTec": "AzureWave",
    "RivetNetwork": "Rivet Networks",
    "LiteonTechno": "Liteon",
    "Routerboard.": "MikroTik",
    "Routerboard": "MikroTik",
    "Ieee802.1Qbg": "IEEE 802.1",
    "QualcommTech": "Qualcomm",
    "MurataManufa": "Murata",
    "RealTek": "Realtek",
    "CiscoMeraki": "Cisco",
    "CiscoSystems": "Cisco",
    "CiscoSpvtg": "Cisco",
    "DellTechnolo": "Dell",
    "SonyInteract": "Sony",
    "SonyMobileCo": "Sony",
    "NokiaShangha": "Nokia",
    "NokiaDanmark": "Nokia",
    "NokiaSolutio": "Nokia",
    "GoogleInc.": "Google",
    "Commscope": "CommScope",
    "CommScope": "CommScope",
    "zte": "ZTE",
    "Espressif": "Espressif",
    "Intelbras": "Intelbras",
}

# Regex: capitalised words, ignoring trailing abbreviations like "Inc.", "Ltd."
_WORD_BOUNDARY_RE = re.compile(r"(?<=[a-z])(?=[A-Z])")


def _normalise_vendor(short_name: str, full_name: str) -> str:
    """Return a human-friendly canonical vendor name."""
    if short_name in VENDOR_ALIASES:
        return VENDOR_ALIASES[short_name]

    # Use the full name but strip common suffixes
    cleaned = full_name.strip()
    for suffix in (
        ", Inc.",
        ", Inc",
        " Inc.",
        " Inc",
        " Corporation",
        " Corporate",
        " Corp.",
        " Corp",
        " Co., Ltd.",
        " Co.,Ltd.",
        " Co., Ltd",
        " Co.,Ltd",
        " Co. Ltd.",
        " Co. Ltd",
        " Ltd.",
        " Ltd",
        " Limited",
        " LLC",
        " L.L.C.",
        " GmbH",
        " AG",
        " S.A.",
        " S.p.A.",
        " S.p.A",
        " Pty",
        " B.V.",
        " A/S",
        " AB",
        " Pte",
        " Pvt",
        " Technologies",
        " Technology",
        " Electronics",
        " Electric",
        " International",
        " Semiconductor",
        " Systems",
        " Solutions",
        " Communications",
        " Communication",
        " Networks",
        " Networking",
        " Computer",
        " Computers",
    ):
        if cleaned.endswith(suffix):
            cleaned = cleaned[: -len(suffix)].rstrip(" ,")

    return cleaned if cleaned else full_name.strip()


def _parse_manuf_line(line: str) -> tuple[str, str, str] | None:
    """Parse a single manuf line. Returns (mac_prefix, short_name, full_name) or None."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    parts = line.split("\t")
    if len(parts) < 2:
        return None

    mac_block = parts[0].strip()
    # Skip 28-bit and 36-bit sub-allocations, we only want standard 24-bit OUIs
    if "/" in mac_block or len(mac_block.replace(":", "").replace("-", "")) > 6:
        return None

    short_name = parts[1].strip() if len(parts) > 1 else ""
    full_name = parts[2].strip() if len(parts) > 2 else short_name

    oui = mac_block.upper().replace("-", ":").rstrip(":")
    # Normalise to XX:XX:XX
    hex_digits = oui.replace(":", "")
    if len(hex_digits) != 6:
        return None
    oui = f"{hex_digits[0:2]}:{hex_digits[2:4]}:{hex_digits[4:6]}"

    return oui, short_name, full_name


def build_vendor_db(lines: list[str]) -> dict[str, list[str]]:
    """Build vendor -> [OUI, ...] mapping from manuf lines."""
    vendor_ouis: dict[str, list[str]] = defaultdict(list)
    skipped = 0

    for line in lines:
        parsed = _parse_manuf_line(line)
        if parsed is None:
            continue

        oui, short_name, full_name = parsed
        if short_name in ("Private", "IeeeRegistra"):
            skipped += 1
            continue

        vendor = _normalise_vendor(short_name, full_name)
        oui_lower = oui.lower()
        if oui_lower not in vendor_ouis[vendor]:
            vendor_ouis[vendor].append(oui_lower)

    print(
        f"Parsed {sum(len(v) for v in vendor_ouis.values())} OUIs across {len(vendor_ouis)} vendors (skipped {skipped} private/reserved)"
    )
    return dict(vendor_ouis)


def download_manuf() -> list[str]:
    """Download the latest manuf file from Wireshark."""
    print(f"Downloading {MANUF_URL} ...")
    req = urllib.request.Request(MANUF_URL, headers={"User-Agent": "MacSpoofer/build"})

    try:
        resp = urllib.request.urlopen(req, timeout=30)
    except urllib.error.URLError as exc:
        if "CERTIFICATE_VERIFY_FAILED" not in str(exc):
            raise
        print("WARNING: SSL verification failed, retrying without verification.")
        print("  Tip: run 'pip install certifi' or install macOS Python certificates.")
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        resp = urllib.request.urlopen(req, timeout=30, context=ctx)

    with resp:
        data = resp.read().decode("utf-8", errors="replace")

    lines = data.splitlines()
    print(f"Downloaded {len(lines)} lines")
    return lines


def _file_hash(path: str) -> str | None:
    """Return SHA-256 hex digest of a file, or None if it doesn't exist."""
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Update vendor OUI database")
    parser.add_argument("--input", "-i", help="Path to local manuf file (skip download)")
    args = parser.parse_args()

    if args.input:
        with open(args.input, encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
        print(f"Read {len(lines)} lines from {args.input}")
    else:
        lines = download_manuf()

    vendor_db = build_vendor_db(lines)

    # Sort vendors alphabetically, sort OUIs within each vendor
    sorted_db = {k: sorted(v) for k, v in sorted(vendor_db.items(), key=lambda x: x[0].lower())}

    old_hash = _file_hash(OUTPUT_PATH)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    new_content = json.dumps(sorted_db, indent=2) + "\n"
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    new_hash = hashlib.sha256(new_content.encode()).hexdigest()

    if old_hash is None:
        print(f"\nCreated {OUTPUT_PATH} ({os.path.getsize(OUTPUT_PATH):,} bytes)")
    elif old_hash == new_hash:
        print("\nNo changes, vendors.json is already up to date.")
    else:
        print(f"\nUpdated {OUTPUT_PATH} ({os.path.getsize(OUTPUT_PATH):,} bytes)")
        print("Run 'git diff macspoofer/data/vendors.json' to review changes.")


if __name__ == "__main__":
    main()
