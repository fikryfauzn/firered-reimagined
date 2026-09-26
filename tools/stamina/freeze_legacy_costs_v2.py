#!/usr/bin/env python3

import json
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()

QUEUE = ROOT / "tools/stamina/data/legacy_review_queue_v2.json"
DECISIONS = ROOT / "tools/stamina/data/legacy_review_decisions_v2.json"

OUT = ROOT / "tools/stamina/data/legacy_costs_v2.json"
REPORT = ROOT / "tools/stamina/reports/legacy_costs_v2.md"


def load(path):
    return json.loads(path.read_text())


queue = load(QUEUE)
decisions = load(DECISIONS)["moves"]

rows = []

for x in queue["moves"]:
    name = x["v2_constant"]

    if x["final_status"] == "CARRY_FORWARD":
        cost = x["legacy_cost"]
        source = "V1_CARRY_FORWARD"
        decision = "CARRY_FORWARD"

    else:
        if name not in decisions:
            raise SystemExit(
                f"Missing human decision: {name}"
            )

        d = decisions[name]

        cost = d["approved_cost"]
        decision = d["decision"]
        source = "HUMAN_REVIEW"

    rows.append({
        "numeric_id": x["numeric_id"],
        "constant": name,
        "name": x["name"],

        "v1_cost": x["legacy_cost"],
        "v2_candidate_cost": cost,

        "changed_from_v1":
            cost != x["legacy_cost"],

        "resolution_source": source,
        "decision": decision,

        "review_family":
            x.get("review_family"),

        "original_queue_status":
            x["final_status"],
    })


rows.sort(key=lambda x: x["numeric_id"])


# ------------------------------------------------------------
# Validation
# ------------------------------------------------------------

assert len(rows) == 355

ids = [x["numeric_id"] for x in rows]

assert ids == list(range(355)), (
    "Legacy numeric IDs are not exactly 0..354"
)

assert len(decisions) == 115, (
    f"Expected 115 human decisions, got {len(decisions)}"
)

for x in rows:
    if not 0 <= x["v2_candidate_cost"] <= 6:
        raise SystemExit(
            f"Invalid cost: {x['constant']} "
            f"{x['v2_candidate_cost']}"
        )


cost_dist = Counter(
    x["v2_candidate_cost"]
    for x in rows
)

changed = [
    x for x in rows
    if x["changed_from_v1"]
]


out = {
    "schema":
        "firered-reimagined.stamina.legacy-costs-v2",
    "schema_version": 1,

    "status":
        "PROVISIONAL_LEGACY_V2",

    "warning":
        "These costs resolve the legacy migration only. "
        "They are not the final whole-system V2 balance freeze; "
        "new moves and global economy review remain pending.",

    "summary": {
        "move_count": len(rows),
        "human_reviewed": len(decisions),
        "carried_forward": sum(
            x["resolution_source"] == "V1_CARRY_FORWARD"
            for x in rows
        ),
        "changed_from_v1": len(changed),
        "cost_distribution":
            dict(sorted(cost_dist.items())),
    },

    "moves": rows,
}


OUT.write_text(
    json.dumps(out, indent=2) + "\n"
)


lines = [
    "# Stamina V2 — Legacy Cost Freeze",
    "",
    "Status: **PROVISIONAL LEGACY V2**",
    "",
    f"- Legacy moves: **{len(rows)}**",
    f"- Human reviewed: **{len(decisions)}**",
    f"- Carry-forward: **{out['summary']['carried_forward']}**",
    f"- Changed from V1: **{len(changed)}**",
    "",
    "## Cost distribution",
    "",
]

for cost, count in sorted(cost_dist.items()):
    lines.append(
        f"- Cost {cost}: **{count}**"
    )


lines += [
    "",
    "## Changed from V1",
    "",
]

for x in changed:
    lines.append(
        f"- `{x['constant']}`: "
        f"**{x['v1_cost']} → {x['v2_candidate_cost']}**"
    )


REPORT.write_text(
    "\n".join(lines) + "\n"
)


print("Legacy V2 candidate freeze complete.")
print()
print("MOVES         :", len(rows))
print("HUMAN REVIEWED:", len(decisions))
print("CARRY FORWARD :", out["summary"]["carried_forward"])
print("CHANGED       :", len(changed))
print()

print("Cost distribution:")

for cost, count in sorted(cost_dist.items()):
    print(f"  cost {cost}: {count}")

print()
print("Wrote:")
print(" ", OUT.relative_to(ROOT))
print(" ", REPORT.relative_to(ROOT))
