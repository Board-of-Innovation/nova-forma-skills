# Levers, formulas and the calculator's inputs

The user never hears the word lever. Name the four as sources of value: savings (lever 1), freed time put to use (lever 2), better results (lever 3) and a new offer (lever 4).

## Lever 1: FTE savings

FTE released × loaded cost per FTE × realization share.

The realization share is the part of the released FTE that turns into cash within a year. Name the mechanism, such as natural attrition, a hiring freeze, fewer contractors or less overtime. Without a mechanism the realization share is zero, and the hours meant for savings have no destination. A low case of 50% and a high case of 80% is a reasonable start when a mechanism exists.

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

When the user sends freed hours to quality, put their share under `quality` in the capacity split and value them here only, with the Quality row. Never count them again as hours put to use or as savings.

## Lever 4: value creation

New units or customers × price × contribution margin, for an offer the redesign makes possible. When the numbers do not exist yet, describe the opportunity and the decision it needs, and set both cases to zero rather than invent them.

## Costs

- One-off: build and integration, data preparation, change and training.
- Yearly: licenses and usage, hosting, monitoring and maintenance, and the time people spend overseeing the AI.

## Checks on the size of the case

Run all four, and name any failure in plain words. The script runs each one when it has the inputs that check needs.

- Extra units above 25% of today's volume: cap at 25%, unless the user confirms both the demand and the capacity to deliver it.
- Freed hours above the hours the team spends on the workflow, or above what the whole team works in a year: cap at the lower of the two. When the workflow takes more hours than the team works, check both numbers.
- A case above 1% of revenue, or above 5% of EBIT (operating profit): keep it, say so, and name the input that drives it. Test revenue and EBIT each on their own, and skip the EBIT test when EBIT is 0 or less. To show how rare 5% of EBIT is, use the McKinsey finding on EBIT in `evidence.md`.
- Payback under six months: say it needs checking, and check the biggest guess first.

## Pitfalls

- Counting the same hours in levers 1 and 2.
- Valuing freed hours at salary without a decision behind them.
- Using revenue instead of contribution margin.
- Ignoring the ramp: the first year rarely reaches full value, so the low case should reflect partial adoption.
- Forgetting the yearly running costs.

## The calculator's inputs

`scripts/value_case.py` reads one JSON file. A number holds either a single value or a pair such as `{"low": 0.3, "high": 0.6}`. Shares run from 0 to 1, so 30% is 0.3. When a pair has its low above its high, the script swaps the two and says so.

```json
{
  "workflow": "Inquiry to quote",
  "currency": "EUR",
  "baseline": {"hours_per_year": 11300, "working_hours_per_fte": 1700, "loaded_cost_per_fte": 75000,
               "team_fte": 8},
  "addressable_share": {"low": 0.3, "high": 0.6},
  "capacity_split": {"fte_savings": 0.4, "put_to_use": 0.6, "quality": 0},
  "fte_savings": {"realization": {"low": 0.5, "high": 0.8}},
  "put_to_use": {"unit_name": "quotes", "hours_per_unit": 2, "volume_today": 5500, "demand_cap_units": 1200,
                 "conversion": {"low": 0.15, "high": 0.25}, "value_per_unit": 5000, "contribution_margin": 0.25},
  "impact_levers": [{"name": "Price realization", "low": 200000, "high": 400000}],
  "value_creation": [{"name": "A new offer", "low": 0, "high": 0}],
  "costs": {"one_off": {"low": 250000, "high": 400000}, "yearly": {"low": 60000, "high": 100000}},
  "company": {"revenue": 150000000}
}
```

Every field the script reads:

| Field | What it holds | When it is needed |
| --- | --- | --- |
| `workflow`, `currency` | The workflow's name, and the currency code. The currency defaults to EUR. | Optional |
| `baseline.hours_per_year` | Hours the team spends on the workflow a year: hours a week × 46. | Always, unless freed hours are given |
| `baseline.working_hours_per_fte` | Working hours of one full-time person a year. Defaults to 1,700. | Optional |
| `baseline.loaded_cost_per_fte` | The yearly cost of one full-time person, salary and overheads. | For savings |
| `baseline.team_fte` | The people who do the work, counted as full-time. | For the team check |
| `baseline.freed_hours_per_year` | Freed hours a year, when known directly. Replaces hours × share. | Optional |
| `addressable_share` | The share of hours AI could take over, from `addressable-share.md`. | Always, unless freed hours are given |
| `capacity_split.put_to_use`, `.fte_savings`, `.quality` | Where freed hours go, as shares that add up to 1 or less. The rest has no destination. A pair here is kept as given, because a split has no low or high side. | When the input has `put_to_use` or `fte_savings` |
| `fte_savings.realization` | The share of released FTE that turns into cash within a year. Missing or 0 means no mechanism. | For savings |
| `put_to_use.unit_name` | One unit of work, such as "quotes". The script adds "extra" itself. | Optional |
| `put_to_use.hours_per_unit` | Hours one extra unit takes. Above 0. | For freed time put to use |
| `put_to_use.volume_today` | Units the team handles a year today. | For the 25% check |
| `put_to_use.demand_cap_units` | Real demand for extra units a year, such as requests declined today. | For the demand cap |
| `put_to_use.demand_and_delivery_confirmed` | `true` once the user confirms both the demand and the capacity to deliver it. Lifts the 25% cap. Defaults to `false`. | Optional |
| `put_to_use.conversion` | The share of extra units that turn into a sale. | For freed time put to use |
| `put_to_use.value_per_unit` | Revenue from one won unit. | For freed time put to use |
| `put_to_use.contribution_margin` | The share of that revenue left after delivery costs. | For freed time put to use |
| `put_to_use.won_unit_name` | One won unit, such as "orders", for the break-even rows. | Optional |
| `impact_levers` | Better results: a list of entries, each with a `name` and a yearly `value`, or a `low` and a `high`. | Optional |
| `value_creation` | A new offer: entries like those above, plus an optional `break_even` text to show when both cases are 0. | Optional |
| `costs.one_off`, `costs.yearly` | The build cost, and the running cost a year. | For net value and payback |
| `reference_spend` | A one-off amount to test before costs are known, such as a first quote. Adds break-even and payback rows. | Optional |
| `finance.discount_rate`, `finance.years` | For the one-off spend at which the case breaks even over the years. Defaults to 0.08 and 5. | Optional |
| `company.revenue`, `company.ebit` | Revenue and EBIT (operating profit) a year. Each runs its own size check. | For the size check, at least one |

Work out levers 3 and 4 with the formulas above before entering their totals. The low case pairs low values with high costs, and the high case pairs high values with low costs. For costs, `reference_spend`, `hours_per_unit`, `working_hours_per_fte` and `discount_rate`, a higher figure lowers the value, so the low case takes the higher one. The script also flags freed hours that have no destination.

A missing field the case needs, a 0 where the script divides, a share above 1, or text where a number belongs stops the script with one line that starts "Error:". Fix that input and run the script again.
