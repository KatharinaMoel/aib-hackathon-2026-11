#!/usr/bin/env bash
# Create the four labels from CONTRIBUTING.md, section 5. Run once: tools/labels.sh
# Needs `gh` logged in with write access. --force updates a label that already exists.
# The issue forms and the review flow use these labels. See docs/FILES.md.
set -euo pipefail  # stop at the first failing command
# Repo as owner/name; default is this repo. Another repo: tools/labels.sh <owner>/<name>
R="${1:-KatharinaMoel/aib-hackathon-2026-11}"
echo "Creating labels in $R"
gh label create task           -R "$R" --force -c 1d76db -d "Issue: one piece of work, one PR"
gh label create second-opinion -R "$R" --force -c d93f0b -d "Touches fetched text, keys, shell or network; adds review view B"
gh label create norma          -R "$R" --force -c 5319e7 -d "Fixes, accepts or causes a Norma finding; adds review view B"
gh label create hotfix         -R "$R" --force -c b60205 -d "Emergency mode only (docs/TEAM.md): fewer blocks, view A only"
echo "Done: 4 labels."
