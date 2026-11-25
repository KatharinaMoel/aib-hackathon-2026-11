# Eval

<!-- How we measure the agent on Stackgini's labelled examples. The eval code is built on the day.
See docs/FILES.md. -->

Runs the agent on `data/labelled/` (git-ignored, event data) and wraps Stackgini's scoring script.
Empty on purpose: built on the day.

## Protocol (draft)

1. **Before any tuning**, put about 30 % of the labelled products aside as a hold-out, split evenly by label.
   Write the split to `data/holdout.txt`. Run the hold-out at most twice, the last time around 18:00.
2. Tune only on the other 70 %. Every prompt change names a **signal**, never a product.
3. Report two numbers separately: **hollow called solid** and **solid called hollow**. We try to bring both
   down, not only one (README, "Our goal").
4. Also report: share of `evidence_strength: thin` verdicts, and share of reasons that are verified and
   independent.
5. Small set: with about 10 hold-out products, one error moves the score by 10 points. Do not chase one product.
6. The labelled products are real, so the model may already know them. The judge gets only our verified facts,
   never the product name alone.

Command: `…` (set on the day; it goes into `AGENTS.md`, "Stack and commands").
