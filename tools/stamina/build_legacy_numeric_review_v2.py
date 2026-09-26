#!/usr/bin/env python3

import json
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()

PACKETS = ROOT / "tools/stamina/data/legacy_review_packets_v2.json"

OUT_JSON = ROOT / "tools/stamina/data/legacy_numeric_review_v2.json"
OUT_MD = ROOT / "tools/stamina/reports/legacy_numeric_review_v2.md"


def load(path):
    return json.loads(path.read_text())


def numeric_pair(details, key):
    d = details.get(key)

    if not isinstance(d, dict):
        return None

    old = d.get("v1")
    new = d.get("v2")

    if not isinstance(old, (int, float)):
        return None

    if not isinstance(new, (int, float)):
        return None

    return old, new


def power_metrics(details):
    pair = numeric_pair(details, "power")

    if pair is None:
        return None

    old, new = pair
    delta = new - old

    ratio = None

    if old != 0:
        ratio = delta / abs(old)

    # Power=1 is commonly a sentinel for an effect-specific
    # damage formula rather than literal 1 BP.
    semantic = None

    if old == 1 or new == 1:
        semantic = "VARIABLE_OR_SENTINEL_POWER"

    return {
        "old": old,
        "new": new,
        "delta": delta,
        "ratio": ratio,
        "semantic": semantic,
    }


def accuracy_metrics(details):
    pair = numeric_pair(details, "accuracy")

    if pair is None:
        return None

    old, new = pair

    # Expansion uses accuracy=0 for moves that do not perform
    # the ordinary accuracy/evasion check. It must never be
    # interpreted numerically as 0% accuracy.
    semantic = None

    if old == 0 or new == 0:
        semantic = "NO_NORMAL_ACCURACY_CHECK"

    return {
        "old": old,
        "new": new,
        "delta": new - old,
        "semantic": semantic,
    }


def classify_numeric(power, accuracy):
    # Representation / custom-formula cases must be resolved
    # semantically before ordinary numeric comparisons.
    if power and power.get("semantic"):
        return "POWER_SENTINEL_REVIEW"

    if accuracy and accuracy.get("semantic"):
        return "ACCURACY_SEMANTICS_REVIEW"

    power_delta = power["delta"] if power else 0
    power_ratio = power["ratio"] if power else None

    acc_delta = accuracy["delta"] if accuracy else 0

    # ----------------------------------------------------------
    # Truly transformative changes
    # ----------------------------------------------------------

    if (
        power_delta >= 30
        or (
            power_ratio is not None
            and power_ratio >= 0.50
            and power_delta >= 20
        )
        or acc_delta >= 30
    ):
        return "TRANSFORMATIVE_UPGRADE"

    if (
        power_delta <= -30
        or (
            power_ratio is not None
            and power_ratio <= -0.50
            and power_delta <= -20
        )
        or acc_delta <= -30
    ):
        return "TRANSFORMATIVE_NERF"

    # ----------------------------------------------------------
    # Major absolute changes
    # ----------------------------------------------------------

    if power_delta >= 20 or acc_delta >= 20:
        return "MAJOR_UPGRADE"

    if power_delta <= -20 or acc_delta <= -20:
        return "MAJOR_NERF"

    # ----------------------------------------------------------
    # This is the bucket we especially care about:
    # old low-power moves can trip a 25% ratio threshold despite
    # a small absolute change.
    # ----------------------------------------------------------

    if (
        power_ratio is not None
        and abs(power_ratio) >= 0.25
        and abs(power_delta) < 20
        and abs(acc_delta) < 20
    ):
        return "RATIO_ONLY_SMALL_CHANGE"

    # ----------------------------------------------------------
    # Ordinary moderate changes
    # ----------------------------------------------------------

    if power_delta > 0 or acc_delta > 0:
        return "MODERATE_UPGRADE"

    if power_delta < 0 or acc_delta < 0:
        return "MODERATE_NERF"

    return "OTHER"


doc = load(PACKETS)

moves = [
    x for x in doc["moves"]
    if x["review"]["family"] == "MAJOR_NUMERIC_PROFILE"
]

assert len(moves) == 71, (
    f"Expected 71 major numeric-profile moves, got {len(moves)}"
)


rows = []

