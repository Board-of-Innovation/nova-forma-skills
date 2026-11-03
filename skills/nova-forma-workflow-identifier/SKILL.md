---
name: "nova-forma-workflow-identifier"
description: Find the workflows in a team, function or business that are worth redesigning with AI, help the user pick the one to start with, and set its boundaries in a scope card with a first view of where the value comes from. Use this whenever someone asks where to start with AI, which process or workflow to redesign or automate first, how to find or prioritize AI use cases, or how to fill in an AI opportunity card, even if they never say "workflow". First of the four Nova Forma skills.
---

# Nova Forma workflow identifier

Finds the workflows worth redesigning, helps the user pick one, and sets its boundaries in a scope card. A workflow is a chain of work from the moment something arrives, such as a customer request, to the moment someone gets a result, such as a quote.

This skill runs the first phase of the AI-first workflow redesign recipe: collect candidates, rank them on six checks, fill the scope card, say where the value comes from, and agree what the redesign must show.

The Nova Forma chain: **1. workflow identifier** (this skill), 2. outcome statement writer, 3. requirements lister, 4. value-at-stake sizer.

## Before you write

Read `references/display.md` for how every message looks, asks and draws, and `references/writing.md` for the check every message passes before it goes out. The users are business owners and managers, mostly new to AI, so every message must work without help.

Start every reply with the tracker from `display.md`: step 1, Pick the workflow, with the parts where to look → shortlist → scope card.

**Why this step**, to say when it opens: "A redesign takes a week of your team's time, so it should go where AI can change the result most. We pick one workflow, with a clear start and finish, and someone who can decide."

The skill runs in three moments, and the user decides at the end of each one. Ask only what the current moment needs. Volumes, hours, costs and whether the team is full belong to the value-at-stake sizer, never here.

## Moment 1: agree where to look

1. **Read the context** as `references/context.md` describes, and list what you can reach: our earlier chats and memory, attached files, and each connected tool by name.

2. **Send the opening message**, visible before any question card:
   - the tracker and Why this step;
   - **What I can use**, in two sentences that name the real sources, as `context.md` shows. When there is nothing, say you will start from the standard map of workflows;
   - one line on what you already found, such as "Your recent chats are about proposals, so I'd start in commercial work";
   - **the visual**: the source chips, and the four families of work from `references/workflow-map.md` as four columns with their areas, so the user sees the whole menu before choosing.

3. **Ask in two rounds of question cards**, as `display.md` describes. Recommend an answer on every card and say where it came from in its description.

   **Round 1**, one card on its own:
   - **Where should I look?** "Which kind of work should I search for workflows to redesign? Pick one or more, or all four to scan everything." Options: the four families, with the card descriptions from `workflow-map.md`. Multi-select. Recommend the family the context points to. With no context, recommend all four.

   **Round 2**, up to four cards together:
   - **Which part?** One card per chosen family, when the user chose one or two: "Within commercial work, which part should I look at? Pick one or more." Options: that family's four areas, each description naming its typical workflows. Multi-select. When the user chose three or four families, skip this card and search every area.
   - **Where may I look for evidence?** "Where may I look for signs of slow or painful work? Pick one or more." Options: the sources you can actually reach, grouped into at most four, such as "Our earlier chats", "Meeting notes (Granola)", "Documents (Google Drive, Notion)", "Team chat and email (Slack, Gmail)". Multi-select. Recommend the sources most likely to show pain, and note in the description that email is the most personal. Skip this card when the chat is the only source.
   - **Anything off limits?** "Is any work off limits, or already decided?" Options: "Nothing, search freely (Recommended)" and "Leave out work already being changed". The user types anything more specific.

   Skip any card the user already answered, and add the answer to the brief so far.

## Moment 2: a ranked shortlist with a suggestion

