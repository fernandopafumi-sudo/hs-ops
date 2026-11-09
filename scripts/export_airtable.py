#!/usr/bin/env python3
"""Export diario de Airtable -> airtable/<base>/ (esquema + registros por tabla).

Env: AIRTABLE_TOKEN (PAT solo lectura: data.records:read, schema.bases:read).
Opcionales: AIRTABLE_BASES (coma), OUT_DIR (airtable), MIN_TABLES (5).
"""
import json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_make import redact, redactions, slug, dump  # mismos patrones de secretos

TOKEN = os.environ.get("AIRTABLE_TOKEN", "")
BASES = [b for b in os.environ.get(
    "AIRTABLE_BASES",
    "appjkRayvA0YEjczd,appd73iOSApIFksdP,appNQXVewVeJC8Gkx",  # HealthSignals, Brief, Prospect Intelligence
).split(",") if b]
OUT = Path(os.environ.get("OUT_DIR", "airtable"))
MIN_TABLES = int(os.environ.get("MIN_TABLES", "5"))
API = "https://api.airtable.com/v0"


def get(url, params=None):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    time.sleep(0.25)  # límite: 5 req/s por base
    for attempt in range(5):
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOKEN}", "User-Agent": "hs-ops-backup/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 4:
                time.sleep(30 if e.code == 429 else 3 * 2 ** attempt)
                continue
            raise SystemExit(f"HTTP {e.code} en {url.split('?')[0]}: {e.read()[:300]!r}")
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < 4:
                time.sleep(3 * 2 ** attempt)
                continue
            raise SystemExit(f"Red en {url}: {e}")


def main():
    if not TOKEN:
        sys.exit("Falta AIRTABLE_TOKEN")
    total_tables, summary = 0, []
    for base in BASES:
        base_dir = OUT / base
        if base_dir.exists():  # una tabla borrada en Airtable desaparece del repo (queda en el historial)
            for f in base_dir.glob("*.json"):
                f.unlink()
        tables = get(f"{API}/meta/bases/{base}/tables").get("tables", [])
        dump(base_dir / "_schema.json", tables)
        for t in tables:
            records, offset = [], None
            while True:
                params = {"pageSize": 100}
                if offset:
                    params["offset"] = offset
                page = get(f"{API}/{base}/{t['id']}", params)
                records += page.get("records", [])
                offset = page.get("offset")
                if not offset:
                    break
            records.sort(key=lambda r: r["id"])
            for r in records:
                for v in r.get("fields", {}).values():  # URLs firmadas de adjuntos vencen y ensucian el diff
                    if isinstance(v, list):
                        for a in v:
                            if isinstance(a, dict) and "url" in a:
                                a.pop("url", None)
                                a.pop("thumbnails", None)
            dump(base_dir / f"{t['id']}-{slug(t['name'])}.json", redact(records, f"{base}/{t['name']}"))
            summary.append(f"{base}/{t['name']}: {len(records)}")
            total_tables += 1
    dump(OUT / "redactions.json", sorted(set(redactions)))
    print("OK Airtable:\n  " + "\n  ".join(summary))
    if total_tables < MIN_TABLES:
        sys.exit(f"Export sospechoso: {total_tables} tablas (mín {MIN_TABLES}). Revisar token y bases.")


if __name__ == "__main__":
    main()
