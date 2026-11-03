# Nova Forma skills

Four AI skills that take one workflow from "where do we start with AI?" to a one-page brief for its redesign.

## What this is

Nova Forma is an AI-first redesign of one workflow, done with your team in one week. These four skills are its intake. They prepare one workflow for the redesign week, step by step, in a normal conversation with Claude. At each step Claude asks a few questions, suggests an answer for each and draws on your files where you allow it. You end with a one-page brief.

A skill is a set of written instructions that Claude follows when your request matches it. These skills are plain text files plus one small calculation script. You don't need to write any code.

**Who it is for:** teams starting a Nova Forma redesign. Anyone else may use the skills too, free of charge.

## The four steps

Run them in order. Each step builds on the result of the one before.

| Step | Skill | What you get |
| --- | --- | --- |
| 1. Pick the workflow | `nova-forma-workflow-identifier` | A ranked shortlist of workflows worth redesigning, your pick, and a scope card that fixes where it starts and ends |
| 2. Define success | `nova-forma-outcome-statement-writer` | One sentence on who gets what result, with three to six measures and the rules the new way of working may never break |
| 3. Map today's work | `nova-forma-requirements-lister` | Every requirement the workflow follows today, who owns it and where it shows up, plus the cases that leave the normal path |
| 4. Size the value | `nova-forma-value-at-stake-sizer` | A value range a year, low to high, with every assumption visible, then the one-page brief for the redesign week |

## Install

### In Claude (web or desktop)

This is the recommended way. It adds all four skills at once and keeps them up to date.

