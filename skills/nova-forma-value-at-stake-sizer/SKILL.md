---
name: nova-forma-value-at-stake-sizer
description: Estimate what redesigning one workflow with AI is worth a year, as a low to high value range with every assumption visible, next to the rough cost and payback, then put the four Nova Forma results on one page for the redesign week. Use when someone plans to redesign or automate a specific workflow with AI and asks what it is worth, wants an ROI, payback, business case or value estimate for it, or needs to justify a pilot, even for a rough first number. Not for choosing which workflow to start with, which nova-forma-workflow-identifier does. Step 4 of the four Nova Forma skills.
license: Apache-2.0
metadata:
  author: Board of Innovation
  version: "1.0.0"
---

# Nova Forma value-at-stake sizer

Estimates what redesigning the workflow could be worth, as a range a year with every assumption visible.

This skill runs step 4 of the Nova Forma intake: agree where the value comes from, measure today's work, and size a low and a high case next to the build and running costs. It ends with a one-page brief for the redesign week.

The Nova Forma chain: 1. workflow identifier, 2. outcome statement writer, 3. requirements lister, **4. value-at-stake sizer** (this skill).

Two rules matter most. Freed hours are worth nothing until someone decides where they go, or turns them into a real saving. And early estimates shrink, so always show a range.

## Before you write

Read `references/display.md` for how every message looks, asks and draws, and `references/writing.md` for the check every message passes before it goes out. The users are business owners and managers, mostly new to AI, so every message must work without help.

Start every step message with the tracker from `display.md`: step 4, Size the value, with the parts where the value lands → numbers → value range.

**Why this step**, to say when it opens: "Freed hours are only worth money once someone decides where they go. So we first agree where the value lands, then ask only the numbers that size it, and you get a range you can defend."

The skill runs in three moments. Never ask for numbers before the user has agreed where the value lands.

## Moment 1: agree where the value lands

1. **Read the context** as `references/context.md` describes. The scope card gives where the value comes from, the outcome statement the measures, and the requirements list the work.

   **If you start here**: you need the workflow, from what starts it to what the receiver gets at the end, who does the work today, and where the value comes from. Ask for what is missing as `context.md` describes. The cards in step 3 settle where the value comes from, so ask the other two first.

2. **Send the opening message**, visible before the cards: the tracker, the brief so far, Why this step, and in one sentence where the value comes from according to the scope card. Then the visual: the four sources of value in `references/levers.md` as cards, each marked `●` likely, `◐` possible or `○` unlikely, with a reason in a few words. Call them sources of value, never levers.

3. **Ask in one round of question cards**, as `display.md` describes, each with a recommended answer and where it came from:
   - **Is the team full?** "Does some work go unanswered, or get a rushed answer, because the team is full?" Options: "Yes, some work is turned away or rushed", "No, we keep up with all of it". Yes means the value is growth.
   - **Where would freed hours go?** "If this work took less time, where would the hours go?" Options: "More of the same work, such as more proposals", "Fewer hires as people leave", "More time on quality". Multi-select: pick more than one for a mix. Hours spent on quality count only under better results, as errors and rework avoided.
   - **What matters most?** "Which result matters most to the business?" Options: "Win more work", "Faster turnaround", "Better price or margin", "Lower cost or risk".

## Moment 2: the numbers that size it

4. **List only the inputs the agreed sources of value need**, from `references/levers.md`. Add what the checks in step 11 need: the team's size in full-time people, the work it handles today when freed time goes to more of it, and the company's revenue or operating profit (EBIT). Eight rows at most: put related inputs in one row. Fill each from the earlier steps or the user's files. Tag each one `✓ from you`, `≈ hypothesis` or `? needed`. Use a hypothesis only for what nobody can know yet, such as the share of hours AI could take over, and say what it rests on. Never invent a number the user is likely to know, such as order value, hours per case or cost per error.

5. **Send the inputs table** as a visible message: #, Input, Value, Source. Mark the two inputs that move the case most, and say why in one line.

6. **Ask for each `? needed` input in question cards**, up to four a round, as ranges that do not overlap, such as "Under 50 a year", "50 to 100", "100 to 200", "More than 200". Recommend the range the evidence points to. The user types an exact figure when they know it. In an inline form, use sliders. Then ask one last card: "Shall I use my hypotheses for the rest?" Options: "Yes, use them and mark them (Recommended)", "No, I'll correct a row".

## Moment 3: the value range

7. **Build the baseline**: hours a year and FTE, at about 1,700 hours per FTE unless told otherwise. Turn hours a week into hours a year at 46 working weeks.
8. **Estimate the share of hours AI could take over**, low and high, with `references/addressable-share.md`.
9. **Size the four sources of value**, each with its formula in `references/levers.md`: savings, freed time put to use (capped by real demand), better results, and a new offer. Count every freed hour in one source only.
10. **Compute** with `scripts/value_case.py`, so both cases use the same arithmetic. Write the inputs to a JSON file in the format in `references/levers.md`, then run `python3 scripts/value_case.py <file>`. When it stops with a line that starts "Error:", fix that input and run it again. If code cannot run here, work it out by hand and check it twice. The script's labels are for you: show the user savings, freed time put to use, better results and a new offer, never FTE savings, business impact or NPV.
11. **Run the four checks** in `references/levers.md`: extra volume, the team's hours, the case against the company's size, and a payback under six months. When the case fails one, cap it and say why in plain words. A range that looks too good loses the reader.

## The result

Send it as one visible message, in this order:

1. **Headline**: "Worth about X to Y a year, before costs", the source of value that matters most, and one line on what moves the range most.
2. **The visual**: a floating bar from low to high for each source of value, and one for the total, the biggest source in the accent.
3. **Where the money comes from**: a table with Source of value, Low, High, and Basis in one line.
4. **Reality check**: one line on how big the case is against the business, such as a share of revenue or of today's margin, and one line with the rough cost, the net value a year and the payback. Mark costs nobody has quoted as a placeholder, and say when a payback under six months needs checking. Cite at most one finding, from `references/evidence.md`, where it helps, such as how few companies get 5% of their EBIT from AI.
5. **How we use this**: "The range says whether a redesign is worth a week of your team's time, and which number to firm up first."
6. **Where I need your input**: review the range and share feedback, then one or two things the user can do this month, without IT or spend, that firm up the weakest input, such as counting last year's declined requests or timing 20 recent cases. Name freed hours that still need a destination.

Then ask the next step in a question card: "Shall I put the four results on one page for the redesign week?" Options: "Yes, make the one-pager (Recommended)" and "Adjust the numbers first". Without cards, end with "Reply Accept for the one-pager, or Adjust with your changes."

On accept, make the one-pager as `references/one-pager.md` describes. It is a document with five short sections: the workflow and why it was picked, with the swimlane flow; the success definition; today's work; the value range; and the open points as a checklist. Use the environment's document type where there is one.

When the user names a template, such as a stage gate, map the result to its headings and mark what is still open.

Round money to two significant figures and show the currency. `references/example-inquiry-to-quote.md` shows the three moments, and `references/one-pager.md` ends with the one-pager for the same example.
