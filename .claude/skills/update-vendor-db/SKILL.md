---
name: update-vendor-db
description: Refresh macspoofer/data/vendors.json from Wireshark's upstream manuf OUI file, sanity-check the diff, and commit it. Use when the user asks to update vendors, refresh the OUI/MAC vendor database, sync from manuf, or says the vendor list is stale.
---

# Update the vendor OUI database

`macspoofer/data/vendors.json` is a generated file — never hand-edit it. It maps
canonical vendor name -> sorted list of lowercase `xx:xx:xx` OUIs, and is built from
Wireshark's `manuf` file by `scripts/update_vendor_db.py`.

## Steps

**1. Regenerate**

```bash
python3 scripts/update_vendor_db.py
```

Add `--input path/to/manuf` to build from a local copy instead of downloading.
The script prints "No changes" and leaves the file alone when upstream hasn't moved —
in that case, stop and report that; don't create an empty commit.

**2. Sanity-check the diff**

Upstream additions are incremental. A healthy update adds tens-to-low-hundreds of OUIs
and removes very few. Compare against `HEAD`:

```bash
python3 - <<'PY'
import json, subprocess
new = json.load(open('macspoofer/data/vendors.json'))
old = json.loads(subprocess.run(
    ['git', 'show', 'HEAD:macspoofer/data/vendors.json'],
    capture_output=True, text=True).stdout)
print('vendors old/new:', len(old), len(new))
print('ouis    old/new:', sum(map(len, old.values())), sum(map(len, new.values())))
print('added  :', sorted(set(new) - set(old)))
print('removed:', sorted(set(old) - set(new)))
PY
```

Stop and ask the user before committing if any of these hold — they signal a bad
download or a parser/alias regression rather than a normal upstream refresh:

- total OUI count *drops*, or the file shrinks noticeably
- hundreds of vendors disappear at once
- removals aren't explainable as renames (upstream reformats names constantly, e.g.
  `Hyundai Telecom` -> `HYUNDAI HT`, `PURE Storage` -> `Pure Storage`)

**3. Verify the package still loads it**

```bash
python3 -c "
from macspoofer.utils.vendors import VendorRegistry as V
missing = [v for v in V.FEATURED if not V.get_ouis_for_vendor(v)]
print('vendor_count:', V.vendor_count())
print('missing featured:', missing)
"
```

`missing featured` **must** be empty. `VendorRegistry.FEATURED` in
`macspoofer/utils/vendors.py` hardcodes display names like `Apple`, `TP-Link`, `Hon Hai
/ Foxconn`; those only exist because `VENDOR_ALIASES` in `scripts/update_vendor_db.py`
maps upstream's truncated short names onto them. When upstream changes a short name the
alias stops matching, the vendor silently splits into an un-normalised variant, and the
featured entry goes empty.

Fix by adding the new short name to `VENDOR_ALIASES` (grep the raw manuf file for the
OUI to find what upstream now calls it), then rerun from step 1.

**4. Commit**

Only `macspoofer/data/vendors.json` (plus `scripts/update_vendor_db.py` if aliases
changed). The established message for this repo is:

```
chore(manuf): update vendors.json
```

## Notes

- The script keeps only 24-bit OUIs; 28-/36-bit sub-allocations (`/28`, `/36`) and
  `Private` / IEEE-registry blocks are dropped by design.
- `pyproject.toml` already ships the JSON in the wheel via `include`; no packaging
  change is needed when the data updates.
