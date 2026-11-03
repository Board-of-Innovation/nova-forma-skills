# The one-pager for the redesign week

The one-pager puts the four results on one page, so everyone in the redesign week starts from the same brief. Make it when the user accepts the value range.

## Where it goes

Use the environment's document type where there is one, such as an artifact, a canvas or a document the user can download. Without one, send it as one message in plain markdown that the user can copy. It is a document, so the word limit for messages in `display.md` does not apply. Keep it to about 400 words, visuals and tables included.

## What it holds

The tracker comes first, with all four steps marked `✓ Done`. Nothing goes above it. Then the title, `<Workflow>: brief for the redesign week`, and five short sections in this order. Each one reuses the visual of its step from `display.md`, or that visual's text version where nothing can be drawn.

| Section | What it holds | Visual |
| --- | --- | --- |
| The workflow | From what start to what end, why it was picked in one line, the owner and the sponsor | The swimlane flow from the scope card |
| Success | The outcome statement, the measures with today and target, the red lines with their owners | The statement as a card, each measure as a today → target bar, the red lines in a table marked `⛔` |
| Today's work | How many requirements, which steps carry most of them, and the exceptions that matter most | The heat map of steps against the five buckets |
| The value | The yearly range before costs, the source of value that leads, the rough cost and the payback, or the spending ceiling when there is no cost | The floating bars for each source of value and the total |
| Open points | The open asks from the four steps that would change the brief, at most eight, those that move the value or the scope first | A checklist, one `- [ ]` per point |

- **Copy from the results the user accepted**: the same numbers, names and words. Add no new number or claim here.
- **A step that never ran** keeps its section, with one line: `Not done yet: run step N, <step name>.` When the user gave some of that step's content, such as the workflow's start and end under "If you start here", show it above that line, marked `from you`. Its tracker column reads `Skipped`, as `display.md` says. Never fill it in from guesses, and end the open points with one line saying the four skills are at <https://github.com/Board-of-Innovation/nova-forma-skills>.
- **Each open point once**, in the words of the step that raised it. Leave out the ones the user has settled since.
- **Cut detail before you cut a section.** Two lines and a visual make a section.
- **Close with the sources line** from `context.md` when any step used more than the conversation.

## The closing ask

After the document, send one short message with "Where I need your input:". First, review the one-pager and share feedback. Then the one open point that matters most before the redesign week.

Then ask in a question card: "Is the one-pager ready to share with the people in the redesign week?" Options: "Yes, it's ready to share (Recommended)" and "Adjust it first". Without cards, end with "Reply Accept if it is ready to share, or Adjust with your changes." On accept, close in one line: the four steps are done, and the brief is ready for the redesign week.

## Example: inquiry to quote

Figures are illustrative. Each section copies the example result of its step.

| 1 Pick the workflow | 2 Define success | 3 Map today's work | 4 Size the value |
| :---: | :---: | :---: | :---: |
| ✓ Done | ✓ Done | ✓ Done | ✓ Done |

**Inquiry to quote: brief for the redesign week**

### The workflow

From a request for a quote landing in the shared inbox to a correct quote the customer can act on, logged in the ERP. Picked at 17 of 18: small requests are declined today, so it loses money every month. Owner: the inside sales lead. Sponsor: the sales director.

[Visual: the swimlane flow from the scope card, titled "Every quote waits on an engineer and two manager decisions".]

### Success

> Every customer who sends a request for a quote receives a correct quote they can act on within one working day, priced inside the discount rules and above the margin floor.

[Visual: one bar per measure, today to target. Turnaround: days → one working day. Quotes checked against the rules: a sample → every quote. Small requests: most declined → every one quoted.]

| Red line | Owner |
| --- | --- |
| ⛔ Never quote below the margin floor | Pricing manager |
| ⛔ Discounts above the limit need the sales manager's approval | Sales manager |
| ⛔ Every deviation from the specification is signed | Application engineer |
| ⛔ A person still signs every price and bid before anything leaves | Sales manager |

### Today's work

15 requirements. Reading the request, building the price, and sending and logging carry the most. About half of requests arrive with missing specifications.

[Visual: the heat map of the six steps against the five buckets, the columns of the three busiest steps in the accent.]

### The value

Worth about EUR 420k to 1M a year, before costs. Better prices and the small requests you now decline lead.

[Visual: floating bars from low to high. Better results EUR 200k to 550k in the accent; freed time put to more quotes EUR 190k to 380k; savings EUR 30k to 97k; a new offer not sized; total EUR 420k to 1M.]

At EUR 250k to 400k to build and EUR 60k to 100k a year, the net value is EUR 320k to 960k a year, and payback runs 3 to 15 months.

### Open points

- [ ] Check last quarter's discounts against the rules: the leakage figure carries half the low case.
- [ ] Count last year's declined requests.
- [ ] Check how many requests really need an engineer: if most do, the gain shrinks.
- [ ] Decide where 1,700 freed hours go in the high case.
- [ ] Confirm the sales director as sponsor.
- [ ] Name who owns the margin check before sending, or confirm nobody does.
- [ ] Ask two inside sales reps how often a request arrives with missing specifications.
- [ ] Check whether time records split standard from novel requests. If not, engineer hours stay unmeasured.

Sources: your note, Google Drive and Gmail.

**Closing message**

Where I need your input:

- Review the one-pager and share feedback.
- Check last quarter's discounts before the redesign week: that figure moves the range most.

**Next card**

- Header "One-pager". "Is the one-pager ready to share with the people in the redesign week?"
- Options: "Yes, it's ready to share (Recommended)", "Adjust it first".

Had the user skipped step 3, its section would read "Not done yet: run step 3, Map today's work.", and its tracker column `Skipped`.
