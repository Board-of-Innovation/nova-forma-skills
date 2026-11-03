---
name: "nova-forma-outcome-statement-writer"
description: Write the outcome statement of a workflow as one sentence that says who gets what result, by when or to what standard, within which constraints, backed by three to six measures, the working principles, and the red lines with their owners. Use this whenever someone wants to define the purpose, goal, outcome or north star of a process or workflow, set KPIs for it, write a problem statement before an AI project, or check whether a goal is really an outcome. Second of the four Nova Forma skills.
---

# Nova Forma outcome statement writer

Writes one sharp outcome statement for a workflow: who gets what result, by when or to what standard, within which limits. Every later choice traces back to it.

This skill runs the outcome part of the recipe's second phase: the statement, its four tests, the measures, the principles and the red lines.

The Nova Forma chain: 1. workflow identifier, **2. outcome statement writer** (this skill), 3. requirements lister, 4. value-at-stake sizer.

## Before you write

Read `references/display.md` for how every message looks, asks and draws, and `references/writing.md` for the check every message passes before it goes out. The users are business owners and managers, mostly new to AI, so every message must work without help.

Start every reply with the tracker from `display.md`: step 2, Define success, with the parts your calls → success definition.

**Why this step**, to say when it opens: "This sets the yardstick for the redesign: work that serves the result stays, and work that only exists because systems don't connect goes. The measures and red lines then help us pick between the new ways of working we design."

## How it runs

1. **Read the context** as `references/context.md` describes. Start from the scope card of the workflow identifier if there is one. When there is none, ask its core question first, as `context.md` describes.

2. **Send the opening message**, visible before the cards: the tracker, the brief so far, Why this step, and one line on what you found, with a visual: the scope card's start and end as a simple from → to strip, with the receiver named.

3. **Ask your calls in one round of question cards**, as `display.md` describes, at most four. Recommend an answer on each, with where it came from. Skip any the context already answers. Never ask for volumes, hours or costs: the value-at-stake sizer asks those.
   - **Who receives the result?** "Whose result should the new way of working improve?" Options built from the scope card, such as "The client's decision maker (Recommended)", "Our own team", "Both, with different needs". When two receivers want different results, the statement names both.
   - **What counts as good?** "What standard or deadline counts as a good result?" Two or three concrete standards from the evidence, such as "Within 5 working days, or by the deadline (Recommended)" and "Within 10 working days".
   - **Which red lines apply?** "Which rules may the new way of working never break? Pick all that apply." Multi-select, up to four, built from the scope card's approvals and the evidence, such as "An MD signs every price". The user types any others.
   - **Which principles fit?** "Which working principles should the new way of working follow? Pick all that fit." Multi-select, all four recommended:
     - "AI prepares, people decide": AI reads, drafts and checks, and people sign what commits the company.
     - "Visible AI, labelled and logged": every AI draft is marked, and every edit and approval is logged.
     - "Guidance without roadblocks": checks flag gaps and risks, and only red lines block.
     - "Reduce work, don't shift it": time saved in one role does not move to another.

     The recipe's fifth starter card, what stays human-only, is answered by the red lines card.

4. **Write the statement** with one pattern: who gets what result, by when or to what standard, within which limits. One statement per workflow.

5. **Test it** and fix it until it passes all four tests:
   - Receiver: it names who gets the result, never "the business" or "leadership".
   - Solution-free: it names a result in the world. What the receiver acts on, such as a quote, is fine; a tool, a report or a meeting as the goal is not.
   - Stop: someone outside the team would notice if the workflow stopped.
   - Measurable: three to six measures prove it.

6. **Add the measures and red lines.** Three to six measures, each with today, a target and where it is measured, or "unmeasured". Typical ones: elapsed time, hours of the scarcest people per case, quality at first review, win or conversion rate, price held. Red lines are rules a new way of working may never break, each with an owner. Savings belong in the business case, never in the statement.

## The result

Send it as one visible message, in this order:

1. **The statement**, on its own, as a highlighted card where the environment can draw, otherwise as a quote block.
2. **Tests**: four ticks, such as `Receiver ✓ Solution-free ✓ Stop ✓ Measurable ✓`.
3. **Measures**: the visual first, each measure as a today → target bar, then a table with Measure, Today, Target and Source.
4. **Principles**: the chosen principles, one line each.
5. **Red lines**: the visual as a fence the new way of working stays inside, then a table with Red line and Owner, each marked `⛔`.
6. **How we use this**: "These measures and red lines are the scorecard for picking the best new way of working: each option is scored on the measures, and any option that breaks a red line is out." Show it as a mini scorecard: the measures as rows, options A, B and C as empty columns, and a last row "Breaks a red line?".
7. **Where I need your input**: review the statement and share feedback, then each open point, such as a target to confirm or a measure nobody tracks yet.

Then ask the next step in a question card: "Is this the right definition of success?" Options: "Yes, go to step 3: map today's work (Recommended)" and "Adjust the statement first". Without cards, end with "Reply Accept to go to step 3, or Adjust with your changes." On accept, launch nova-forma-requirements-lister.

`references/examples.md` shows two results.
