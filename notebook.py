"""
GitGrind — Notebook system.
Progressive reference of all commands learned during gameplay.
Can be viewed in-game or exported as a .txt file.
"""
import os


NOTEBOOK_FILE = os.path.join(os.path.dirname(__file__), "git_notebook.txt")


# ── Category Map ─────────────────────────────────────────
# Maps taught commands to notebook categories.
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


def generate_notebook_txt(state):
    """
    Save the notebook entries to a formatted .txt file.
    Returns the path to the saved file, or None if notebook is empty.
    """
    entries = state.notebook_entries
    if not entries:
        return None

    # Group by category
    categorized = {cat: [] for cat in CATEGORY_ORDER}
    categorized["Other"] = []

    for cmd, data in entries.items():
        cat = category_map.get(cmd, "Other")
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append((cmd, data))

    lines = []
    lines.append("=" * 60)
    lines.append("  GIT NOTEBOOK — Generated by GitGrind")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"  Commands learned: {len(entries)}")
    lines.append("")
    lines.append("-" * 60)

    for cat in CATEGORY_ORDER + ["Other"]:
        cmds = categorized.get(cat, [])
        if not cmds:
            continue

        lines.append("")
        lines.append(f"  📂 {cat.upper()}")
        lines.append(f"  {'─' * 50}")

        for cmd, data in cmds:
            lines.append("")
            lines.append(f"    ▸ {cmd}")
            if data.get("syntax"):
                lines.append(f"      Syntax: {data['syntax']}")
            if data.get("explanation"):
                for eline in data["explanation"].strip().split("\n"):
                    lines.append(f"      {eline}")
            if data.get("pro_tip"):
                lines.append(f"      💡 Tip: {data['pro_tip']}")

    lines.append("")
    lines.append("=" * 60)
    lines.append("  Keep grinding. You've got this. 🚀")
    lines.append("=" * 60)

    with open(NOTEBOOK_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return NOTEBOOK_FILE
