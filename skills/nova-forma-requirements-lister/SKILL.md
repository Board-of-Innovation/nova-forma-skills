---
name: nova-forma-requirements-lister
description: List every requirement a current workflow follows, sorted into what it must know, decide, produce, execute and monitor, with who owns each one and the step where it shows up, plus the exceptions the workflow handles. Use this whenever someone wants to map how a process really works, build an as-is inventory before a redesign or AI project, understand why a workflow has so many hand-offs, approvals or checks, or turn process documents and interview notes into a structured list, even if they just say "map our current process". Third of the four Nova Forma skills.
license: Apache-2.0
metadata:
  author: Board of Innovation
  version: "1.0.0"
---

# Nova Forma requirements lister

Lists everything the workflow requires today, as it runs now: what it must know, decide, produce, do and check, who owns each part, and the cases that leave the normal path. The list describes and never judges, because a redesign needs to see the habits too.

This skill runs the first part of the recipe's third phase: the requirements in five buckets and the exceptions. Each requirement gets its verdict later, in the redesign week.

The Nova Forma chain: 1. workflow identifier, 2. outcome statement writer, **3. requirements lister** (this skill), 4. value-at-stake sizer.

## Before you write

Read `references/display.md` for how every message looks, asks and draws, and `references/writing.md` for the check every message passes before it goes out. The users are business owners and managers, mostly new to AI, so every message must work without help.

Start every reply with the tracker from `display.md`: step 3, Map today's work, with the parts your calls → requirements.

**Why this step**, to say when it opens: "A redesign starts from what the work needs. With every requirement listed, with its owner and where it shows up, we can test each one against the result: keep it, combine it, move it or drop it. The odd cases decide whether a new way of working holds up in real life."

The five buckets are what the work must **know**, **decide**, **produce**, **do** and **check**. Use these plain names everywhere the user looks, tables included. They are the recipe's Know, Decide, Produce, Execute and Monitor.

## How it runs

1. **Read the context** as `references/context.md` describes. The scope card and the outcome statement set the boundary: nothing before what starts the workflow, nothing after what the receiver gets.

2. **Send the opening message**, visible before the cards: the tracker, the brief so far, Why this step, and one line on what you found and where, with a visual: the workflow's steps as a strip, each marked by how much evidence you have, so the user sees where the gaps are.

3. **Ask your calls in one round of question cards**, as `display.md` describes, at most four. Recommend an answer on each, with where it came from. Skip any the context already answers. Never ask for volumes, hours or costs: the value-at-stake sizer asks those. Typical cards:
   - **Who owns a requirement nobody named?** "Who decides go or no-go on a proposal today?" Options: the roles you saw in the evidence, the likeliest first.
   - **Which source holds where they disagree?** "Your process document says X, the meetings show Y. Which is how it really works?" Options: "How it really runs: Y (Recommended)", "What the document says: X".
   - **How often does an important exception happen?** "How often does a brief come through a procurement portal?" Options as ranges that leave no gaps, in their natural order: "Under 1 in 10", "1 in 10 to 1 in 5 (Recommended)", "1 in 5 to 1 in 3", "More than 1 in 3".

4. **Walk the workflow step by step**, using the step names of the scope card's swimlane flow, so the user sees the same steps in every picture. At each step, ask what must be known, decided, produced, done and checked there. Add the approvals, reports and recurring meetings that cut across steps.

5. **Write each requirement as found**, in one line, at a size one owner can carry. Include the hidden ones: checks no procedure mentions, typing the same data twice, chasing people for status.

6. **List the exceptions** from six sources, in this order of priority: law, rules, input, case, clock and format. When exceptions coincide, the higher one is settled first.

7. **Check coverage** without showing it: every step meets at least one requirement.

## The result

Send it as one visible message, in this order:

1. **Summary**: one line with the number of requirements, and the three that take the most time.
2. **The visual**: a heat map of the workflow's steps against the five buckets, cells shaded by count, the three heaviest cells in the accent.
3. **The requirements that matter most**: one table with five to eight rows, at least one per bucket, each prefixed with its bucket. Columns:
   - Requirement: one line, in the words of the people who do the work.
   - By whom: the person or role who owns it today, or "Nobody today".
   - Step: where it shows up.
4. **Exceptions**: one table with four columns:
   - Source: law, rules, input, case, clock or format.
   - Exception and how often: the case, and its share, or "unmeasured".
   - Step: where it enters the workflow.
   - Handled by: who deals with it today.
5. **How we use this**: "In the redesign week, each requirement gets one verdict against the result, and each one that stays gets an owner: a person, AI with a person checking, or AI alone."
6. **Where I need your input**: review the list and share feedback, then each open point: a requirement with no owner or reason, sources that contradict each other, or a short set of questions to forward to the people who do the work.
7. **Appendix: all requirements by bucket**, after a horizontal rule and "For reference, no action needed.": one table per bucket, same three columns. Where the environment can attach a file or a collapsed section, use that instead.

Then ask the next step in a question card: "Does this match how the work really runs?" Options: "Yes, go to step 4: size the value (Recommended)" and "Adjust the list first". Without cards, put the question in a quote block before the appendix and repeat it as the last line: "Reply Accept to go to step 4, or Adjust with your changes." On accept, launch nova-forma-value-at-stake-sizer.

`references/example-inquiry-to-quote.md` shows a result.
