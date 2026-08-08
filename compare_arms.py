#!/usr/bin/env python3
"""Paired comparison of the two predictor arms.

The Claude arm mirrors a subset of the primary ledger's event-move claims
EXACTLY - same claim, same resolution rule, same dates - so question difficulty
is held constant and the only difference is the probability. That makes this a
PAIRED comparison, which is far more powerful at small n than comparing two
independent question sets.

Scores only pairs where the shared claim has RESOLVED in the primary ledger.
Run after `python score.py --resolve`.

    python compare_arms.py
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIMARY = HERE / "predictions.json"
CLAUDE = HERE / "predictions_claude.json"


def load(p: Path) -> list[dict]:
    return json.loads(p.read_text(encoding="utf-8"))["predictions"]


def main() -> None:
    primary = {e["id"]: e for e in load(PRIMARY)}
    claude = load(CLAUDE)

    pairs = []
    unresolved = 0
    for c in claude:
        src = primary.get(c.get("mirrors"))
        if src is None:
            continue
        if src.get("outcome") is None:
            unresolved += 1
            continue
        o = int(src["outcome"])
        pairs.append(
            {
                "claim": src["claim"],
                "resolve_date": src["resolve_date"],
                "outcome": o,
                "p_matt": float(src["prob"]),
                "p_claude": float(c["prob"]),
                "b_matt": (float(src["prob"]) - o) ** 2,
                "b_claude": (float(c["prob"]) - o) ** 2,
            }
        )

    print(f"# Paired arm comparison\n")
    print(f"mirrored pairs: {len(pairs) + unresolved}  |  resolved: {len(pairs)}  |  awaiting: {unresolved}\n")

    if not pairs:
        print("Nothing resolved yet - the comparison populates as the shared claims come due.")
        print("The first pair resolves 2026-08-12 (SUN, CBA).")
        return

    pairs.sort(key=lambda r: r["resolve_date"])
    print(f"{'date':12} {'outcome':8} {'p_matt':>7} {'p_claude':>9} {'B_matt':>7} {'B_claude':>9}  claim")
    for r in pairs:
        print(
            f"{r['resolve_date']:12} {('HIT' if r['outcome'] else 'MISS'):8} "
            f"{r['p_matt']:7.2f} {r['p_claude']:9.2f} {r['b_matt']:7.4f} {r['b_claude']:9.4f}  {r['claim'][:58]}"
        )

    n = len(pairs)
    bm = sum(r["b_matt"] for r in pairs) / n
    bc = sum(r["b_claude"] for r in pairs) / n
    diffs = [r["b_matt"] - r["b_claude"] for r in pairs]
    mean_d = sum(diffs) / n
    wins = sum(1 for d in diffs if d > 0)      # Claude closer on this pair
    losses = sum(1 for d in diffs if d < 0)

    print()
    print(f"Brier  Matt   : {bm:.4f}")
    print(f"Brier  Claude : {bc:.4f}")
    print(f"paired mean difference (Matt - Claude): {mean_d:+.4f}"
          f"  ({'Claude' if mean_d > 0 else 'Matt'} better)")
    print(f"pairs where Claude was closer: {wins}/{n}  |  Matt closer: {losses}/{n}")

    # Sign test, exact binomial two-sided, no scipy dependency.
    dec = wins + losses
    if dec:
        from math import comb
        k = max(wins, losses)
        tail = sum(comb(dec, i) for i in range(k, dec + 1)) / (2 ** dec)
        p = min(1.0, 2 * tail)
        print(f"sign test (exact, two-sided): p = {p:.3f}")

    print()
    if n < 20:
        print(
            f"WARNING: n={n}. This CANNOT distinguish skill from noise. The primary run's own power\n"
            f"    calculation put the threshold near 21 for detecting even gross miscalibration,\n"
            f"    and a paired design helps with variance but does not manufacture sample size.\n"
            f"    Read the direction, not the verdict."
        )


if __name__ == "__main__":
    main()