1. Open [Customize > Plugins](https://claude.ai/customize/plugins) in Claude.
2. Select **Add**, then **Add marketplace**.
3. Paste `Board-of-Innovation/nova-forma-skills` and confirm.
4. Find the Nova Forma plugin in the list and select **Add**.

The four skills now appear under **Customize > Skills**. They also work in Cowork, and in Claude Code when you sign in with the same account. To get a newer version, select **Check for updates**, or turn on **Sync automatically**.

<details>
<summary><b>Upload the skills one by one</b></summary>

<br>

Use this when your organization doesn't let you add a marketplace, or when you want only some of the skills.

1. Download each skill you want from the [latest release](https://github.com/Board-of-Innovation/nova-forma-skills/releases/latest):
   - [nova-forma-workflow-identifier.zip](https://github.com/Board-of-Innovation/nova-forma-skills/releases/latest/download/nova-forma-workflow-identifier.zip)
   - [nova-forma-outcome-statement-writer.zip](https://github.com/Board-of-Innovation/nova-forma-skills/releases/latest/download/nova-forma-outcome-statement-writer.zip)
   - [nova-forma-requirements-lister.zip](https://github.com/Board-of-Innovation/nova-forma-skills/releases/latest/download/nova-forma-requirements-lister.zip)
   - [nova-forma-value-at-stake-sizer.zip](https://github.com/Board-of-Innovation/nova-forma-skills/releases/latest/download/nova-forma-value-at-stake-sizer.zip)
2. Open [Customize > Skills](https://claude.ai/customize/skills) in Claude, select **+**, then **Create skill**, then **Upload a skill**.
3. Choose the zip file. Repeat for each skill, then turn each one on.

Upload the zip file as it is. If your browser unzipped it, compress the folder again before you upload it.

Uploaded skills don't update themselves. For a new version, download and upload them again.

</details>

<details>
<summary><b>Claude Code</b></summary>

<br>

Run these two commands in Claude Code:

```
/plugin marketplace add Board-of-Innovation/nova-forma-skills
/plugin install nova-forma@nova-forma-skills
```

Describe what you need, or start a step by name, such as `/nova-forma:nova-forma-workflow-identifier`. If you already added the plugin in Claude on the web, it is there when you sign in with the same account.

</details>

<details>
<summary><b>Other assistants that support Agent Skills</b></summary>

<br>

The skills follow the open [Agent Skills](https://agentskills.io) standard, so they also work in Codex, Cursor, Gemini CLI, GitHub Copilot and other assistants. With [Node.js](https://nodejs.org) installed, run:

```
npx skills add Board-of-Innovation/nova-forma-skills
```

It asks which skills to install and for which assistants. The value sizer runs a small Python 3 script, so your assistant needs to be able to run Python.

</details>

<details>
<summary><b>For Team and Enterprise admins</b></summary>

<br>

An Owner can give the skills to the whole organization. Go to **Organization settings > Plugins & skills**, select **Add**, then **Upload a skill**, and upload each of the four zip files from the [latest release](https://github.com/Board-of-Innovation/nova-forma-skills/releases/latest). Then choose who gets them. [Manage plugins for your organization](https://claude.com/docs/plugins/admin) has the details.

Members also need **Code execution and file creation** turned on under **Organization settings > Capabilities**. To add the marketplace themselves, they need **User-created skills** turned on under **Organization settings > Plugins & skills > Policy**.

</details>

## What you need

- A paid Claude plan: Pro, Max, Ultra, Team or Enterprise.
- Code execution switched on: in [Settings > Capabilities](https://claude.ai/settings/capabilities), turn on **Code execution and file creation**. On Team and Enterprise plans, an Owner turns it on for the organization.
- The skills work best with your meeting notes, documents and team chat connected to Claude. They tell you which of these they can reach, you decide which ones they may use, and they work from your answers when nothing is connected.

## Get started

Open a new chat and say what you need. Claude picks the right skill. For example:

- "Where should we start with AI in our sales team?"
- "Which process in our finance team should we redesign first?"
- "Help us define what success looks like for how we turn customer requests into quotes."
- "What would redesigning our invoice handling with AI be worth?"

To choose a skill yourself, type `/` in the message box and pick it. Each step asks its questions with a suggested answer, as cards where your app can show them, so you can click through or type your own. At the end of each step, accept the result and Claude moves on to the next one. After step 4, Claude offers to put all four results on one page.

## Your data

- The skills run inside your assistant. Nothing is sent to Board of Innovation, and the skills contain no tracking.
- They draw on what you write, the files you attach and, where your assistant has them, your earlier chats and connected tools. A result that used more than the conversation ends with a line naming its sources, and you can tell the skills which sources to leave out.
- The value sizer's script only does arithmetic. It runs in your assistant's own code environment, reads only the numbers it is given and makes no network calls.
- Your assistant's provider handles your conversation under your plan's terms, as with any other chat.
- Every estimate is marked as a hypothesis. Check names and numbers before you share a result.

## FAQ

**Do I need all four skills?**
For the one-page brief, yes. Each step uses the result of the one before.

**Can I run one step on its own?**
Yes. When the result of an earlier step is missing, the skill asks the one question it needs, such as which workflow to work on, and carries on.

**Can I change the skills?**
Yes. They are plain text files you can edit, under the Apache 2.0 license. Edit a copy and upload your version. If you share it, give it your own name, as the [License](#license) section explains.

**Which languages do they work in?**
The skills are written in English. Claude usually replies in the language you write in, so you can work in your own. Check the wording of the result before you share it.

**Is it free?**
Yes. The skills are free and open source. You only need your own Claude plan.

## Contributing

Feedback and fixes are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) first: this repository is public, so never paste confidential company data into an issue. Report security problems as [SECURITY.md](SECURITY.md) describes. Everyone who takes part follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

The skills are licensed under the [Apache License 2.0](LICENSE): you may use, change and share them, also for commercial work. Keep the license and the [NOTICE](NOTICE) file with any copy, and mark the files you change. Copyright 2026 Board of Innovation BV.

**Names and logos.** The license grants no rights to the Nova Forma or Board of Innovation names or logos (section 6 of the license). You may say that your work is based on the Nova Forma skills. A changed version should carry its own name and should not present itself as the official Nova Forma skills.

**Sources.** The skills cite published research. Those sources belong to their publishers. The license covers this repository's own text and code.

## Acknowledgements

The writing rules draw on David Ogilvy's 1982 memo "How to Write" and on "Writing That Works" by Kenneth Roman and Joel Raphaelson. The list of signs of machine-made writing draws on the [humanizer](https://github.com/blader/humanizer) skill and Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

## About

Nova Forma is an offering by Board of Innovation. In one week, it redesigns one of your workflows around AI, together with your team. Read more at [novaforma.ai](https://novaforma.ai).
