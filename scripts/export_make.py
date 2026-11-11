#!/usr/bin/env python3
"""Export diario de Make -> make/ (blueprints, scheduling, data stores, estructuras, webhooks, conexiones).

Env: MAKE_API_TOKEN (solo lectura). Opcionales: MAKE_ZONE (us2.make.com), MAKE_TEAM_ID (2174293), OUT_DIR (make).
Scopes del token: scenarios:read, datastores:read, udts:read, hooks:read, connections:read.
"""
import json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

ZONE = os.environ.get("MAKE_ZONE", "us2.make.com")
TEAM = os.environ.get("MAKE_TEAM_ID", "2174293")
TOKEN = os.environ.get("MAKE_API_TOKEN", "")
OUT = Path(os.environ.get("OUT_DIR", "make"))
BASE = f"https://{ZONE}/api/v2"
# 148747 Event Dedup, 161375 gate, 162492 Voices Rules, 164495 dedup Social v3
RECORD_STORES = [int(x) for x in os.environ.get("MAKE_RECORD_STORES", "148747,161375,162492,164495").split(",") if x]
MIN_SCENARIOS = int(os.environ.get("MIN_SCENARIOS", "20"))
MIN_STORES = int(os.environ.get("MIN_STORES", "5"))
record_counts = {}

# Patrones de secretos que no deben quedar en git (el valor real vive en Bitwarden)
SECRET_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9_\-]{10,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"sk-(?:proj|svcacct|admin)-[A-Za-z0-9_\-]{20,}"),
    re.compile(r"https://hook\.[a-z0-9]+\.make\.com/[A-Za-z0-9]+"),
    re.compile(r"(?i)\b(?:bearer|basic|token)\s+[A-Za-z0-9+/=._\-]{16,}"),
    re.compile(r"xox[abprs]-[A-Za-z0-9\-]{10,}"),
    re.compile(r"(?i)\"(?:api[_-]?key|apikey|token|secret|password|access_token)\"\s*:\s*\"[^\"]{12,}\""),
    re.compile(r"xkeysib-[A-Za-z0-9\-]{20,}"),          # Brevo
    re.compile(r"pat[A-Za-z0-9]{14}\.[A-Za-z0-9]{20,}"),  # Airtable PAT
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"AIza[0-9A-Za-z_\-]{35}"),
    re.compile(r"(?i)(api[_-]?key|apikey|token|secret|password)=([^&\s\"']{12,})"),
]
redactions = []


SENSITIVE_NAME = re.compile(r"(?i)^(authorization|api[-_]?key|x-api-key|token|secret|password|access[-_]?token)$")


def redact(obj, where):
    if isinstance(obj, dict):
        label = obj.get("key") or obj.get("name")
        if isinstance(label, str) and SENSITIVE_NAME.match(label) and isinstance(obj.get("value"), str) and obj["value"]:
            redactions.append(f"{where}.value")
            obj = {**obj, "value": "<<REDACTED>>"}
        return {k: redact(v, f"{where}.{k}") for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact(v, f"{where}[{i}]") for i, v in enumerate(obj)]
    if isinstance(obj, str):
        new = obj
        for p in SECRET_PATTERNS:
            if p.search(new):
                new = p.sub("<<REDACTED>>", new)
        if new != obj:
            redactions.append(where)
        return new
    return obj


class NotFound(Exception):
    pass


