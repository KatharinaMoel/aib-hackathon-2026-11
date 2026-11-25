# Eval

<!-- How we measure the agent on Stackgini's labelled examples. The eval code is built on the day.
See docs/FILES.md. -->

Runs the agent on `data/labelled/` (git-ignored, event data) and wraps Stackgini's scoring script.
Empty on purpose: built on the day.

## Protocol (draft)

1. **Read Stackgini's reasons first.** They show how the judges think. Put a few labelled examples, with their
   reasons, into the judge prompt as examples.
2. **Hold-out depends on the size.** 20 or more labelled products: before any tuning, put about 30 % aside,
   split evenly by label (`data/holdout.txt`), run it at most twice. Fewer than 20: use all of them as examples
   and as a regression check – a change must not add a new mistake.
3. Every prompt change names a **signal**, never a product.
4. Report two numbers separately: **hollow called solid** and **solid called hollow**. We try to bring both
   down, not only one (README, "Our goal").
5. Also report: share of `evidence_strength: thin` verdicts, and share of reasons that are verified and
   independent.
6. Small set: with about 10 hold-out products, one error moves the score by 10 points. Do not chase one product.
7. The labelled products are real, so the model may already know them. The judge gets only our verified facts,
   never the product name alone.

Command: `…` (set on the day; it goes into `AGENTS.md`, "Stack and commands").
