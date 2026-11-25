# Proposals – a menu, not rules

These practices worked for me (Katharina) in longer projects. We use one only if the team agrees at the start.
Cross out what we don't want – that is a fine result too.

What they aim at: say what you did and what you checked; a reader can follow why; write for the next person
who opens it; keep it simple.

## 1.–2. Comments and labels

Now part of `CONTRIBUTING.md` (sections 4 and 5). Change them there by PR.

---

**Background – not needed today.**

## 3. Asking for a second view

Ask a second person or a separate agent session. Give it one question and the goal, not your preferred answer;
otherwise it tends to agree with you.

| View | Ask when … | Question |
|---|---|---|
| Devil's advocate | a plan feels obviously right | What is wrong with this? Find a counter-example. |
| Simplicity | something grew big | What can we remove or merge? Can a newcomer use it after 10 minutes? |
| Security | fetched text, keys, shell or network calls | Which outside text could steer the agent? Where are the keys? |
| Reader | agent output or README changes | Is it clear and short for someone who sees it first? |
| Communication | a review comment, the pitch | How does this land with the receiver? Does it say what to do next? |
| Judge | from 18:00 | Does the brief reward this? Which work will the judges not see? |

## 4. Why no AI reviewer in GitHub Actions

It needs an API key in the repo secrets, and "any user with write access to your repository has read access to
all secrets configured in your repository"
([GitHub docs](https://docs.github.com/en/actions/reference/security/secure-use); wording checked by a research
agent, not by me). Norma's GitHub App already checks every PR. If we want an AI reviewer anyway: a throwaway key
with a spending limit, and a human still approves.

## 5. Docs and config

- Config outside the code: commit `.env.example` with one comment per line; the real `.env` stays local.
- Docs in layers: README (what, how to run, one example) → GUIDE (worked example) → DESIGN (why, decisions,
  limits). Today: README only.
- One real sample output with links instead of a paragraph about it.
- Scripts print what they are about to do before they do it (see `tools/check`).

## 6. Don'ts for AI-assisted team work, with sources

| Don't | Instead | Source |
|---|---|---|
| Let a personal rule file hide the shared one | In Claude Code, any `CLAUDE.md` stops `AGENTS.md` from loading unless it imports it | [Claude Code: memory](https://code.claude.com/docs/en/memory) |
| Write vague rules ("write clean code") | Rules with commands, paths, names | same; [Cursor: rules](https://cursor.com/docs/context/rules) |
| Rely on text for "never" rules | Deny rules in `.claude/settings.json`, checks in CI | [Claude Code: best practices](https://code.claude.com/docs/en/best-practices) |
| Let every agent write its own helpers | Search first; one owner per shared module | [GitClear 2025 report](https://www.gitclear.com/ai_assistant_code_quality_2025_research) (vendor report, not peer-reviewed) |
| Trust AI code on input, network or shell because it looks sure | A person reads those diffs | [Perry et al. 2022, arXiv 2211.03622](https://arxiv.org/abs/2211.03622) (older models) |
| Open big mixed PRs | One self-contained change per PR | [Google: small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) |
| Let two agents edit the same checkout | One branch (or worktree) per person and task | [Claude Code: best practices](https://code.claude.com/docs/en/best-practices) |
| Assume branch protection also covers admins | Turn on "Do not allow bypassing the above settings" | [GitHub: protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) |
| Decide in private messages | Decide in the team channel; one line in `DECISIONS.md` | [opensource.guide](https://opensource.guide/best-practices/) |

| Bad task for an agent | Good task |
|---|---|
| "Add a search tool." | "Add `search` in `src/tools/search.py`, like `src/tools/fetch.py`. Done when `pytest tests/test_search.py` passes. Change no other file." |
