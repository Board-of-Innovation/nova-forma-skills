#!/usr/bin/env python3
"""Value case for redesigning a workflow, as a low and a high case.

Usage: python3 value_case.py inputs.json

Any number in the input may be a single value or a pair such as
{"low": 0.3, "high": 0.6}. Values are per year and before build and
running costs, unless costs are given. references/levers.md lists every
field and the checks this script runs.
"""
import json
import math
import sys


def pick(v, case):
    """Return the value for this case from a number or a low/high pair."""
    if isinstance(v, dict):
        if case in v:
            return float(v[case])
        other = "low" if case == "high" else "high"
        return float(v[other])
    return float(v)


def opt(d, key, case, default=None):
    """Read an optional field, which may be missing, null, a number or a pair."""
    if not d or key not in d or d[key] is None:
        return default
    return pick(d[key], case)


def sig(x, mode="nearest"):
    """Round to two significant figures, rounding down when mode is 'down'."""
    if x == 0:
        return 0.0
    a = abs(x)
    q = 10 ** (int(math.floor(math.log10(a))) - 1)
    a2 = (math.floor(a / q) if mode == "down" else round(a / q)) * q
    return -a2 if x < 0 else a2


def num(x, mode="nearest"):
    if x is None:
        return "n/a"
    v = sig(x, mode)
    a = abs(v)
    if a >= 1e6:
        s = f"{a / 1e6:.3g}M"
    elif a >= 1e3:
        s = f"{a / 1e3:.3g}k"
    else:
        s = f"{a:.3g}"
    return ("-" if v < 0 else "") + s


def months(spend, yearly):
    if spend is None:
        return "n/a"
    if yearly <= 0:
        return "no payback"
    m = spend / yearly * 12
    if m < 1:
        return "under 1 month"
    return "1 month" if round(m) == 1 else f"{m:.0f} months"


def compute(inp, case):
    flags = []
    b = inp["baseline"]
    hours = opt(b, "hours_per_year", case, 0.0)
    hpf = opt(b, "working_hours_per_fte", case, 1700.0)
    cost = opt(b, "loaded_cost_per_fte", case, 0.0)
    team = opt(b, "team_fte", case)
    share = opt(inp, "addressable_share", case, 0.0)
    split = inp.get("capacity_split", {"put_to_use": 1.0, "fte_savings": 0.0})
    s_use = opt(split, "put_to_use", case, 0.0)
    s_fte = opt(split, "fte_savings", case, 0.0)
    if s_use + s_fte > 1.0001:
        flags.append("The capacity split adds up to more than 100%, so hours are counted twice.")

    freed = opt(b, "freed_hours_per_year", case)
    if freed is None:
        freed = hours * share
    if team is not None and freed / hpf > team:
        flags.append(f"Freed time exceeds the team of {team:g} FTE, so it is capped at the team.")
        freed = team * hpf
    r = {"freed": freed, "fte": freed / hpf}
    unassigned = freed * max(0.0, 1.0 - s_use - s_fte)

    use = inp.get("put_to_use")
    r["units"], r["lever_use"] = 0.0, 0.0
    if use and s_use > 0:
        hpu = pick(use["hours_per_unit"], case)
        raw = freed * s_use / hpu
        used = raw
        cap = opt(use, "demand_cap_units", case)
        vol = opt(use, "volume_today", case)
        confirmed = bool(use.get("demand_and_delivery_confirmed", False))
        if cap is not None and used > cap:
            used = cap
            flags.append(f"Extra units are capped at the demand you named: {num(cap)}.")
        if vol is not None and not confirmed and used > 0.25 * vol:
            used = 0.25 * vol
            flags.append(
                f"Extra units are capped at 25% of today's volume, {num(used)}, "
                "until you confirm the demand and the capacity to deliver it."
            )
        unassigned += (raw - used) * hpu
        r["units"] = used
        r["lever_use"] = (used * pick(use["conversion"], case)
                          * pick(use["value_per_unit"], case)
                          * pick(use["contribution_margin"], case))

    fte = inp.get("fte_savings") or {}
    r["lever_fte"] = (freed * s_fte / hpf) * cost * opt(fte, "realization", case, 0.0)

    r["impact"] = [(l["name"], pick({"low": l["low"], "high": l["high"]}, case))
                   for l in inp.get("impact_levers", [])]
    r["creation"] = [(l["name"], pick({"low": l["low"], "high": l["high"]}, case), l.get("break_even", ""))
                     for l in inp.get("value_creation", [])]
    r["lever_impact"] = sum(v for _, v in r["impact"])
    r["lever_creation"] = sum(v for _, v, _ in r["creation"])
    r["value"] = r["lever_use"] + r["lever_fte"] + r["lever_impact"] + r["lever_creation"]
    r["unassigned"] = unassigned

    costs = inp.get("costs") or {}
    opposite = "high" if case == "low" else "low"
    r["yearly_cost"] = opt(costs, "yearly", opposite, 0.0)
    r["one_off"] = opt(costs, "one_off", opposite)
    r["net"] = r["value"] - r["yearly_cost"]

    fin = inp.get("finance") or {}
    rate = float(fin.get("discount_rate", 0.08))
    years = int(fin.get("years", 5))
    r["annuity"] = (1 - (1 + rate) ** -years) / rate
    r["npv_ceiling"] = r["net"] * r["annuity"]
    r["rate"], r["years"] = rate, years

    spend = opt(inp, "reference_spend", case)
    r["spend"] = spend
    if spend is not None and use:
        per_unit = pick(use["value_per_unit"], case) * pick(use["contribution_margin"], case)
        r["break_even_units"] = spend / per_unit if per_unit > 0 else None
        conv = pick(use["conversion"], case)
        r["break_even_requests"] = r["break_even_units"] / conv if r["break_even_units"] and conv > 0 else None
    else:
        r["break_even_units"], r["break_even_requests"] = None, None

    comp = inp.get("company") or {}
    ebit, revenue = opt(comp, "ebit", case), opt(comp, "revenue", case)
    if ebit and r["value"] > 0.05 * ebit:
        flags.append("This case is above 5% of EBIT. About 6% of companies report AI adding that much (McKinsey, 2026).")
    elif not ebit and revenue and r["value"] > 0.01 * revenue:
        flags.append("This case is above 1% of revenue. About 6% of companies report AI adding 5% of EBIT (McKinsey, 2026).")
    if spend is not None and r["one_off"] is None and r["net"] > 0 and spend / r["net"] * 12 < 6:
        flags.append("Payback this short needs checking: under six months. Check the biggest guess first.")
    if r["one_off"] is not None and r["net"] > 0 and r["one_off"] / r["net"] * 12 < 6:
        flags.append("Payback this short needs checking: under six months against the rough cost. Check the biggest guess first.")
    r["flags"] = flags
    return r


