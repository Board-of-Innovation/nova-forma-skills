#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Value case for redesigning a workflow, as a low and a high case.

Usage: python3 value_case.py inputs.json

Runs on Python 3.9 or later, the oldest Python 3 a Mac still ships.

Any number in the input may be a single value or a pair such as
{"low": 0.3, "high": 0.6}. Values are per year and before build and
running costs, unless costs are given. references/levers.md lists every
field and the checks this script runs.
"""

import json
import math
import sys

LOW, HIGH = 0, 1

# Every field the script reads, by section, so a misspelled field stops the script
# instead of quietly taking its default.
FIELDS = {
    "": {
        "workflow",
        "currency",
        "baseline",
        "addressable_share",
        "capacity_split",
        "fte_savings",
        "put_to_use",
        "impact_levers",
        "value_creation",
        "costs",
        "reference_spend",
        "finance",
        "company",
    },
    "baseline": {
        "hours_per_year",
        "working_hours_per_fte",
        "loaded_cost_per_fte",
        "team_fte",
        "freed_hours_per_year",
    },
    "capacity_split": {"put_to_use", "fte_savings", "quality"},
    "fte_savings": {"realization"},
    "put_to_use": {
        "unit_name",
        "won_unit_name",
        "hours_per_unit",
        "volume_today",
        "demand_cap_units",
        "demand_and_delivery_confirmed",
        "conversion",
        "value_per_unit",
        "contribution_margin",
    },
    "costs": {"one_off", "yearly"},
    "finance": {"discount_rate", "years"},
    "company": {"revenue", "ebit"},
}
ENTRY_FIELDS = {"name", "value", "low", "high", "break_even"}


class InputError(Exception):
    """A problem in the input file, reported to the user as one plain line."""


class Reader:
    """Reads every field once, checks it, and returns it as a (low case, high case) pair."""

    def __init__(self):
        self.swapped = []

    def number(self, value, path, share=False, positive=False, negative_ok=False):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InputError(f"{path} must be a number, not {json.dumps(value)}.")
        x = float(value)
        if not math.isfinite(x):
            raise InputError(f"{path} must be a finite number.")
        if x < 0 and not negative_ok:
            raise InputError(f"{path} must be 0 or more, not {x:g}.")
        if positive and x <= 0:
            raise InputError(f"{path} must be above 0.")
        if share and x > 1:
            raise InputError(f"{path} is a share, so it must be 0 to 1, such as 0.3 for 30%.")
        return x

    def field(self, section, path, key, default=None, **options):
        """Return the pair for section[key], or the default pair when it is missing."""
        value = None if section is None else section.get(key)
        if value is None:
            return None if default is None else (float(default), float(default))
        return self.pair(value, f"{path}.{key}" if path else key, **options)

    def pair(self, value, path, inverse=False, ordered=True, **checks):
        """Return a number or a low/high pair as (low case, high case).

        With inverse, the low case takes the higher figure, as for costs.
        Without ordered, a pair is kept as given: a split of hours has no low or high side.
        """
        if isinstance(value, dict):
            if not value or set(value) - {"low", "high"}:
                raise InputError(
                    f"{path} must be a number or a pair with low and high, not {json.dumps(value)}."
                )
            low = self.number(value.get("low", value.get("high")), f"{path}.low", **checks)
            high = self.number(value.get("high", value.get("low")), f"{path}.high", **checks)
            if ordered and low > high:
                self.swapped.append(path)
                low, high = high, low
        else:
            low = high = self.number(value, path, **checks)
        return (high, low) if inverse else (low, high)


def known(value, path, allowed):
    """Stop on a field the script does not read, such as a misspelled one."""
    unknown = sorted(set(value) - allowed)
    if unknown:
        where = path or "The input"
        raise InputError(
            f"{where} has an unknown field {unknown[0]}. Use one of: {', '.join(sorted(allowed))}."
        )


def section(data, key):
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, dict):
        raise InputError(f"{key} must be an object with named fields, as in levers.md.")
    known(value, key, FIELDS[key])
    return value


def text(data, key, default):
    value = data.get(key, default)
    if not isinstance(value, str):
        raise InputError(f"{key} must be text, not {json.dumps(value)}.")
    return value


def entries(rd, data, key):
    """Read impact_levers or value_creation: a name and a number or a low/high pair each."""
    items = data.get(key) or []
    if not isinstance(items, list):
        raise InputError(f"{key} must be a list of entries, each with a name and a value.")
    out = []
    for n, item in enumerate(items, start=1):
        path = f"{key}[{n}]"
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            raise InputError(f"{path} needs a name, and a value or a low and a high.")
        known(item, path, ENTRY_FIELDS)
        if "value" in item:
            spec = item["value"]
        else:
            spec = {k: item[k] for k in ("low", "high") if k in item}
            if not spec:
                raise InputError(f"{path} ({item['name']}) needs a value, or a low and a high.")
        out.append((item["name"], rd.pair(spec, path), str(item.get("break_even", ""))))
    return out


def read_inputs(data):
    """Check the whole input up front and return every number as a pair."""
    if not isinstance(data, dict):
        raise InputError("The input must be a JSON object, like the sample in levers.md.")
    known(data, "", FIELDS[""])
    rd = Reader()
    p = {"workflow": text(data, "workflow", "workflow"), "currency": text(data, "currency", "EUR")}

    base = section(data, "baseline")
    if base is None:
        raise InputError("baseline is missing: the hours the team spends on the workflow a year.")
    p["hours"] = rd.field(base, "baseline", "hours_per_year")
    p["freed_given"] = rd.field(base, "baseline", "freed_hours_per_year")
    if p["hours"] is None and p["freed_given"] is None:
        raise InputError(
            "baseline.hours_per_year is missing: the hours spent on the workflow a year."
        )
    p["hpf"] = rd.field(
        base, "baseline", "working_hours_per_fte", default=1700, inverse=True, positive=True
    )
    p["cost"] = rd.field(base, "baseline", "loaded_cost_per_fte")
    p["team"] = rd.field(base, "baseline", "team_fte", positive=True)
    p["share"] = rd.field(data, "", "addressable_share", share=True)
    if p["freed_given"] is None and p["share"] is None:
        raise InputError("addressable_share is missing: the share of hours AI could take over.")

    split = section(data, "capacity_split")
    use = section(data, "put_to_use")
    fte = section(data, "fte_savings")
    if split is None and (use or fte):
        raise InputError(
            "capacity_split is missing: the share of freed hours for put_to_use, "
            "fte_savings and quality."
        )
    for key in ("put_to_use", "fte_savings", "quality"):
        p[f"s_{key}"] = rd.field(split, "capacity_split", key, default=0, ordered=False, share=True)
    for k, case in ((LOW, "low"), (HIGH, "high")):
        total = p["s_put_to_use"][k] + p["s_fte_savings"][k] + p["s_quality"][k]
        if total > 1.0001:
            raise InputError(
                f"capacity_split adds up to {total:.0%} in the {case} case: "
                "each freed hour can go to one place only."
            )
    if max(p["s_put_to_use"]) > 0 and use is None:
        raise InputError("capacity_split.put_to_use is above 0, but put_to_use is missing.")

    p["use"] = None
    if use is not None:
        u = {
            "unit": text(use, "unit_name", "units"),
            "won": text(use, "won_unit_name", "won units"),
        }
        for key in ("hours_per_unit", "conversion", "value_per_unit", "contribution_margin"):
            u[key] = rd.field(
                use,
                "put_to_use",
                key,
                inverse=key == "hours_per_unit",
                positive=key == "hours_per_unit",
                share=key in ("conversion", "contribution_margin"),
            )
            if u[key] is None:
                raise InputError(f"put_to_use.{key} is missing.")
        u["cap"] = rd.field(use, "put_to_use", "demand_cap_units")
        u["volume"] = rd.field(use, "put_to_use", "volume_today")
        confirmed = use.get("demand_and_delivery_confirmed", False)
        if not isinstance(confirmed, bool):
            raise InputError("put_to_use.demand_and_delivery_confirmed must be true or false.")
        u["confirmed"] = confirmed
        p["use"] = u

    p["realization"] = rd.field(fte, "fte_savings", "realization", default=0, share=True)
    if max(p["s_fte_savings"]) > 0 and max(p["realization"]) > 0 and p["cost"] is None:
        raise InputError(
            "baseline.loaded_cost_per_fte is missing: savings need the cost of one FTE."
        )

    p["impact"] = entries(rd, data, "impact_levers")
    p["creation"] = entries(rd, data, "value_creation")

    costs = section(data, "costs")
    p["has_costs"] = bool(costs)
    p["yearly_cost"] = rd.field(costs, "costs", "yearly", default=0, inverse=True)
    p["one_off"] = rd.field(costs, "costs", "one_off", inverse=True)
    p["spend"] = rd.field(data, "", "reference_spend", inverse=True)

    fin = section(data, "finance")
    p["rate"] = rd.field(fin, "finance", "discount_rate", default=0.08, inverse=True, share=True)
    p["years"] = rd.field(fin, "finance", "years", default=5, positive=True)

    comp = section(data, "company")
    p["revenue"] = rd.field(comp, "company", "revenue")
    p["ebit"] = rd.field(comp, "company", "ebit", negative_ok=True)
    p["swapped"] = rd.swapped
    return p


def sig(x, mode="nearest"):
    """Round to two significant figures, halves up, or down when mode is 'down'."""
    if x == 0:
        return 0.0
    a = abs(x)
    q = 10 ** (math.floor(math.log10(a)) - 1)
    steps = a / q
    a2 = (math.floor(steps + 1e-9) if mode == "down" else math.floor(steps + 0.5)) * q
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


def pct(x):
    return f"{sig(x * 100):g}%"


def months(spend, yearly):
    if spend is None:
        return "n/a"
    if yearly <= 0:
        return "no payback"
    m = spend / yearly * 12
    if m < 1:
        return "under 1 month"
    return "1 month" if round(m) == 1 else f"{m:.0f} months"


def lowest_positive(pair):
    """The lowest figure above 0 in a pair, so a range of revenue or EBIT is tested at its
    weaker side in both cases."""
    if pair is None:
        return None
    above = [x for x in pair if x > 0]
    return min(above) if above else None


def compute(p, k):
    """Work out one case: k is LOW or HIGH."""

    def at(pair):
        return None if pair is None else pair[k]

    flags = []
    hours, hpf, team = at(p["hours"]), at(p["hpf"]), at(p["team"])
    freed = at(p["freed_given"])
    if freed is None:
        freed = hours * at(p["share"])

    limits = []
    if hours is not None:
        limits.append((hours, f"the {num(hours)} hours the team spends on this workflow"))
    if team is not None:
        capacity = team * hpf
        limits.append((capacity, f"the {num(capacity)} hours a team of {team:g} FTE works a year"))
        if hours is not None and hours > capacity * 1.0001:
            flags.append(
                f"The {num(hours)} hours on this workflow are more than a team of {team:g} FTE "
                "works in a year. Check both numbers."
            )
    if limits:
        limit, label = min(limits, key=lambda item: item[0])
        if freed > limit:
            flags.append(f"Freed time is capped at {label}.")
            freed = limit
    r = {"freed": freed, "fte": freed / hpf}

    s_use, s_fte, s_quality = at(p["s_put_to_use"]), at(p["s_fte_savings"]), at(p["s_quality"])
    unassigned = freed * max(0.0, 1.0 - s_use - s_fte - s_quality)

    use = p["use"]
    r["units"], r["lever_use"] = 0.0, 0.0
    if use and s_use > 0:
        hpu = at(use["hours_per_unit"])
        raw = freed * s_use / hpu
        used = raw
        cap, vol = at(use["cap"]), at(use["volume"])
        if cap is not None and used > cap:
            used = cap
            flags.append(f"Extra units are capped at the demand you named: {num(cap)}.")
        if vol is not None and not use["confirmed"] and used > 0.25 * vol:
            used = 0.25 * vol
            flags.append(
                f"Extra units are capped at 25% of today's volume, {num(used)}, "
                "until you confirm the demand and the capacity to deliver it."
            )
        unassigned += (raw - used) * hpu
        r["units"] = used
        r["lever_use"] = (
            used
            * at(use["conversion"])
            * at(use["value_per_unit"])
            * at(use["contribution_margin"])
        )

    realization = at(p["realization"])
    if s_fte > 0 and realization == 0:
        unassigned += freed * s_fte
        flags.append(
            "Savings have no way to turn into cash yet, such as fewer hires as people leave, "
            "so those freed hours count as having no destination."
        )
    cost = at(p["cost"]) or 0.0
    r["lever_fte"] = (freed * s_fte / hpf) * cost * realization

    r["impact"] = [(name, at(pair)) for name, pair, _ in p["impact"]]
    r["creation"] = [(name, at(pair), be) for name, pair, be in p["creation"]]
    if s_quality > 0 and not r["impact"]:
        flags.append(
            "Freed hours go to quality, but no better result is sized. "
            "Size the errors avoided, or those hours create no value."
        )
    r["lever_impact"] = sum(v for _, v in r["impact"])
    r["lever_creation"] = sum(v for _, v, _ in r["creation"])
    r["value"] = r["lever_use"] + r["lever_fte"] + r["lever_impact"] + r["lever_creation"]
    r["unassigned"] = unassigned

    r["yearly_cost"] = at(p["yearly_cost"])
    r["one_off"] = at(p["one_off"])
    r["net"] = r["value"] - r["yearly_cost"]

    rate, years = at(p["rate"]), at(p["years"])
    r["annuity"] = years if rate == 0 else (1 - (1 + rate) ** -years) / rate
    r["npv_ceiling"] = r["net"] * r["annuity"]
    r["rate"], r["years"] = rate, years

    spend = at(p["spend"])
    r["spend"] = spend
    r["break_even_units"], r["break_even_requests"] = None, None
    if spend is not None and use:
        per_unit = at(use["value_per_unit"]) * at(use["contribution_margin"])
        r["break_even_units"] = spend / per_unit if per_unit > 0 else None
        conv = at(use["conversion"])
        if r["break_even_units"] and conv > 0:
            r["break_even_requests"] = r["break_even_units"] / conv

    sources = [("capacity put to use", r["lever_use"]), ("FTE savings", r["lever_fte"])]
    sources += [(f"business impact: {name}", v) for name, v in r["impact"]]
    sources += [(f"value creation: {name}", v) for name, v, _ in r["creation"]]
    biggest = max(sources, key=lambda item: item[1])[0]
    revenue, ebit = lowest_positive(p["revenue"]), lowest_positive(p["ebit"])
    r["share_of_revenue"] = r["value"] / revenue if revenue else None
    r["share_of_ebit"] = r["value"] / ebit if ebit else None
    if r["share_of_revenue"] is not None and r["share_of_revenue"] > 0.01:
        flags.append(
            "This case is above 1% of revenue. Keep it, say so, and check the biggest "
            f"source first ({biggest})."
        )
    if r["share_of_ebit"] is not None and r["share_of_ebit"] > 0.05:
        flags.append(
            "This case is above 5% of EBIT, which few companies get from AI: see the McKinsey "
            "finding on EBIT in references/evidence.md. Check the biggest source first "
            f"({biggest})."
        )
    if spend is not None and r["one_off"] is None and r["net"] > 0 and spend / r["net"] * 12 < 6:
        flags.append(
            "Payback this short needs checking: under six months. Check the biggest guess first."
        )
    if r["one_off"] is not None and r["net"] > 0 and r["one_off"] / r["net"] * 12 < 6:
        flags.append(
            "Payback this short needs checking: under six months against the rough cost. "
            "Check the biggest guess first."
        )
    if r["net"] <= 0:
        flags.append(
            "The yearly running cost is at or above the value a year, so the case does not pay back."
            if r["yearly_cost"] > 0
            else "The case has no value a year yet, so there is nothing to pay back."
        )
    r["flags"] = flags
    return r


def pair(lo_v, hi_v, fmt):
    a, b = fmt(lo_v), fmt(hi_v)
    return a if a == b else f"{a} to {b}"


def per_case(a, b):
    return a if a == b else f"{a} (low) and {b} (high)"


def count(x):
    if x is None:
        return "n/a"
    return f"{x:.1f}" if x < 10 else f"{x:.0f}"


def report(p):
    cur = p["currency"]
    lo, hi = compute(p, LOW), compute(p, HIGH)

    def m(v, mode="nearest"):
        return f"{cur} {num(v, mode)}"

    def ceiling(v):
        """A spending ceiling, or "none" when the case loses money every year."""
        return m(v, "down") if v > 0 else "none"

    use = p["use"] or {}
    unit = use.get("unit", "units")
    won = use.get("won", "won units")
    has_costs = p["has_costs"]
    print(f"# Value case: {p['workflow']}\n")
    print("| Item | Low | High |")
    print("| --- | --- | --- |")
    print(f"| Time back, hours a year | {num(lo['freed'])} | {num(hi['freed'])} |")
    print(
        f"| Time back, hours a week, at 46 weeks | {num(lo['freed'] / 46)} "
        f"| {num(hi['freed'] / 46)} |"
    )
    if use:
        units = pair(lo["units"], hi["units"], num)
        print(
            f"| Capacity put to use: {units} extra {unit} | {m(lo['lever_use'])} "
            f"| {m(hi['lever_use'])} |"
        )
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
    if lo["share_of_revenue"] is not None:
        print(
            f"| Value as a share of revenue | {pct(lo['share_of_revenue'])} "
            f"| {pct(hi['share_of_revenue'])} |"
        )
    if lo["share_of_ebit"] is not None:
        print(
            f"| Value as a share of EBIT | {pct(lo['share_of_ebit'])} "
            f"| {pct(hi['share_of_ebit'])} |"
        )
    if has_costs:
        print(f"| Yearly running cost | {m(lo['yearly_cost'])} | {m(hi['yearly_cost'])} |")
        print(f"| Net value a year | {m(lo['net'])} | {m(hi['net'])} |")
        print(
            f"| Payback on the one-off cost | {months(lo['one_off'], lo['net'])} "
            f"| {months(hi['one_off'], hi['net'])} |"
        )
    before = "" if has_costs else ", before running costs"
    print(f"| Year-one spending ceiling{before} | {ceiling(lo['net'])} | {ceiling(hi['net'])} |")
    years = per_case(f"{lo['years']:g} years", f"{hi['years']:g} years")
    rate = per_case(f"{lo['rate']:.0%}", f"{hi['rate']:.0%}")
    print(
        f"| One-off spend at which NPV is zero{before} ({years}, {rate}) "
        f"| {ceiling(lo['npv_ceiling'])} | {ceiling(hi['npv_ceiling'])} |"
    )
    if lo["spend"] is not None:
        s = per_case(m(lo["spend"]), m(hi["spend"]))
        if lo["break_even_units"]:
            print(
                f"| Break-even at {s}: extra {won} | {count(lo['break_even_units'])} "
                f"| {count(hi['break_even_units'])} |"
            )
        if lo["break_even_requests"]:
            print(
                f"| Break-even at {s}: extra {unit} handled | {count(lo['break_even_requests'])} "
                f"| {count(hi['break_even_requests'])} |"
            )
        print(
            f"| Payback at {s} | {months(lo['spend'], lo['net'])} | {months(hi['spend'], hi['net'])} |"
        )
    print(
        "\nThe low case pairs low values with high costs. The high case pairs high values "
        "with low costs."
    )
    for case, r in (("low", lo), ("high", hi)):
        if r["unassigned"] > 1:
            print(
                f"In the {case} case, {num(r['unassigned'])} freed hours a year have no "
                "destination yet. Decide where they go, or they create no value."
            )
    for path in p["swapped"]:
        print(f"Check: {path} had its low above its high, so the two were swapped.")
    seen = []
    for f in lo["flags"] + hi["flags"]:
        if f not in seen:
            seen.append(f)
    for f in seen:
        cases = [c for c, r in (("low", lo), ("high", hi)) if f in r["flags"]]
        tag = "both cases" if len(cases) == 2 else f"{cases[0]} case"
        print(f"Check, {tag}: {f}")
    for item in not_checked(p):
        print(f"Not checked: {item}.")


def not_checked(p):
    """Name each size check the input leaves out, so a missing field never passes silently."""

    def given(pair):
        return pair is not None and max(pair) > 0

    missing = []
    use = p["use"]
    if use and max(p["s_put_to_use"]) > 0:
        if use["cap"] is None:
            missing.append(
                "extra units against real demand, such as requests declined today "
                "(needs put_to_use.demand_cap_units)"
            )
        if use["volume"] is None and not use["confirmed"]:
            missing.append(
                "extra units against 25% of today's volume (needs put_to_use.volume_today)"
            )
    if p["team"] is None:
        missing.append("freed hours against what the team works a year (needs baseline.team_fte)")
    if not given(p["revenue"]) and not given(p["ebit"]):
        missing.append(
            "the case against the company's size (needs company.revenue, or company.ebit above 0)"
        )
    if p["one_off"] is None and p["spend"] is None:
        missing.append(
            "payback under six months (needs costs.one_off or reference_spend; without a cost, "
            "report the year-one spending ceiling instead)"
        )
    return missing


def main(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except OSError as e:
        sys.exit(f"Error: cannot read {path}: {e.strerror}.")
    except json.JSONDecodeError as e:
        sys.exit(f"Error: {path} is not valid JSON: {e.msg}, line {e.lineno}.")
    try:
        p = read_inputs(data)
    except InputError as e:
        sys.exit(f"Error: {e}")
    report(p)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