def get(path, params=None):
    url = f"{BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    time.sleep(1.1)  # 60 req/min en el plan Core
    for attempt in range(4):
        req = urllib.request.Request(url, headers={"Authorization": f"Token {TOKEN}", "Accept": "application/json", "User-Agent": "hs-ops-backup/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise NotFound(path)
            if e.code in (429, 500, 502, 503, 504) and attempt < 3:
                time.sleep(60 if e.code == 429 else 2 ** attempt * 3)
                continue
            raise SystemExit(f"HTTP {e.code} en {path}: {e.read()[:300]!r}")
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < 3:
                time.sleep(2 ** attempt * 3)
                continue
            raise SystemExit(f"Red en {path}: {e}")


def paged(path, key, extra=None):
    items, seen, offset = [], set(), 0
    while True:
        params = {"teamId": TEAM, "pg[limit]": 100, "pg[offset]": offset, **(extra or {})}
        batch = get(path, params).get(key, [])
        ids = {x.get("id") for x in batch}
        if not batch or ids <= seen:  # endpoint que ignora pg[]: corta en vez de loopear
            return items
        seen |= ids
        items += batch
        if len(batch) < 100:
            return items
        offset += 100


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "sin-nombre"


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n")


def main():
    if not TOKEN:
        sys.exit("Falta MAKE_API_TOKEN")

    scen_dir = OUT / "scenarios"
    if scen_dir.exists():  # borrar exports viejos: un escenario eliminado en Make desaparece del repo
        for f in scen_dir.glob("*.json"):
            f.unlink()

    scenarios = paged("/scenarios", "scenarios", {"pg[sortBy]": "id", "pg[sortDir]": "asc"})
    index, skipped = [], []
    for s in sorted(scenarios, key=lambda x: x["id"]):
        sid = s["id"]
        try:
            bp = get(f"/scenarios/{sid}/blueprint").get("response", {})
        except NotFound:
            skipped.append(sid)  # borrado entre el listado y el fetch
            continue
        doc = {
            "id": sid,
            "name": s.get("name"),
            "folderId": s.get("folderId"),
            "isActive": s.get("isActive"),
            "scheduling": s.get("scheduling") or bp.get("scheduling"),
            "blueprint": bp.get("blueprint"),
        }
        try:  # inputs de los escenarios que se usan como herramienta (MCP); el blueprint no los trae
            itf = get(f"/scenarios/{sid}/interface")
            doc["interface"] = itf.get("interface", itf)
        except NotFound:
            pass
        dump(scen_dir / f"{sid}-{slug(s.get('name') or '')}.json", redact(doc, f"scenario {sid}"))
        index.append({"id": sid, "name": s.get("name"), "isActive": s.get("isActive")})
    dump(OUT / "scenarios.index.json", index)

    stores = paged("/data-stores", "dataStores")
    dump(OUT / "data-stores.json", [
        {k: d.get(k) for k in ("id", "name", "datastructureId", "maxSize", "records", "size")} for d in stores
    ])

    structs = paged("/data-structures", "dataStructures")
    full = []
    for d in structs:
        try:
            full.append(get(f"/data-structures/{d['id']}").get("dataStructure", d))
        except NotFound:
            pass
    dump(OUT / "data-structures.json", redact(full, "data-structures"))

    # Records de los data stores que son estado operativo. Nunca 128118 (X OAuth: client_secret y refresh_token).
    rec_dir = OUT / "data-store-records"
    for f in rec_dir.glob("*.json") if rec_dir.exists() else []:
        f.unlink()
    for ds_id in RECORD_STORES:
        records, offset, missing = [], 0, False
        while True:
            try:
                batch = get(f"/data-stores/{ds_id}/data", {"pg[limit]": 100, "pg[offset]": offset}).get("records", [])
            except NotFound:
                print(f"::warning::Data store {ds_id} no existe (404)")
                missing = True
                break
            records += batch
            if len(batch) < 100:
                break
            offset += 100
        if missing:
            continue
        records.sort(key=lambda r: str(r.get("key")))
        dump(rec_dir / f"{ds_id}.json", redact(records, f"data-store {ds_id}"))
        record_counts[ds_id] = len(records)

    hooks = paged("/hooks", "hooks")  # sin la URL: quien la tiene puede disparar el escenario
    dump(OUT / "hooks.json", [
        {k: h.get(k) for k in ("id", "name", "typeName", "scenarioId", "enabled", "gone")} for h in hooks
    ])

    conns = paged("/connections", "connections")  # solo metadatos, nunca credenciales
    dump(OUT / "connections.json", [
        {k: c.get(k) for k in ("id", "name", "accountName", "accountLabel", "accountType", "scoped", "expire")}
        for c in conns
    ])

    dump(OUT / "redactions.json", sorted(set(redactions)))
    if skipped:
        print(f"Salteados (404): {skipped}")
    print(f"OK: {len(index)} escenarios, {len(stores)} data stores, {len(full)} estructuras, "
          f"{len(hooks)} webhooks, {len(conns)} conexiones, records {record_counts}, "
          f"{len(set(redactions))} campos redactados")

    # Un backup vacío no es un backup: fallar para que no se mande el heartbeat
    if len(index) < MIN_SCENARIOS or len(stores) < MIN_STORES:
        sys.exit(f"Export sospechoso: {len(index)} escenarios (mín {MIN_SCENARIOS}), "
                 f"{len(stores)} data stores (mín {MIN_STORES}). Revisar token, scopes o team.")


if __name__ == "__main__":
    main()