for x in moves:
    details = x["migration_diff"]["details"]
    changes = set(x["migration_diff"]["changes"])

    power = power_metrics(details)
    accuracy = accuracy_metrics(details)

    numeric_bucket = classify_numeric(
        power,
        accuracy,
    )

    # Anything beyond plain power/accuracy/category deserves
    # attention because raw numeric deltas may not tell the full story.
    coupled_changes = sorted(
        c for c in changes
        if c not in {
            "power_changed",
            "accuracy_changed",
            "damage_category_changed",
        }
    )

    mechanic_coupled = bool(coupled_changes)

    row = {
        "numeric_id": x["numeric_id"],
        "constant": x["constant"],
        "name": x["name"],

        "legacy_cost": x["legacy"]["cost"],
        "legacy_role": x["legacy"]["primary_role"],
        "legacy_tags": x["legacy"]["mechanic_tags"],
        "legacy_rules": x["legacy"]["stamina_rules"],

        "numeric_bucket": numeric_bucket,
        "mechanic_coupled": mechanic_coupled,
        "coupled_changes": coupled_changes,

        "power": power,
        "accuracy": accuracy,

        "category_change":
            details.get("category"),

        "changes":
            x["migration_diff"]["changes"],

        "modern": x["modern"],
        "campaign_context":
            x["campaign_context"],

        "decision": {
            "status": "PENDING",
            "approved_cost": None,
            "reasoning": [],
        },
    }

    rows.append(row)


bucket_priority = {
    "POWER_SENTINEL_REVIEW": 0,
    "ACCURACY_SEMANTICS_REVIEW": 1,
    "TRANSFORMATIVE_UPGRADE": 2,
    "TRANSFORMATIVE_NERF": 3,
    "MAJOR_UPGRADE": 4,
    "MAJOR_NERF": 5,
    "RATIO_ONLY_SMALL_CHANGE": 6,
    "MODERATE_UPGRADE": 7,
    "MODERATE_NERF": 8,
    "OTHER": 9,
}


rows.sort(
    key=lambda x: (
        bucket_priority[x["numeric_bucket"]],
        0 if x["mechanic_coupled"] else 1,
        x["numeric_id"],
    )
)


bucket_counts = Counter(
    x["numeric_bucket"]
    for x in rows
)

coupled_count = sum(
    1 for x in rows
    if x["mechanic_coupled"]
)


output = {
    "schema":
        "firered-reimagined.stamina.legacy-numeric-review.v2",
    "schema_version": 1,

    "summary": {
        "count": len(rows),
        "mechanic_coupled_count": coupled_count,
        "bucket_counts":
            dict(bucket_counts),
    },

    "moves": rows,
}


OUT_JSON.write_text(
    json.dumps(output, indent=2) + "\n"
)


lines = [
    "# Stamina V2 — Legacy Review Batch 03",
    "",
    "## Major Numeric Profile",
    "",
    f"Moves: **{len(rows)}**",
    f"Mechanically coupled: **{coupled_count}**",
    "",
]


current_bucket = None

for x in rows:
    bucket = x["numeric_bucket"]

    if bucket != current_bucket:
        current_bucket = bucket

        lines += [
            "",
            f"## {bucket}",
            "",
        ]

    p = x["power"]
    a = x["accuracy"]

    ptext = "—"

    if p:
        ratio = (
            f"{p['ratio']:+.1%}"
            if p["ratio"] is not None
            else "n/a"
        )

        ptext = (
            f"{p['old']} → {p['new']} "
            f"({p['delta']:+}, {ratio})"
        )

    atext = "—"

    if a:
        atext = (
            f"{a['old']} → {a['new']} "
            f"({a['delta']:+})"
        )

    coupled = (
        ", ".join(x["coupled_changes"])
        if x["coupled_changes"]
        else "none"
    )

    lines += [
        f"### {x['constant']} — {x['name']}",
        "",
        f"- V1 cost: **{x['legacy_cost']}**",
        f"- Power: {ptext}",
        f"- Accuracy: {atext}",
        f"- Category change: "
        f"`{x['category_change']}`",
        f"- Coupled mechanics: `{coupled}`",
        "",
    ]


OUT_MD.write_text(
    "\n".join(lines) + "\n"
)


print("Numeric review stratification complete.")
print()
print("TOTAL:", len(rows))
print("MECHANIC_COUPLED:", coupled_count)
print()

for bucket in bucket_priority:
    print(
        f"{bucket:<28}",
        bucket_counts.get(bucket, 0),
    )

print()
print("MOVES")
print()

for x in rows:
    p = x["power"]
    a = x["accuracy"]

    ptext = "-"

    if p:
        ptext = f"{p['old']}->{p['new']}"

    atext = "-"

    if a:
        atext = f"{a['old']}->{a['new']}"

    marker = "*" if x["mechanic_coupled"] else " "

    print(
        f"{marker} "
        f"{x['numeric_id']:>3} "
        f"{x['constant']:<28} "
        f"V1={x['legacy_cost']} "
        f"P={ptext:<9} "
        f"A={atext:<9} "
        f"{x['numeric_bucket']}"
    )

print()
print("* = mechanically coupled")
print()
print("Wrote:")
print(" ", OUT_JSON.relative_to(ROOT))
print(" ", OUT_MD.relative_to(ROOT))
