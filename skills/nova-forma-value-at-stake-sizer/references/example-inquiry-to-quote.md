# Example run: inquiry to quote

Figures are illustrative. The inputs sit in `example-inputs.json`. To keep it short, the example leaves out the tracker and the brief so far, which every step message still opens with.

## Moment 1: where the value lands

The scope card says small requests are turned away today, so freed hours would be worth more quotes.

[Visual: four cards. Freed time put to more quotes ● likely, "small requests are declined today". Better results ● likely, "every quote checked against the discount rules". Savings ◐ possible, "only as people leave". A new offer ○ unlikely, "same-day quotes, not sized".]

**Cards**

- Header "Team full". "Does some work go unanswered, or get a rushed answer, because the team is full?" Options: "Yes, some work is turned away or rushed (Recommended)" with "Your notes mention small requests declined.", "No, we keep up with all of it".
- Header "Freed hours". "If this work took less time, where would the hours go? Pick one or more." Options: "More quotes (Recommended)", "Fewer hires as people leave", "More time on quality".
- Header "Priority". "Which result matters most to the business?" Options: "Better price or margin (Recommended)" with "Discounts drift outside the rules today.", "Win more work", "Faster turnaround", "Lower cost or risk".

The user answers: yes, small ones are turned away; more quotes, and fewer hires as people leave; price first.

## Moment 2: the numbers

| # | Input | Value | Source |
| --- | --- | --- | --- |
| 1 | Team on quoting: hours a week, people, quotes sent a week | ? | ? needed |
| 2 | Share of hours AI could take over | 30% to 60% | ≈ hypothesis, from the kind of work |
| 3 | Requests declined a year | ? | ? needed |
| 4 | Win rate, order value, margin on small requests | ? | ? needed |
| 5 | Freed hours to quotes or fewer hires | 60% quotes, 40% fewer hires | ≈ hypothesis, from your answer |
| 6 | Discount leakage avoided, and a win rate gain on today's quotes from faster turnaround | EUR 200k to 400k, and EUR 0 to 150k | ≈ hypothesis, leakage from the pricing log sample |
| 7 | Build and yearly cost | EUR 250k to 400k, EUR 60k to 100k | ✓ from you, IT's first estimate in your Drive |
| 8 | Revenue a year | EUR 150M | ✓ from you, the annual report in your Drive |

Rows 3 and 6 move the case most: declined requests cap the extra quotes, and leakage carries half the low case.

**Cards, round 1**

- Header "Hours". "Roughly how many hours a week does the team spend on quotes?" Options: "Under 100", "100 to 200", "200 to 300 (Recommended)", "More than 300".
- Header "Declined". "Roughly how many quote requests do you decline a year?" Options: "Under 500", "500 to 1,000", "1,000 to 2,000 (Recommended)", "More than 2,000".
- Header "Win rate". "What is your usual win rate on small requests?" Options: "Under 15%", "15% to 25% (Recommended)", "25% to 40%", "Over 40%".
- Header "Order size". "What is a typical small order worth?" Options: "Under EUR 2,000", "EUR 2,000 to 5,000 (Recommended)", "EUR 5,000 to 10,000", "Over EUR 10,000".

**Cards, round 2**

- Header "Margin". "What margin do you keep on a small order, after delivery costs?" Options: "Under 15%", "15% to 25% (Recommended)", "25% to 35%", "Over 35%".
- Header "Team". "How many people work on quotes, counted as full-time?" Options: "Under 5", "5 to 10 (Recommended)", "10 to 20", "More than 20".
- Header "Quotes". "Roughly how many quotes does the team send a week today?" Options: "Under 50", "50 to 100", "100 to 200 (Recommended)", "More than 200".
- Header "The rest". "Shall I use my hypotheses for the rest?" Options: "Yes, use them and mark them (Recommended)", "No, I'll correct a row".

The user types 250 hours a week and 1,200 declined requests, picks 15% to 25%, types EUR 5,000, a 25% margin, a team of 8 and about 120 quotes a week, and keeps the hypotheses. An extra quote takes about 2 hours: 250 hours a week over about 120 quotes. At 46 working weeks, that is about 11,500 hours and 5,500 quotes a year.

## Moment 3: the result

Worth about EUR 420k to 1M a year, before costs. Better prices and the small requests you now decline lead. Discount leakage moves the range most.

[Visual: floating bars from low to high. Better results EUR 200k to 550k in the accent; freed time put to more quotes EUR 190k to 380k; savings EUR 30k to 97k; a new offer not sized; total EUR 420k to 1M.]

| Source of value | Low | High | Basis |
| --- | --- | --- | --- |
| Better results | EUR 200k | EUR 550k | Discount leakage avoided, and a win rate gain from faster turnaround |
| Freed time put to more quotes | EUR 190k | EUR 380k | Small requests quoted, capped at 1,200 declined a year |
| Savings | EUR 30k | EUR 97k | Fewer hires as people leave |
| A new offer | Not sized | Not sized | Same-day quotes as part of the offer |

**Reality check:** the low case is under 0.3% of your EUR 150M revenue. At EUR 250k to 400k to build and EUR 60k to 100k a year, the net value is EUR 320k to 960k a year and payback runs 3 to 15 months. The 3 months needs checking, starting with the leakage figure. Worth it, if the leakage figure holds.

How we use this: the range says whether a redesign is worth a week of your team's time, and which number to firm up first.

Where I need your input:

- Review the range and share feedback.
- Check last quarter's discounts against the rules: the leakage figure carries half the low case.
- Count last year's declined requests.
- Decide where 1,700 freed hours go in the high case.

Sources: your note and Google Drive.

**Next card**

- Header "Next step". "Shall I put the four results on one page for the redesign week?"
- Options: "Yes, make the one-pager (Recommended)", "Adjust the numbers first".
