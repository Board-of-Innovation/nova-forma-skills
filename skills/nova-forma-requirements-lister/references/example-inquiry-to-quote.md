# Example result: inquiry to quote

Figures are illustrative. To keep it short, the example leaves out the tracker and the brief so far, which every step message still opens with.

**Summary:** 15 requirements. Reading the request, building the price, and sending and logging carry the most.

[Visual: a heat map titled "Reading, pricing and sending carry most requirements". Rows: Know, Decide, Produce, Do, Check. Columns: the six steps of the scope card's swimlane, from read the request to send and log. Cells shaded by count; the heaviest cells in read the request, build the price, and send and log in the accent.]

| Requirement | By whom | Step |
| --- | --- | --- |
| Know: the customer's requirements and specifications | Inside sales | Read the request |
| Decide: bid or no-bid, before pricing | Sales manager | Bid or no-bid |
| Decide: every deviation reviewed and signed by an engineer | Application engineer | Deviation review |
| Produce: the request typed again into the quoting worksheet | Inside sales | Read the request |
| Produce: a priced draft within the discount rules | Pricing manager | Build the price |
| Do: the quote logged in the ERP and the CRM | Inside sales | Send and log |
| Check: margin checked once more before sending, in no procedure | Unknown, to confirm | Send and log |

| Source | Exception and how often | Step | Handled by |
| --- | --- | --- | --- |
| Law | An export-controlled product; unmeasured | Read the request | Compliance |
| Rules | A discount above the limit or a price below the floor; unmeasured | Approve discounts | Sales manager, pricing manager |
| Input | An unreadable request or missing specifications; about half of requests | Read the request | Inside sales |
| Case | A novel request or a strategic account; unmeasured | Deviation review | Application engineer |
| Clock | A rush request; unmeasured | Read the request | Inside sales |
| Format | The customer's own quote form; unmeasured | Send and log | Inside sales |

How we use this: in the redesign week, each requirement gets one verdict against the result. Each one that stays gets an owner: a person, AI with a person checking, or AI alone.

Where I need your input:

- Review the list and share feedback.
- Name who owns the margin check before sending, or confirm nobody does.
- Ask two inside sales reps how often a request arrives with missing specifications.

---

**Appendix: all requirements by bucket**

For reference, no action needed.

## Know

| Requirement | By whom | Step |
| --- | --- | --- |
| The customer's requirements and specifications | Inside sales | Read the request |
| Missing specifications, chased with the customer | Inside sales | Read the request |
| Prices, costs and terms per item | Pricing manager | Build the price |
| The account's bid history, gathered by hand | Inside sales | Bid or no-bid |

## Decide

| Requirement | By whom | Step |
| --- | --- | --- |
| Bid or no-bid, before pricing | Sales manager | Bid or no-bid |
| Every deviation reviewed and signed by an engineer | Application engineer | Deviation review |
| A discount above the limit approved | Sales manager | Approve discounts |

## Produce

| Requirement | By whom | Step |
| --- | --- | --- |
| The request typed again into the quoting worksheet | Inside sales | Read the request |
| Prices compared in a spreadsheet | Pricing manager | Build the price |
| A priced draft within the discount rules | Pricing manager | Build the price |
| A quote document from templates | Inside sales | Send and log |

## Do

| Requirement | By whom | Step |
| --- | --- | --- |
| The quote sent to the customer | Inside sales | Send and log |
| The quote logged in the ERP and the CRM | Inside sales | Send and log |

## Check

| Requirement | By whom | Step |
| --- | --- | --- |
| Margin checked against the floor on a sample | Pricing manager | Build the price |
| Margin checked once more before sending, in no procedure | Unknown, to confirm | Send and log |

**Next card**

- Question: "Does this match how the work really runs?"
- Options: "Yes, go to step 4: size the value (Recommended)", "Adjust the list first".
