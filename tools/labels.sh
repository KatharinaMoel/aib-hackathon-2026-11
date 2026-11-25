#!/usr/bin/env bash
# Create the six labels from CONTRIBUTING.md, section 5. Run once: tools/labels.sh
# Needs `gh` logged in with write access. --force updates a label that already exists.
set -euo pipefail
R="${1:-KatharinaMoel/aib-hackathon-2026-11}"
echo "Creating labels in $R"
gh label create task           -R "$R" --force -c 1d76db -d "Issue: one piece of work, one PR"
gh label create needs-review   -R "$R" --force -c 0e8a16 -d "PR ready; a reviewer is next"
gh label create author-turn    -R "$R" --force -c fbca04 -d "Bug: or Question: open; author acts, then re-requests review"
gh label create second-opinion -R "$R" --force -c d93f0b -d "Touches fetched text, keys, shell or network; view A by a person"
gh label create blocked        -R "$R" --force -c b60205 -d "Waits for a decision; the comment says from whom"
gh label create norma          -R "$R" --force -c 5319e7 -d "Has a Norma finding to fix, accept or log as conflict"
echo "Done: 6 labels."
