#!/usr/bin/env python3

import json
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()

REFINED = ROOT / "tools/stamina/data/legacy_migration_refined_v2.json"
ENCODING = ROOT / "tools/stamina/data/legacy_encoding_resolution_v2.json"
MANUAL = ROOT / "tools/stamina/data/legacy_encoding_manual_v2.json"

OUT_JSON = ROOT / "tools/stamina/data/legacy_review_queue_v2.json"
OUT_MD = ROOT / "tools/stamina/reports/legacy_review_queue_v2.md"


def load(path):
    if not path.exists():
        raise SystemExit(f"Missing required input: {path}")

    return json.loads(path.read_text())


refined_doc = load(REFINED)
encoding_doc = load(ENCODING)
manual_doc = load(MANUAL)

refined_rows = [
    x for x in refined_doc["moves"]
    if x["numeric_id"] <= 354
]

encoding_by_move = {
    x["v2_constant"]: x
    for x in encoding_doc["moves"]
}

manual = manual_doc["decisions"]


# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------

if len(refined_rows) != 355:
    raise SystemExit(
        f"Expected 355 legacy slots, got {len(refined_rows)}"
    )

ids = [x["numeric_id"] for x in refined_rows]

if len(ids) != len(set(ids)):
    raise SystemExit("Duplicate legacy numeric IDs detected")


# Every automatic MANUAL_ENCODING_REVIEW result must have an authored
# adjudication in legacy_encoding_manual_v2.json.
missing_manual = []

for name, row in encoding_by_move.items():
    if (
        row["result"] == "MANUAL_ENCODING_REVIEW"
        and name not in manual
    ):
        missing_manual.append(name)

if missing_manual:
    print("Missing manual encoding decisions:")
    for name in missing_manual:
        print(" ", name)

    raise SystemExit(1)


valid_manual_values = {
    "ENCODING_EQUIVALENT",
    "ENCODING_EQUIVALENT_WITH_RESIDUAL_CHANGE",
    "GENUINE_MODERNIZATION",
}

for name, decision in manual.items():
    if decision not in valid_manual_values:
        raise SystemExit(
            f"Invalid manual decision for {name}: {decision}"
        )


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def significant_numeric_change(row):
    details = row.get("details", {})

    power = details.get("power")
    if power and "v1" in power and "v2" in power:
        old = power["v1"]
        new = power["v2"]

        if isinstance(old, int) and isinstance(new, int):
            if old == 0:
                if new != 0:
                    return True
            else:
                delta = abs(new - old)

                if delta >= 20:
                    return True

                if delta / abs(old) >= 0.25:
                    return True

    accuracy = details.get("accuracy")
    if accuracy and "v1" in accuracy and "v2" in accuracy:
        old = accuracy["v1"]
        new = accuracy["v2"]

        if isinstance(old, int) and isinstance(new, int):
            if abs(new - old) >= 20:
                return True

    return False


def review_family(row, manual_decision=None):
    changes = set(row.get("changes", []))

    if manual_decision == "GENUINE_MODERNIZATION":
        return "MECHANIC_MODERNIZATION"

    if {
        "target_changed",
        "priority_changed",
        "type_changed",
    } & changes:
        return "TACTICAL_SEMANTICS"

    if significant_numeric_change(row):
        return "MAJOR_NUMERIC_PROFILE"

    if "effect_representation_changed" in changes:
        return "MECHANIC_IDENTITY"

    if {
        "power_changed",
        "accuracy_changed",
    } & changes:
        return "MINOR_NUMERIC_PROFILE"

    return "GENERAL_MECHANIC_REVIEW"


def make_base(row):
    return {
        "numeric_id": row["numeric_id"],
        "legacy_constant": row["legacy_constant"],
        "v2_constant": row["v2_constant"],
        "name": row["name"],
        "legacy_cost": row["legacy_cost"],
        "legacy_primary_role":
            row.get("legacy_primary_role"),
        "legacy_mechanic_tags":
            row.get("legacy_mechanic_tags", []),
        "legacy_stamina_rules":
            row.get("legacy_stamina_rules", []),
        "changes": row.get("changes", []),
        "details": row.get("details", {}),
    }