def pair(lo_v, hi_v, fmt):
    a, b = fmt(lo_v), fmt(hi_v)
    return a if a == b else f"{a} to {b}"


def count(x):
    if x is None:
        return "n/a"
    return f"{x:.1f}" if x < 10 else f"{x:.0f}"


def main(path):
    inp = json.load(open(path))
    cur = inp.get("currency", "EUR")
    lo, hi = compute(inp, "low"), compute(inp, "high")
    m = lambda v, mode="nearest": f"{cur} {num(v, mode)}"
    use = inp.get("put_to_use") or {}
    unit = use.get("unit_name", "units")
    won = use.get("won_unit_name", "won units")
    has_costs = bool(inp.get("costs"))
    print(f"# Value case: {inp.get('workflow', 'workflow')}\n")
    print("| Item | Low | High |")
    print("| --- | --- | --- |")
    print(f"| Time back, hours a year | {num(lo['freed'])} | {num(hi['freed'])} |")
    print(f"| Time back, hours a week, at 46 weeks | {num(lo['freed'] / 46)} | {num(hi['freed'] / 46)} |")
    if use:
        print(f"| Capacity put to use: {pair(lo['units'], hi['units'], num)} extra {unit} | {m(lo['lever_use'])} | {m(hi['lever_use'])} |")
    if lo["lever_fte"] or hi["lever_fte"]:
        print(f"| FTE savings | {m(lo['lever_fte'])} | {m(hi['lever_fte'])} |")
    for (name, a), (_, b2) in zip(lo["impact"], hi["impact"]):
        print(f"| Business impact: {name} | {m(a)} | {m(b2)} |")
    for (name, a, be), (_, b2, _) in zip(lo["creation"], hi["creation"]):
        if a == 0 and b2 == 0 and be:
            print(f"| Value creation: {name} | not sized, {be} | not sized, {be} |")
        else:
            print(f"| Value creation: {name} | {m(a)} | {m(b2)} |")
    label = "Value a year" if has_costs else "Value a year, before costs"
    print(f"| {label} | {m(lo['value'])} | {m(hi['value'])} |")
    if has_costs:
        print(f"| Yearly running cost | {m(lo['yearly_cost'])} | {m(hi['yearly_cost'])} |")
        print(f"| Net value a year | {m(lo['net'])} | {m(hi['net'])} |")
        print(f"| Payback on the one-off cost | {months(lo['one_off'], lo['net'])} | {months(hi['one_off'], hi['net'])} |")
    print(f"| Year-one spending ceiling | {m(lo['net'], 'down')} | {m(hi['net'], 'down')} |")
    npv_label = "One-off spend at which NPV is zero" + ("" if has_costs else ", before running costs")
    print(f"| {npv_label} ({lo['years']} years, {lo['rate']:.0%}) | {m(lo['npv_ceiling'], 'down')} | {m(hi['npv_ceiling'], 'down')} |")
    if lo["spend"] is not None:
        s_lo, s_hi = m(lo["spend"]), m(hi["spend"])
        s = s_lo if s_lo == s_hi else f"{s_lo} (low) and {s_hi} (high)"
        if lo["break_even_units"]:
            print(f"| Break-even at {s}: extra {won} | {count(lo['break_even_units'])} | {count(hi['break_even_units'])} |")
        if lo["break_even_requests"]:
            print(f"| Break-even at {s}: extra {unit} handled | {count(lo['break_even_requests'])} | {count(hi['break_even_requests'])} |")
        print(f"| Payback at {s} | {months(lo['spend'], lo['net'])} | {months(hi['spend'], hi['net'])} |")
    print("\nThe low case pairs low values with high costs. The high case pairs high values with low costs.")
    for case, r in (("low", lo), ("high", hi)):
        if r["unassigned"] > 1:
            print(f"In the {case} case, {num(r['unassigned'])} freed hours a year have no destination yet. Decide where they go, or they create no value.")
    seen = []
    for f in lo["flags"] + hi["flags"]:
        if f not in seen:
            seen.append(f)
    for f in seen:
        cases = [c for c, r in (("low", lo), ("high", hi)) if f in r["flags"]]
        tag = "both cases" if len(cases) == 2 else f"{cases[0]} case"
        print(f"Check, {tag}: {f}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
