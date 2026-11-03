# Use what is already known, and say so

Read before you ask. Look in this order and stop when you have enough:

1. This conversation, including the result of the previous Nova Forma step.
2. Attached files and project documents.
3. What this assistant remembers about the user: memory and earlier chats, where available.
4. The tools the user has connected, such as meeting notes, email, calendar, team chat, documents or a CRM. Name each one you can reach.

## Tell the user what you can use

Users new to AI often do not know that the assistant can draw on their earlier chats and connected tools. Tell them plainly, the first time it matters, in two sentences at most, and name the actual tools:

> I can look through what this assistant already knows about your work: our earlier chats and the tools you have connected, here Granola, Slack and Google Drive. You decide which of these I may use.

When there is nothing to draw on, say so just as plainly and start from the standard map of workflows in the workflow identifier:

> I have no earlier chats or connected tools to look at, so I'll start from the workflows most companies run, and you steer.

## Rules

- Use only what the environment exposes, and only the sources the user allowed.
- Keep personal details to the names of owners and sponsors. Never quote private messages back at length.
- When you used more than this conversation, close the result with one line naming the sources, such as "Sources: Granola meeting notes, August to October."
- When the result of an earlier Nova Forma step is missing, say so in one line and ask its core question, such as "Which workflow should we work on, from what start to what end?" Ask it as a card when the context suggests two to four candidates, with the likeliest first; otherwise ask it in plain text. Never refuse to run.