# ----------------------------------------------------------------------
# Final classification
# ----------------------------------------------------------------------

rows = []

for row in refined_rows:
    name = row["v2_constant"] or row["legacy_constant"]
    status = row["status"]

    out = make_base(row)

    out["source_status"] = status
    out["encoding_resolution"] = None
    out["manual_encoding_decision"] = None
    out["review_family"] = None
    out["review_reason"] = None


    # --------------------------------------------------------------
    # Existing high-priority mechanical re-audit
    # --------------------------------------------------------------

    if status == "LEGACY_REAUDIT":
        out["final_status"] = "REVIEW_REQUIRED"
        out["review_family"] = review_family(row)
        out["review_reason"] = (
            "Refined migration classified this move as a "
            "material legacy mechanical change."
        )

        rows.append(out)
        continue


    # --------------------------------------------------------------
    # Encoding-review population
    # --------------------------------------------------------------

    if status == "LEGACY_ENCODING_REVIEW":
        enc = encoding_by_move.get(name)

        if enc is None:
            raise SystemExit(
                f"Missing encoding resolution for {name}"
            )

        out["encoding_resolution"] = enc["result"]

        if enc["result"] == "ENCODING_EQUIVALENT":
            residual = enc.get("residual_changes", [])

            out["encoding_residual_changes"] = residual

            # Automatic equivalence already guarantees that the
            # effect representation itself is not a semantic reason
            # to re-cost the move.
            #
            # The refined triage would already have elevated major
            # power/accuracy/target/type/priority changes to
            # LEGACY_REAUDIT. Therefore remaining residuals here are
            # minor enough to carry as V2 candidate costs.
            out["final_status"] = "CARRY_FORWARD"
            out["review_reason"] = (
                "Strict encoding equivalence proven. "
                "Any remaining modernization is below the "
                "mandatory re-audit threshold."
            )

            rows.append(out)
            continue


        # Automatic resolver intentionally left this move for an
        # authored semantic decision.
        decision = manual.get(name)

        if decision is None:
            raise SystemExit(
                f"Missing authored encoding decision for {name}"
            )

        out["manual_encoding_decision"] = decision

        if decision == "ENCODING_EQUIVALENT":
            out["final_status"] = "CARRY_FORWARD"
            out["review_reason"] = (
                "Human adjudication confirmed semantic "
                "equivalence of the modern representation."
            )

        elif decision == (
            "ENCODING_EQUIVALENT_WITH_RESIDUAL_CHANGE"
        ):
            out["final_status"] = "REVIEW_WATCHLIST"
            out["review_family"] = review_family(
                row,
                decision,
            )
            out["review_reason"] = (
                "Core mechanic is encoding-equivalent, but a "
                "residual modern numeric/mechanical change remains."
            )

        elif decision == "GENUINE_MODERNIZATION":
            out["final_status"] = "REVIEW_REQUIRED"
            out["review_family"] = review_family(
                row,
                decision,
            )
            out["review_reason"] = (
                "Human adjudication confirmed a genuine "
                "modern mechanical change."
            )

        rows.append(out)
        continue


    # --------------------------------------------------------------
    # Safe / minor modernizations
    # --------------------------------------------------------------

    if status in {
        "LEGACY_SAFE",
        "LEGACY_MODERNIZED_MINOR",
    }:
        out["final_status"] = "CARRY_FORWARD"

        if status == "LEGACY_SAFE":
            out["review_reason"] = (
                "No meaningful legacy mechanical difference found."
            )
        else:
            out["review_reason"] = (
                "Only minor modernization detected; V1 cost remains "
                "the provisional V2 candidate."
            )

        rows.append(out)
        continue


    raise SystemExit(
        f"Unhandled refined status for {name}: {status}"
    )


rows.sort(key=lambda x: x["numeric_id"])


# ----------------------------------------------------------------------
# Final validation
# ----------------------------------------------------------------------

if len(rows) != 355:
    raise SystemExit(
        f"Expected 355 final legacy rows, got {len(rows)}"
    )