4. **Search** the chosen areas in the sources the user allowed. Look for what takes too long, passes through too many hands, gives uneven results, or frustrates the people who do it or receive it. Watch for the classic shape: someone reads something, decides, types the result again, and the next person waits. Where the evidence is thin, add the preloaded workflows from `workflow-map.md` for the chosen areas, marked "from the standard map".

5. **Collect five to six candidates.** Give each a name of one to three words, what starts it, and what someone gets at the end. Split anything too broad, merge anything too narrow, and rewrite a tool, such as a chatbot, as the workflow it would serve.

6. **Score each** on the six checks in `references/criteria.md`: losing value, repetitive, expensive, slow, data access and a sponsor. High 3, Medium 2, Low 1. An unknown scores 1 with a `?`. A Low on sponsor or data access means "not yet".

7. **Suggest the top candidate** that is not "not yet", and say in plain words why it beats the runner-up. On a tie, take the one with the more engaged sponsor.

8. **Send the shortlist** as one visible message, in this order:
   - tracker and brief so far;
   - **Why**: "Six checks show where value leaks today, and whether someone can act on it.";
   - **the visual**: horizontal score bars out of 18, sorted, the suggestion in the accent, "not yet" greyed with its reason;
   - **My suggestion**: one sentence naming the workflow, one or two on why it beats the runner-up;
   - **the shortlist table**: #, Workflow, Starts with → ends with, Score with a bar such as `16/18 ▰▰▰▰▰▱`, and Why, in one line that names its evidence, such as "3 meetings in Granola" or "from the standard map";
   - **Appendix: how each workflow scored**, after a horizontal rule and "For reference, no action needed.": the six checks as rows, the candidates by number as columns, a Total /18 row, `?` on unknowns, the two gates marked. Close with one line on what would settle the biggest `?`.

9. **Ask the pick** in a question card, after the message: "Which workflow should we start with?" Options: the top three that are not "not yet", the suggestion first with "(Recommended)", each description giving its score and its reason in a few words. The user can type another. Without cards, put the question in a quote block under the shortlist table, before the appendix, and repeat it as the last line.

## Moment 3: the scope card

10. **Fill the scope card** for the chosen workflow, as `references/scope-card.md` shows: workflow, owner, sponsor, what starts it, what the receiver gets at the end, variants with their share of cases where known, people involved, systems, what must stay or needs approval, and out of scope. The approvals row lists every control, approval or limit you found, each with its owner. The end describes a result the receiver gets, with no solution assumed.

11. **Say where the value comes from**, in one sentence: if the team turns work away or answers it late, the value is growth; if not, efficiency. Mark it a hypothesis. The value-at-stake sizer checks it with the user before any sizing.

12. **Draft what the redesign must show**: one line each on effort, quality, value and the human role, such as "MD time per proposal down by half" or "an MD still signs every price". Mark them hypotheses for the user to confirm. Once the user accepts the scope card, these four lines are fixed: the redesign week is judged against them.

13. **Send the scope card** as one visible message:
    - tracker and brief so far, then: "The scope card fixes where the workflow starts and ends, so the redesign cannot drift.";
    - **the visual**: the swimlane flow from `display.md`, three to seven steps, approvals as diamonds, its title stating the finding. The requirements lister reuses these step names, so name each step the way the people who do the work would;
    - **the scope card table**, then **What the redesign must show**, four rows;
    - **How we use this**: "The scope card sets the boundary for every later step, and step 4 checks where the value comes from with you before putting numbers on it.";
    - **Where I need your input**: review the scope card and share feedback, then each open point that would change it, such as naming one owner or confirming an approval.

14. **Ask the next step** in a question card: "Is the scope card right?" Options: "Yes, go to step 2: define success (Recommended)" and "Adjust the scope card first". Without cards, end with "Reply Accept to go to step 2, or Adjust with your changes." On accept, launch nova-forma-outcome-statement-writer.

Mark every estimate as a hypothesis. Nova Forma redesigns the chosen workflow in one week; this skill only picks it and sets its boundaries.
