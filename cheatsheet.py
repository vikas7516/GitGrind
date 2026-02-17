"""
GitGrind — Cheat sheet generator (endgame reward).
Categorizes all learned commands and saves a formatted text file.
"""
import os


CHEATSHEET_FILE = os.path.join(os.path.dirname(__file__), "git_cheatsheet.txt")
MASTERY_REPORT_FILE = os.path.join(os.path.dirname(__file__), "git_mastery_report.txt")


# ── Category Map ─────────────────────────────────────────
# Maps taught commands to cheat sheet categories.
# Keys MUST exactly match the strings used in commands_taught
# arrays across all level files.

category_map = {
    # Setup & Configuration
    "git --version": "Setup & Configuration",
    "git config --global user.name": "Setup & Configuration",
    "git config --global user.email": "Setup & Configuration",
    "git config --list": "Setup & Configuration",
    # Basics
    "git init": "Basics",
    "git status": "Basics",
    # Staging & Committing
    "git add <file>": "Staging & Committing",
    "git add .": "Staging & Committing",
    "git commit -m": "Staging & Committing",
    "git commit --amend": "Staging & Committing",
    # .gitignore
    ".gitignore": ".gitignore",
    "git rm --cached": ".gitignore",
    # Viewing Changes & History
    "git diff": "Viewing Changes & History",
    "git diff --staged": "Viewing Changes & History",
    "git log": "Viewing Changes & History",
    "git log --oneline": "Viewing Changes & History",
    "git log --oneline --graph": "Viewing Changes & History",
    "git log --stat": "Viewing Changes & History",
    "git log --author": "Viewing Changes & History",
    "git log --since": "Viewing Changes & History",
    "git log --grep": "Viewing Changes & History",
    "git log --graph": "Viewing Changes & History",
    # Branching
    "git branch <name>": "Branching",
    "git branch": "Branching",
    "git branch -a": "Branching",
    "git branch -d <name>": "Branching",
    "git branch -r": "Branching",
    "git switch <branch>": "Branching",
    "git switch -c <name>": "Branching",
    "git checkout <branch>": "Branching",
    "git checkout -b <name>": "Branching",
    # Merging
    "git merge <branch>": "Merging",
    "conflict resolution": "Merging",
    # Note: "git add <file>" already mapped in Staging & Committing
    # Remotes
    "git remote add origin <url>": "Remotes",
    "git remote -v": "Remotes",
    "git remote set-url": "Remotes",
    "git clone <url>": "Remotes",
    "git push -u origin main": "Remotes",
    "git push": "Remotes",
    "git push origin <branch>": "Remotes",
    "git push origin --delete <branch>": "Remotes",
    "git fetch origin": "Remotes",
    "git fetch --prune": "Remotes",
    "git pull": "Remotes",
    "git pull origin main": "Remotes",
    # Undo & Restore
    "git restore <file>": "Undo & Restore",
    "git restore --staged <file>": "Undo & Restore",
    "git reset HEAD~1": "Undo & Restore",
    "git reset --soft HEAD~1": "Undo & Restore",
    "git reset --hard HEAD~1": "Undo & Restore",
    "git revert <hash>": "Undo & Restore",
    # Stash
    "git stash": "Stash",
    "git stash list": "Stash",
    "git stash pop": "Stash",
    "git stash apply": "Stash",
    "git stash drop": "Stash",
    # Reflog
    "git reflog": "Reflog",
    # Rebase
    "git rebase main": "Rebase",
    "git rebase -i HEAD~N": "Rebase",
    "git rebase --onto <newbase> <upstream> <branch>": "Rebase",
    "git rebase --continue": "Rebase",
    "git rebase --abort": "Rebase",
    # Pro Moves
    "git cherry-pick <hash>": "Pro Moves",
    "git tag v1.0": "Pro Moves",
    "git tag -a v1.0 -m 'msg'": "Pro Moves",
    "git blame <file>": "Pro Moves",
    "git push --force-with-lease": "Pro Moves",
    "git config --global alias.st status": "Pro Moves",
    # Maintenance & Team Flow
    "git show <hash>": "Maintenance & Team Flow",
    "git mv <old> <new>": "Maintenance & Team Flow",
    "git clean -fd": "Maintenance & Team Flow",
    "git branch -m <old> <new>": "Maintenance & Team Flow",
    "git grep <pattern>": "Maintenance & Team Flow",
    "git log --follow <file>": "Maintenance & Team Flow",
    "git diff <branch1>..<branch2>": "Maintenance & Team Flow",
    "git merge --squash <branch>": "Maintenance & Team Flow",
    "git bisect start|good|bad|reset": "Maintenance & Team Flow",
    ".git/info/exclude": "Maintenance & Team Flow",
    "pull request workflow": "Maintenance & Team Flow",
}


