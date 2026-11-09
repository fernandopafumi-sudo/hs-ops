#!/usr/bin/env python3
"""Genera make/ids.md: qué usa cada escenario (data stores, hooks, conexiones, otros escenarios)."""
import collections, glob, json, re

idx = {s["id"]: s for s in json.load(open("make/scenarios.index.json"))}
ds = {d["id"]: d["name"] for d in json.load(open("make/data-stores.json"))}
hooks = {h["id"]: h for h in json.load(open("make/hooks.json"))}
conns = {c["id"]: c["name"] for c in json.load(open("make/connections.json"))}
rows, ds_users, conn_users = [], collections.defaultdict(set), collections.defaultdict(set)


def walk(o, acc):
    if isinstance(o, dict):
        p = o.get("parameters") or {}
        if isinstance(p, dict):
            for k, v in p.items():
                if k.startswith("__IMTCONN__") and isinstance(v, int):
                    acc["conn"].add(v)
                if k in ("datastore", "dataStore") and isinstance(v, int):
                    acc["ds"].add(v)
                if k == "hook" and isinstance(v, int):
                    acc["hook"].add(v)
        if o.get("module"):
            acc["mods"][o["module"].split(":")[0]] += 1
        for v in o.values():
            walk(v, acc)
    elif isinstance(o, list):
        for v in o:
            walk(v, acc)


for f in sorted(glob.glob("make/scenarios/*.json")):
    d = json.load(open(f))
    acc = {"conn": set(), "ds": set(), "hook": set(), "mods": collections.Counter()}
    walk(d.get("blueprint"), acc)
    txt = json.dumps(d.get("blueprint"))
    calls = {int(x) for x in re.findall(r"\b([56]\d{6})\b", txt) if int(x) in idx and int(x) != d["id"]}
    for x in acc["ds"]:
        ds_users[x].add(d["id"])
    for x in acc["conn"]:
        conn_users[x].add(d["id"])
    sch = d.get("scheduling") or {}
    when = sch.get("time") or sch.get("interval")
    rows.append((d["id"], d["name"], "ON" if d.get("isActive") else "off",
                 sch.get("type", "-") + (f":{when}" if when else ""),
                 ", ".join(f"{x} {ds.get(x, '?')}" for x in sorted(acc["ds"])),
                 ", ".join(str(x) for x in sorted(acc["hook"])),
                 ", ".join(str(x) for x in sorted(calls)),
                 ", ".join(sorted(acc["mods"]))))

out = ["# Mapa de dependencias de Make (generado desde el backup)", "",
       "Regenerar con `python3 scripts/gen_ids.py` después de cada backup. Las referencias desde tareas "
       "programadas de Claude y skills están en `runbooks/scheduled-tasks.md`.", "",
       "## Escenarios", "", "| ID | Nombre | Estado | Schedule | Data stores | Hooks | IDs de escenarios citados | Apps |",
       "|---|---|---|---|---|---|---|---|"]
out += [f"| {' | '.join(str(c) for c in r)} |" for r in rows]
out += ["", "## Data stores → escenarios que los usan", "", "| ID | Nombre | Usado por |", "|---|---|---|"]
out += [f"| {k} | {v} | {', '.join(str(x) for x in sorted(ds_users.get(k, []))) or 'ningún escenario (verificar tareas de Claude)'} |"
        for k, v in sorted(ds.items())]
out += ["", "## Conexiones → escenarios", "", "| ID | Nombre | Escenarios |", "|---|---|---|"]
out += [f"| {k} | {v} | {len(conn_users.get(k, []))}: {', '.join(str(x) for x in sorted(conn_users.get(k, [])))} |"
        for k, v in sorted(conns.items())]
out += ["", "## Webhooks", "", "| ID | Nombre | Escenario |", "|---|---|---|"]
out += [f"| {k} | {h.get('name')} | {h.get('scenarioId')} |" for k, h in sorted(hooks.items())]
open("make/ids.md", "w").write("\n".join(out) + "\n")
print(f"make/ids.md: {len(rows)} escenarios")
