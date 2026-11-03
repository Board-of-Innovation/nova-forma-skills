---
name: nova-forma-outcome-statement-writer
description: Write the outcome statement of a workflow as one sentence that says who gets what result, by when or to what standard, within which constraints, backed by three to six measures, the working principles, and the red lines with their owners. Use when someone wants to define the purpose, goal, outcome or north star of a specific workflow they plan to redesign or automate with AI, set the measures or KPIs that prove it, or check whether its goal is really an outcome. Not for team or company KPIs in general. Step 2 of the four Nova Forma skills.
license: Apache-2.0
metadata:
  author: Board of Innovation
  version: "1.0.0"
---

# Nova Forma outcome statement writer

Writes one sharp outcome statement for a workflow: who gets what result, by when or to what standard, within which limits. Every later choice traces back to it.

This skill runs step 2 of the Nova Forma intake: the statement, its four tests, the measures, the principles and the red lines.

The Nova Forma chain: 1. workflow identifier, **2. outcome statement writer** (this skill), 3. requirements lister, 4. value-at-stake sizer.

## Before you write

Read `references/display.md` for how every message looks, asks and draws, and `references/writing.md` for the check every message passes before it goes out. The users are business owners and managers, mostly new to AI, so every message must work without help.

Start every step message with the tracker from `display.md`: step 2, Define success, with the parts your calls → success definition.

**Why this step**, to say when it opens: "This sets the yardstick for the redesign: work that serves the result stays, and work that only exists because systems don't connect goes. The measures and red lines then help us pick between the new ways of working we design."

## How it runs

1. **Read the context** as `references/context.md` describes. Start from the scope card of the workflow identifier if there is one, including its four lines on what the redesign must show: effort, quality, value and the human role. The user accepted them in step 1, so never ask them again. Turn each into at least one measure or red line, and keep its wording. When one needs to change, such as a target nobody can measure, keep it as it is and raise the change under Where I need your input.

   **If you start here**: you need the workflow, what starts it, what the receiver gets at the end, and who that receiver is. Ask for what is missing as `context.md` describes.

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

     Do not ask separately what stays human-only: the red lines card covers it.

4. **Write the statement** with one pattern: who gets what result, by when or to what standard, within which limits. One statement per workflow.

5. **Test it** and fix it until it passes all four tests:
   - Receiver: it names who gets the result, never "the business" or "leadership".
   - Solution-free: it names a result in the world. What the receiver acts on, such as a quote, is fine; a tool, a report or a meeting as the goal is not.
   - Stop: someone outside the team would notice if the workflow stopped.
   - Measurable: three to six measures prove it.

6. **Add the measures and red lines.** Three to six measures, each with today, a target and where it is measured, or "unmeasured". Typical ones: elapsed time, hours of the scarcest people per case, quality at first review, win or conversion rate, price held. To show a target is realistic, cite at most one finding from `references/evidence.md`, by its rules, and only when it fits. Red lines are rules a new way of working may never break, each with an owner. Savings belong in step 4, Size the value, never in the statement.

## The result

Send it as one visible message, in this order:

1. **The statement**, on its own, as a highlighted card where the environment can draw, otherwise as a quote block.
2. **Tests**: four ticks, such as `Receiver ✓ Solution-free ✓ Stop ✓ Measurable ✓`.
3. **Measures**: the visual first, each measure as a today → target bar, then a table with Measure, Today, Target and Source.
4. **Principles**: the chosen principles, one line each.
5. **Red lines**: a table with Red line and Owner, each marked `⛔`.
6. **How we use this**, in one line: "In the redesign week, each new way of working is scored on these measures, and any that breaks a red line is out."
7. **Where I need your input**: review the statement and share feedback, then each open point, such as a target to confirm, a measure nobody tracks yet, or a change to one of the scope card's four lines.

Then ask the next step in a question card: "Is this the right definition of success?" Options: "Yes, go to step 3: map today's work (Recommended)" and "Adjust the statement first". Without cards, end with "Reply Accept to go to step 3, or Adjust with your changes." On accept, continue with step 3, Map today's work, by following the nova-forma-requirements-lister skill. If that skill is not available here, say so in one line, give the accepted success definition, with the workflow's start and end, as one block the user can paste into a new chat, and say the four Nova Forma skills are at <https://github.com/Board-of-Innovation/nova-forma-skills>.

`references/examples.md` shows two results.