# Category display order
CATEGORY_ORDER = [
    "Setup & Configuration",
    "Basics",
    "Staging & Committing",
    ".gitignore",
    "Viewing Changes & History",
    "Branching",
    "Merging",
    "Remotes",
    "Undo & Restore",
    "Stash",
    "Reflog",
    "Rebase",
    "Pro Moves",
    "Maintenance & Team Flow",
]


def generate_cheatsheet(state):
    """Generate the cheat sheet reward file."""

    mastery = int(round(state.accuracy * 0.7 + state.first_try_accuracy * 0.3))
    if mastery >= 90:
        rank = "GitGrind Grandmaster"
    elif mastery >= 75:
        rank = "GitGrind Pro"
    elif mastery >= 60:
        rank = "GitGrind Practitioner"
    else:
        rank = "GitGrind Graduate"

    # Build categories from learned commands
    categories = {cat: [] for cat in CATEGORY_ORDER}
    categories["Other"] = []

    for cmd in state.data["commands_learned"]:
        cat = category_map.get(cmd, "Other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(cmd)

    # Build output
    lines = []
    lines.append("=" * 60)
    lines.append("  GIT CHEAT SHEET — Generated by GitGrind")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"  Rank:             {rank}")
    lines.append(f"  Mastery score:    {mastery}%")
    lines.append("")

    # Stats
    lines.append(f"  Accuracy:         {state.accuracy}%")
    lines.append(f"  First-Try:        {state.first_try_accuracy}%")
    lines.append(f"  Commands typed:   {state.total_commands_typed}")
    lines.append(f"  Hints used:       {state.hints_used}")
    lines.append(f"  Time played:      {state.time_played_display}")
    lines.append("")
    lines.append("-" * 60)

    for cat in CATEGORY_ORDER:
        cmds = categories.get(cat, [])
        if not cmds:
            continue
        lines.append("")
        lines.append(f"  📂 {cat.upper()}")
        lines.append(f"  {'─' * 40}")
        for cmd in cmds:
            lines.append(f"    {cmd}")

    # Show "Other" if any unmapped commands exist
    other_cmds = categories.get("Other", [])
    if other_cmds:
        lines.append("")
        lines.append("  📂 OTHER")
        lines.append(f"  {'─' * 40}")
        for cmd in other_cmds:
            lines.append(f"    {cmd}")

    lines.append("")
    lines.append("=" * 60)
    lines.append("  Keep grinding. You've got this. 🚀")
    lines.append("=" * 60)

    with open(CHEATSHEET_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("  GITGRIND MASTERY REPORT")
    report_lines.append("=" * 60)
    report_lines.append("")
    report_lines.append(f"  Final rank:        {rank}")
    report_lines.append(f"  Mastery score:     {mastery}%")
    report_lines.append(f"  Accuracy:          {state.accuracy}%")
    report_lines.append(f"  First-try:         {state.first_try_accuracy}%")
    report_lines.append(f"  Best streak:       {state.best_streak}")
    report_lines.append(f"  Commands learned:  {len(state.data['commands_learned'])}")
    report_lines.append(f"  Commands typed:    {state.total_commands_typed}")
    report_lines.append(f"  Hints used:        {state.hints_used}")
    report_lines.append(f"  Time played:       {state.time_played_display}")
    report_lines.append("")

    if mastery >= 90:
        report_lines.append("  Verdict: You can run day-to-day Git confidently without docs.")
    elif mastery >= 75:
        report_lines.append("  Verdict: Strong practical skill. Occasional docs for edge cases.")
    else:
        report_lines.append("  Verdict: Good foundation. Keep replaying retention rounds.")

    report_lines.append("")
    report_lines.append("  Recommended next practice:")
    report_lines.append("    1) Replay Round 6 and Round 7 once per week")
    report_lines.append("    2) Replay Boss Fight 6 until 2 clean wins in a row")
    report_lines.append("    3) Build one mini project using branch + PR + rebase flow")
    report_lines.append("")
    report_lines.append("=" * 60)

    with open(MASTERY_REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
