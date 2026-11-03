---
name: nova-forma-requirements-lister
description: List every requirement a workflow follows today, sorted into what it must know, decide, produce, do and check, with who owns each one, the step where it shows up, and the exceptions it handles. Use when someone plans to redesign or automate a specific workflow with AI and wants to map how it really runs today, build an as-is inventory before the redesign, see why it has so many hand-offs, approvals or checks, or turn its process documents and interview notes into a requirements list. Not for drawing flowcharts or BPMN diagrams, or writing SOPs. Step 3 of the four Nova Forma skills.
license: Apache-2.0
metadata:
  author: Board of Innovation
  version: "1.0.0"
---

# Nova Forma requirements lister

Lists everything the workflow requires today, as it runs now: what it must know, decide, produce, do and check, who owns each part, and the cases that leave the normal path. The list describes and never judges, because a redesign needs to see the habits too.

This skill runs step 3 of the Nova Forma intake: list the requirements in five buckets, with their owners and steps, and the exceptions. Each requirement gets its verdict later, in the redesign week.

The Nova Forma chain: 1. workflow identifier, 2. outcome statement writer, **3. requirements lister** (this skill), 4. value-at-stake sizer.

## Before you write

Read `references/display.md` for how every message looks, asks and draws, and `references/writing.md` for the check every message passes before it goes out. The users are business owners and managers, mostly new to AI, so every message must work without help.

Start every step message with the tracker from `display.md`: step 3, Map today's work, with the parts your calls → requirements.

**Why this step**, to say when it opens: "A redesign starts from what the work needs. With every requirement listed, its owner and where it shows up, we can test each one against the result. Then we keep it, combine it, move it or drop it. The odd cases decide whether a new way of working holds up in real life."

The five buckets are what the work must **know**, **decide**, **produce**, **do** and **check**. Use these plain names everywhere the user looks, tables included.

## How it runs

1. **Read the context** as `references/context.md` describes. The scope card and the outcome statement set the boundary: nothing before what starts the workflow, nothing after what the receiver gets.

   **If you start here**: you need the workflow, what starts it, what the receiver gets at the end, and who that receiver is, plus the outcome statement if there is one. Ask for what is missing as `context.md` describes.

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

1. **Summary**: one line with the number of requirements, and the three steps that carry the most requirements.
2. **The visual**: a heat map of the workflow's steps against the five buckets, cells shaded by count, the three heaviest cells in the accent.
3. **The requirements that matter most**: one table with five to eight rows, at least one per bucket, each prefixed with its bucket. Columns:
   - Requirement: one line, in the words of the people who do the work.
   - By whom: the person or role who owns it today, "Nobody today" when no one owns it, or "Unknown, to confirm" when the evidence does not say.
   - Step: where it shows up.
4. **Exceptions**: one table with four columns:
   - Source: law, rules, input, case, clock or format.
   - Exception and how often: the case, and its share, or "unmeasured".
   - Step: where it enters the workflow.
   - Handled by: who deals with it today.
5. **How we use this**: "In the redesign week, each requirement gets one verdict against the result. Each one that stays gets an owner: a person, AI with a person checking, or AI alone."
6. **Where I need your input**: review the list and share feedback, then each open point: a requirement with no owner or reason, sources that contradict each other, or a short set of questions to forward to the people who do the work.
7. **Appendix: all requirements by bucket**, after a horizontal rule and "For reference, no action needed.": one table per bucket, same three columns. Where the environment can attach a file or a collapsed section, use that instead.

Then ask the next step in a question card: "Does this match how the work really runs?" Options: "Yes, go to step 4: size the value (Recommended)" and "Adjust the list first". Without cards, put the question in a quote block before the appendix and repeat it as the last line: "Reply Accept to go to step 4, or Adjust with your changes." On accept, continue with step 4, Size the value, by following the nova-forma-value-at-stake-sizer skill. If that skill is not available here, say so in one line, give the accepted requirements and exceptions, with the workflow's start and end, as one block the user can paste into a new chat, and say the four Nova Forma skills are at <https://github.com/Board-of-Innovation/nova-forma-skills>.

`references/example-inquiry-to-quote.md` shows a result.