final_counts = Counter(
    x["final_status"]
    for x in rows
)

family_counts = Counter(
    x["review_family"]
    for x in rows
    if x["review_family"]
)

cost_counts_required = Counter(
    x["legacy_cost"]
    for x in rows
    if x["final_status"] == "REVIEW_REQUIRED"
)

cost_counts_watch = Counter(
    x["legacy_cost"]
    for x in rows
    if x["final_status"] == "REVIEW_WATCHLIST"
)


required = [
    x for x in rows
    if x["final_status"] == "REVIEW_REQUIRED"
]

watchlist = [
    x for x in rows
    if x["final_status"] == "REVIEW_WATCHLIST"
]

carry = [
    x for x in rows
    if x["final_status"] == "CARRY_FORWARD"
]


output = {
    "schema":
        "firered-reimagined.stamina.legacy-review-queue.v2",
    "schema_version": 1,

    "policy": {
        "REVIEW_REQUIRED":
            "V1 cost must be reconsidered before V2 freeze.",

        "REVIEW_WATCHLIST":
            "V1 cost remains a plausible candidate, but residual "
            "modernization should receive a quick human check.",

        "CARRY_FORWARD":
            "V1 cost is accepted as the provisional V2 candidate. "
            "It is still subject to later whole-economy balance review.",
    },

    "counts": dict(final_counts),
    "review_family_counts": dict(family_counts),

    "required_legacy_cost_distribution":
        dict(sorted(cost_counts_required.items())),

    "watchlist_legacy_cost_distribution":
        dict(sorted(cost_counts_watch.items())),

    "moves": rows,
}

OUT_JSON.write_text(
    json.dumps(output, indent=2) + "\n"
)


# ----------------------------------------------------------------------
# Human-readable report
# ----------------------------------------------------------------------

lines = [
    "# Stamina V2 — Final Legacy Review Queue",
    "",
    "## Summary",
    "",
    f"- Review required: **{len(required)}**",
    f"- Review watchlist: **{len(watchlist)}**",
    f"- Carry forward: **{len(carry)}**",
    f"- Legacy total: **{len(rows)}**",
    "",
    "## Review-family counts",
    "",
]

for family, count in family_counts.most_common():
    lines.append(
        f"- `{family}`: **{count}**"
    )


lines += [
    "",
    "## Review required",
    "",
]

for x in required:
    change_text = ", ".join(x["changes"]) or "authored"

    lines.append(
        f"- `{x['v2_constant']}` "
        f"— V1 cost **{x['legacy_cost']}** "
        f"— `{x['review_family']}`"
    )
    lines.append(
        f"  - {change_text}"
    )


lines += [
    "",
    "## Review watchlist",
    "",
]

for x in watchlist:
    change_text = ", ".join(x["changes"]) or "authored"

    lines.append(
        f"- `{x['v2_constant']}` "
        f"— V1 cost **{x['legacy_cost']}**"
    )
    lines.append(
        f"  - {change_text}"
    )


lines += [
    "",
    "## Carry-forward candidates",
    "",
]

for x in carry:
    lines.append(
        f"- `{x['v2_constant']}` "
        f"— candidate cost **{x['legacy_cost']}**"
    )


OUT_MD.write_text(
    "\n".join(lines) + "\n"
)


print("Final legacy review queue complete.")
print()

print(f"REVIEW_REQUIRED  : {len(required)}")
print(f"REVIEW_WATCHLIST : {len(watchlist)}")
print(f"CARRY_FORWARD    : {len(carry)}")
print(f"LEGACY_TOTAL     : {len(rows)}")

print()
print("Review families:")

for family, count in family_counts.most_common():
    print(f"  {family:<28} {count}")

print()
print("Required V1 cost distribution:")

for cost, count in sorted(cost_counts_required.items()):
    print(f"  cost {cost}: {count}")

print()
print("Wrote:")
print("  tools/stamina/data/legacy_review_queue_v2.json")
print("  tools/stamina/reports/legacy_review_queue_v2.md")
