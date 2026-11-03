# Levers, formulas and the calculator's inputs

The user never hears the word lever. Name the four as sources of value: savings (lever 1), freed time put to use (lever 2), better results (lever 3) and a new offer (lever 4).

## Lever 1: FTE savings

FTE released × loaded cost per FTE × realization share.

The realization share is the part of the released FTE that turns into cash within a year. Name the mechanism, such as natural attrition, a hiring freeze, fewer contractors or less overtime. Without a mechanism the realization share is zero. A low case of 50% and a high case of 80% is a reasonable start when a mechanism exists.

## Lever 2: capacity put to use

Extra units handled × conversion × value per unit × contribution margin.

- Extra units are freed hours divided by the hours one extra unit takes.
- Cap the extra units by real demand, such as the requests declined or answered too late today. Capacity beyond that cap creates no value.
- Use contribution margin, never revenue, because extra revenue also brings extra cost.

## Lever 3: business impact

| Impact | Formula | Typical source |
| --- | --- | --- |
| Speed | Change in win or conversion rate × volume × value per unit × contribution margin | CRM win rates by response time |
| Quality | Errors or rework avoided × cost per error | Complaints, credit notes, rework logs |
| Price realization | Revenue affected × change in realization | Discounts given against the rules |
| Working capital | Days reduced × daily value × cost of capital | Days sales outstanding, inventory days |
| Risk | Incidents avoided × cost per incident | Audit findings, penalties |

## Lever 4: value creation

New units or customers × price × contribution margin, for an offer the redesign makes possible. When the numbers do not exist yet, describe the opportunity and the decision it needs, and set both cases to zero rather than invent them.

## Costs

- One-off: build and integration, data preparation, change and training.
- Yearly: licenses and usage, hosting, monitoring and maintenance, and the time people spend overseeing the AI.

## Checks on the size of the case

Run all four, and name any failure in plain words.

- Extra units above 25% of today's volume: cap at 25%, unless the user confirms both the demand and the capacity to deliver it.
- Freed hours above the hours the team spends on the workflow: cap at the team.
- High case above 1% of revenue, or 5% of EBIT: keep it, say so, and name the input that drives it. About 6% of companies report AI adding 5% or more to EBIT (McKinsey, 2026).
- Payback under six months: say it needs checking, and check the biggest guess first.

## Pitfalls

- Counting the same hours in levers 1 and 2.
- Valuing freed hours at salary without a decision behind them.
- Using revenue instead of contribution margin.
- Ignoring the ramp: the first year rarely reaches full value, so the low case should reflect partial adoption.
- Forgetting the yearly running costs.

## The calculator's inputs

`scripts/value_case.py` reads one JSON file. A field holds either a single number or a pair such as `{"low": 0.3, "high": 0.6}`.

```json
{
  "workflow": "Name of the workflow",
  "currency": "EUR",
  "baseline": {"hours_per_year": 11300, "working_hours_per_fte": 1880, "loaded_cost_per_fte": 75000},
  "addressable_share": {"low": 0.3, "high": 0.6},
  "capacity_split": {"fte_savings": 0.4, "put_to_use": 0.6},
  "fte_savings": {"realization": {"low": 0.5, "high": 0.8}},
  "put_to_use": {"unit_name": "extra quotes", "hours_per_unit": 2, "demand_cap_units": 1200,
                 "conversion": {"low": 0.15, "high": 0.25}, "value_per_unit": 5000, "contribution_margin": 0.25},
  "impact_levers": [{"name": "Price realization", "low": 200000, "high": 400000}],
  "value_creation": [{"name": "A new offer", "low": 0, "high": 0}],
  "costs": {"one_off": {"low": 250000, "high": 400000}, "yearly": {"low": 60000, "high": 100000}}
}
```

Work out levers 3 and 4 with the formulas above before entering their totals. The low case pairs low values with high costs, and the high case pairs high values with low costs. The script also flags freed hours that have no destination.
