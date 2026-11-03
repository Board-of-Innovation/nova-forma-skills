# Security

## Report a problem privately

Please don't open a public issue for a security problem. Report it privately through GitHub instead:

1. Open the **Security** tab of this repository.
2. Select **Report a vulnerability**.
3. Describe the problem, the skill and the assistant involved, and the steps to reproduce it. Use invented data, never real company or personal data.

Only the maintainers see your report. We confirm that we received it, keep you updated, and credit you when we publish the fix, unless you prefer not to be named. GitHub's guide [Privately reporting a security vulnerability](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately) shows the steps.

## What counts

- A skill instruction that could make the assistant read, reveal or send data from connected tools, such as email, team chat, documents or meeting notes, beyond what the user allowed.
- Prompt injection: text in a file, email or web page that a skill reads, and that can steer the assistant to act against the user.
- The value sizer's script, `skills/nova-forma-value-at-stake-sizer/scripts/value_case.py`: anything that makes it read or write files it should not, run other code, or reach the network.
- Release zips or plugin manifests that differ from the source in this repository.
- Secrets or personal data committed to this repository by mistake.

## What does not count

- Problems in Claude or another assistant itself. Report those to the company that makes it.
- A weak result or a wrong number. That is skill feedback: open an issue.

## Supported versions

Fixes go into the latest release only.

## Before you install

Skills are instructions your assistant follows. Install them only from this repository or its releases, and read a skill's `SKILL.md` before you turn it on.
