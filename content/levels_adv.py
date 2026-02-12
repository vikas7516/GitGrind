"""
GitGrind — Levels 15-20: Advanced (Undo, Stash, Reflog, Rebase, Pro Moves).
"""
from content.models import Exercise, Level, Teaching


# ═══════════════════════════════════════════════════════════
#  LEVEL 15 — Restore & Reset
# ═══════════════════════════════════════════════════════════

LEVEL_15 = Level(
    number=15,
    name="Restore & Reset",
    tagline="Discard changes and undo commits.",
    concept=(
        "git restore <file> discards changes in your working directory.\n"
        "git restore --staged <file> unstages a file (keeps changes).\n"
        "git reset HEAD~1 undoes the last commit. --soft keeps staged, --hard deletes everything."
    ),
    commands_taught=["git restore <file>", "git restore --staged <file>",
                     "git reset HEAD~1", "git reset --soft HEAD~1", "git reset --hard HEAD~1"],
    teachings=[
        Teaching(
            command="git restore <file>",
            syntax="git restore <filename>",
            explanation=(
                "Made a mess of a file and want to go back to how it was at the last commit?\n"
                "This command discards ALL changes in that file, restoring it to its last\n"
                "committed state.\n"
                "\n"
                "WARNING: This is destructive! Your edits are gone permanently."
            ),
            example_output=(
                "$ git status\n"
                "Changes not staged for commit:\n"
                "  modified:   app.py\n"
                "\n"
                "$ git restore app.py\n"
                "\n"
                "$ git status\n"
                "nothing to commit, working tree clean"
            ),
            pro_tip="If you want to restore ALL files, use 'git restore .' — but be very sure you want to lose everything.",
        ),
        Teaching(
            command="git restore --staged <file>",
            syntax="git restore --staged <filename>",
            explanation=(
                "Accidentally staged a file with 'git add' and want to unstage it?\n"
                "This command removes the file from the staging area, but keeps your\n"
                "changes in the working directory. Nothing is lost — the file just\n"
                "moves from 'staged' back to 'modified'."
            ),
            example_output=(
                "$ git status\n"
                "Changes to be committed:\n"
                "  modified:   app.py    ← oops, didn't mean to stage this\n"
                "\n"
                "$ git restore --staged app.py\n"
                "\n"
                "$ git status\n"
                "Changes not staged for commit:\n"
                "  modified:   app.py    ← still modified, just not staged"
            ),
        ),
        Teaching(
            command="git reset HEAD~1",
            syntax="git reset HEAD~N",
            explanation=(
                "This undoes the last N commits. What happens to the changes depends on the flag:\n"
                "\n"
                "  git reset HEAD~1          (default/--mixed)\n"
                "    → Removes the commit\n"
                "    → Changes go back to working directory (unstaged)\n"
                "\n"
                "HEAD~1 means 'one commit before HEAD'. HEAD~3 means '3 commits back'."
            ),
            example_output=(
                "$ git log --oneline\n"
                "abc1234 (HEAD -> main) add feature\n"
                "def5678 initial commit\n"
                "\n"
                "$ git reset HEAD~1\n"
                "Unstaged changes after reset:\n"
                "M  app.py\n"
                "\n"
                "$ git log --oneline\n"
                "def5678 (HEAD -> main) initial commit"
            ),
        ),
        Teaching(
            command="git reset --soft HEAD~1",
            syntax="git reset --soft HEAD~1",
            explanation=(
                "Undoes the last commit but keeps all changes STAGED.\n"
                "This is perfect when you committed too early and want to add more\n"
                "changes or fix the commit message before re-committing.\n"
                "\n"
                "The difference from default reset: changes stay in staging area,\n"
                "ready to be committed again immediately."
            ),
            example_output=(
                "$ git reset --soft HEAD~1\n"
                "\n"
                "$ git status\n"
                "Changes to be committed:\n"
                "  modified:   app.py   ← still staged, ready to re-commit"
            ),
            pro_tip="Use --soft when you just want to redo a commit. Use default (--mixed) when you want to restage differently.",
        ),
        Teaching(
            command="git reset --hard HEAD~1",
            syntax="git reset --hard HEAD~1",
            explanation=(
                "DANGER ZONE! This undoes the last commit AND permanently deletes\n"
                "all changes. The code is gone. The commit is gone.\n"
                "\n"
                "Only use this when you are absolutely sure you want to destroy work.\n"
                "If you do this by accident, 'git reflog' might save you (Level 18)."
            ),
            example_output=(
                "$ git reset --hard HEAD~1\n"
                "HEAD is now at def5678 initial commit\n"
                "\n"
                "$ git status\n"
                "nothing to commit, working tree clean\n"
                "# The commit and all its changes are GONE"
            ),
            pro_tip="If you accidentally --hard reset, use 'git reflog' to find the lost commit hash and 'git reset --hard <hash>' to recover.",
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="Discard all changes in 'app.py' (restore it to last committed version).",
            answers=["git restore app.py"],
            explanation="'git restore <file>' throws away ALL uncommitted changes in that file. It's gone forever—there's no undo! Use when you've made a mess and want to start over.",
            sim_output="$ git restore app.py\n(file restored to last committed state)",
        ),
        Exercise(
            type="recall",
            prompt="Unstage 'app.py' (remove from staging area, keep the changes in working directory).",
            answers=["git restore --staged app.py"],
            explanation="'git restore --staged <file>' is the opposite of 'git add'. It unstages the file but keeps your changes. Use this to un-stage something you added by mistake.",
            sim_output="$ git restore --staged app.py\n(file unstaged, changes still in working directory)",
        ),
        Exercise(
            type="recall",
            prompt="Undo the last commit but keep changes staged (ready to re-commit).",
            answers=["git reset --soft HEAD~1"],
            explanation="--soft undoes the commit but leaves everything staged. Perfect for when you want to amend/redo a commit. Just edit and commit again.",
            sim_output="$ git reset --soft HEAD~1\n(last commit undone, changes still staged)",
        ),
        Exercise(
            type="recall",
            prompt="Undo the last commit and unstage changes (keep in working directory).",
            answers=["git reset HEAD~1", "git reset --mixed HEAD~1"],
            explanation="Default reset (--mixed) undoes the commit and unstages changes. The code still exists as modifications. Use this to rework what goes into a commit.",
            sim_output="$ git reset HEAD~1\nUnstaged changes after reset:\nM  app.py",
        ),
        Exercise(
            type="recall",
            prompt="Completely destroy the last commit AND all its changes (DANGEROUS!).",
            answers=["git reset --hard HEAD~1"],
            explanation="--hard deletes everything: the commit AND your changes. It's permanent destruction. Only use when you're 100% sure you want to lose that work.",
            sim_output="$ git reset --hard HEAD~1\nHEAD is now at abc1234 previous commit",
        ),
        Exercise(
            type="multi_choice",
            prompt="git reset --soft HEAD~1 does what?",
            answers=["c"],
            explanation="--soft keeps changes staged, ready to commit again. --mixed (default) keeps changes unstaged. --hard deletes everything. Know the difference!",
            choices=["a) Deletes the commit and all changes", "b) Keeps changes in working directory (unstaged)", "c) Keeps changes staged (ready to re-commit)"],
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Discard changes in 'server.js'.", answers=["git restore server.js"],
                 explanation="This permanently throws away your edits. Make sure you really want to lose them!"),
        Exercise(type="recall", prompt="Unstage 'config.py'.", answers=["git restore --staged config.py"],
                 explanation="Moves the file from staged back to modified. Your changes are safe."),
        Exercise(type="recall", prompt="Undo last commit, keep staged.", answers=["git reset --soft HEAD~1"],
                 explanation="Great for fixing commit messages or adding forgotten files before re-committing."),
        Exercise(type="recall", prompt="Undo last commit, keep in working dir.", answers=["git reset HEAD~1"],
                 explanation="The default reset mode. Changes become unstaged modifications."),
        Exercise(type="recall", prompt="Nuke last commit entirely.", answers=["git reset --hard HEAD~1"],
                 explanation="Nuclear option. Everything is deleted. Use reflog if you regret this."),
        Exercise(type="recall", prompt="Discard changes in 'index.html'.", answers=["git restore index.html"],
                 explanation="Restores the file to its last committed state. Unsaved edits are lost."),
        Exercise(type="recall", prompt="Remove 'main.py' from staging.", answers=["git restore --staged main.py"],
                 explanation="Oops, didn't mean to stage that? This fixes it without losing your changes."),
        Exercise(type="recall", prompt="Soft reset — undo commit, keep staged.", answers=["git reset --soft HEAD~1"],
                 explanation="The gentlest reset. Commit goes away but work stays ready to commit."),
        Exercise(type="recall", prompt="Hard reset — destroy last commit.", answers=["git reset --hard HEAD~1"],
                 explanation="Commits and changes vanish. Reflog is your only hope if you made a mistake."),
        Exercise(type="recall", prompt="Undo last commit (default/mixed).", answers=["git reset HEAD~1"],
                 explanation="Changes exist but are unstaged. You can git add selectively before re-committing."),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 16 — Revert
# ═══════════════════════════════════════════════════════════

LEVEL_16 = Level(
    number=16,
    name="Revert",
    tagline="Safe undo for shared history.",
    concept=(
        "git revert <hash> creates a NEW commit that undoes a previous one.\n"
        "Unlike reset, it doesn't erase history — safe for shared branches.\n"
        "Use revert on main/shared branches. Use reset on local-only work."
    ),
    commands_taught=["git revert <hash>"],
    teachings=[
        Teaching(
            command="git revert <hash>",
            syntax="git revert <commit-hash>",
            explanation=(
                "What if you pushed a bad commit and your teammates already pulled it?\n"
                "You can't use 'git reset' because that rewrites history — it would break\n"
                "everyone else's repos.\n"
                "\n"
                "Instead, 'git revert' creates a BRAND NEW commit that does the OPPOSITE\n"
                "of the bad commit. It undoes the changes without erasing history.\n"
                "\n"
                "Think of it like this:\n"
                "  • reset  = pretend the commit never happened (rewrites history)\n"
                "  • revert = add a new commit that cancels out the bad one (safe)"
            ),
            example_output=(
                "$ git log --oneline\n"
                "abc1234 (HEAD -> main) add broken feature   ← this is the bad one\n"
                "def5678 fix navbar\n"
                "ghi9012 initial commit\n"
                "\n"
                "$ git revert abc1234\n"
                '[main xyz9876] Revert "add broken feature"\n'
                " 1 file changed, 0 insertions(+), 5 deletions(-)\n"
                "\n"
                "$ git log --oneline\n"
                'xyz9876 (HEAD -> main) Revert "add broken feature"   ← new undo commit\n'
                "abc1234 add broken feature\n"
                "def5678 fix navbar\n"
                "ghi9012 initial commit"
            ),
            pro_tip="Rule of thumb: use 'revert' for pushed commits, 'reset' for unpushed/local commits.",
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="Safely undo commit abc1234 (create a new commit that reverses it).",
            answers=["git revert abc1234"],
            explanation="'git revert <hash>' creates a new commit that undoes an old one. History stays intact—safe for shared branches. Get the hash from 'git log'.",
            sim_output='$ git revert abc1234\n[main xyz9876] Revert "add broken feature"\n 1 file changed, 0 insertions(+), 5 deletions(-)',
        ),
        Exercise(
            type="scenario",
            prompt="You committed a bug to 'main'. Your teammates already pulled it. What command safely undoes it without rewriting history?",
            answers=["git revert <hash>", "git revert abc1234"],
            hint="revert, not reset — because others already have the commit",
            explanation="Since teammates have the commit, you can't use reset (rewrites history). Revert adds a new commit that cancels the bad one—everyone can pull this safely.",
        ),
        Exercise(
            type="multi_choice",
            prompt="When should you use 'git revert' instead of 'git reset'?",
            answers=["b"],
            explanation="Use revert when commits are pushed/shared. Revert is safe because it doesn't rewrite history. Reset is only for local, unpushed commits.",
            choices=["a) When you want to delete history", "b) When the commit is on a shared/pushed branch", "c) When you want to unstage files"],
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Revert commit def5678.", answers=["git revert def5678"],
                 explanation="Copy the hash from 'git log --oneline' and revert it. Git will open an editor for the revert commit message."),
        Exercise(type="recall", prompt="Safely undo commit abc1234.", answers=["git revert abc1234"],
                 explanation="Revert is the safe undo for production/main branches. Reset would break everyone else's repos."),
        Exercise(type="recall", prompt="Revert commit ghi9012.", answers=["git revert ghi9012"],
                 explanation="The reverted commit stays in history—you can see both the original and the revert."),
        Exercise(type="recall", prompt="Create an undo commit for xyz7890.", answers=["git revert xyz7890"],
                 explanation="Revert literally creates the opposite changes: lines that were added get deleted, deleted lines get added back."),
        Exercise(type="recall", prompt="Safely reverse commit aaa1111.", answers=["git revert aaa1111"],
                 explanation="If the revert causes conflicts, resolve them like any merge conflict: edit, add, commit."),
        Exercise(type="recall", prompt="Revert commit bbb2222.", answers=["git revert bbb2222"],
                 explanation="You can revert ANY commit, not just the most recent one. But older reverts can cause conflicts."),
        Exercise(type="recall", prompt="Undo a pushed commit safely.", answers=["git revert <hash>", "git revert abc1234"],
                 explanation="Pushed = shared. Revert is the only safe undo for pushed work."),
        Exercise(type="recall", prompt="Revert commit ccc3333.", answers=["git revert ccc3333"],
                 explanation="After reverting, push the revert commit so others get the fix."),
        Exercise(type="recall", prompt="Safe undo for commit ddd4444.", answers=["git revert ddd4444"],
                 explanation="Revert won't delete anything permanently. If you revert a revert, you get the original changes back!"),
        Exercise(type="recall", prompt="Revert commit eee5555.", answers=["git revert eee5555"],
                 explanation="Professional teams use revert on main branches. Reset is for personal/feature branches only."),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 17 — Stash
# ═══════════════════════════════════════════════════════════

LEVEL_17 = Level(
    number=17,
    name="Stash",
    tagline="Shelve unfinished work temporarily.",
    concept=(
        "git stash saves your uncommitted changes and cleans working directory.\n"
        "git stash pop brings them back and removes from stash.\n"
        "git stash apply brings them back but KEEPS them in stash."
    ),
    commands_taught=["git stash", "git stash list", "git stash pop", "git stash apply", "git stash drop"],
    teachings=[
        Teaching(
            command="git stash",
            syntax="git stash",
            explanation=(
                "Imagine you're halfway through coding a feature and suddenly need to\n"
                "switch branches for an urgent bug fix. You can't commit half-finished code,\n"
                "and you can't switch with uncommitted changes.\n"
                "\n"
                "'git stash' saves all your uncommitted work into a temporary storage area\n"
                "and gives you a clean working directory. It's like putting your work on\n"
                "a shelf to come back to later."
            ),
            example_output=(
                "$ git status\n"
                "Changes not staged for commit:\n"
                "  modified:   app.py\n"
                "\n"
                "$ git stash\n"
                "Saved working directory and index state WIP on main: abc1234 latest commit\n"
                "\n"
                "$ git status\n"
                "nothing to commit, working tree clean\n"
                "# Your changes are saved in the stash!"
            ),
        ),
        Teaching(
            command="git stash list",
            syntax="git stash list",
            explanation=(
                "Shows all your stashed changes. Each entry has a stash ID like stash@{0}.\n"
                "The most recent stash is at stash@{0}. You can have multiple stashes."
            ),
            example_output=(
                "$ git stash list\n"
                "stash@{0}: WIP on main: abc1234 fix navbar\n"
                "stash@{1}: WIP on feature: def5678 add login"
            ),
        ),
        Teaching(
            command="git stash pop",
            syntax="git stash pop",
            explanation=(
                "Takes the most recent stash (stash@{0}), applies the changes back to your\n"
                "working directory, AND removes it from the stash list.\n"
                "\n"
                "This is the most common way to get your stashed work back."
            ),
            example_output=(
                "$ git stash pop\n"
                "On branch main\n"
                "Changes not staged for commit:\n"
                "  modified:   app.py\n"
                "\n"
                "Dropped refs/stash@{0}"
            ),
            pro_tip="If popping causes a conflict, resolve it like a merge conflict. The stash won't be dropped until you fix it.",
        ),
        Teaching(
            command="git stash apply",
            syntax="git stash apply",
            explanation=(
                "Like 'pop', but keeps the stash entry in the list. Useful when you want\n"
                "to apply the same stash to multiple branches."
            ),
            example_output=(
                "$ git stash apply\n"
                "On branch main\n"
                "Changes not staged for commit:\n"
                "  modified:   app.py\n"
                "# The stash is still in 'git stash list'"
            ),
        ),
        Teaching(
            command="git stash drop",
            syntax="git stash drop",
            explanation=(
                "Deletes the most recent stash entry without applying it.\n"
                "Use this to clean up old stashes you no longer need."
            ),
            example_output=(
                "$ git stash drop\n"
                "Dropped refs/stash@{0} (abc123...)"
            ),
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="Save your current uncommitted changes temporarily.",
            answers=["git stash"],
            explanation="'git stash' puts your uncommitted work on a shelf. Your directory becomes clean so you can switch branches safely. Get it back later with 'pop' or 'apply'.",
            sim_output="$ git stash\nSaved working directory and index state WIP on main: abc1234 latest commit",
        ),
        Exercise(
            type="recall",
            prompt="List all your stashed changes.",
            answers=["git stash list"],
            explanation="Shows all stashes. stash@{0} is the newest. You can have multiple stashes—useful when juggling several tasks.",
            sim_output="$ git stash list\nstash@{0}: WIP on main: abc1234 latest commit\nstash@{1}: WIP on feature: def5678 add login",
        ),
        Exercise(
            type="recall",
            prompt="Bring back stashed changes and remove them from the stash.",
            answers=["git stash pop"],
            explanation="'git stash pop' restores your work AND removes it from the stash list. It's the most common way to retrieve stashed changes.",
            sim_output="$ git stash pop\nOn branch main\nChanges not staged for commit:\n  modified: app.py\nDropped refs/stash@{0}",
        ),
        Exercise(
            type="recall",
            prompt="Bring back stashed changes but KEEP them in the stash.",
            answers=["git stash apply"],
            explanation="'git stash apply' restores changes but leaves them in the stash. Use this when you want to apply the same stash to multiple branches.",
            sim_output="$ git stash apply\nOn branch main\nChanges not staged for commit:\n  modified: app.py",
        ),
        Exercise(
            type="scenario",
            prompt="You're mid-feature on 'feature-x' but need to urgently fix a bug on 'main'. Your work isn't ready to commit. What's the stash workflow? (4 commands separated by &&)\n(Note: the actual bug fix happens between switch-to-main and switch-back.)",
            answers=[
                "git stash && git switch main && git switch feature-x && git stash pop",
                "git stash && git checkout main && git checkout feature-x && git stash pop",
            ],
            hint="Stash → switch to main → (fix bug there) → switch back → pop",
            explanation="Classic stash workflow: save uncommitted work, switch branches, do urgent task, switch back, restore your work. Stash is perfect for context switching.",
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Stash current changes.", answers=["git stash"],
                 explanation="Use stash when you need a clean directory but aren't ready to commit."),
        Exercise(type="recall", prompt="List stashes.", answers=["git stash list"],
                 explanation="Check what you've stashed. Each entry shows which branch and commit it came from."),
        Exercise(type="recall", prompt="Pop stashed changes.", answers=["git stash pop"],
                 explanation="Pop = apply + drop. Gets your work back and cleans up the stash list."),
        Exercise(type="recall", prompt="Apply stash without removing it.", answers=["git stash apply"],
                 explanation="When you need the same changes in multiple places, apply instead of pop."),
        Exercise(type="recall", prompt="Delete the top stash entry.", answers=["git stash drop"],
                 explanation="Clean up stashes you no longer need. drop removes without applying."),
        Exercise(type="recall", prompt="Save uncommitted work temporarily.", answers=["git stash"],
                 explanation="Stash before switching branches to avoid carrying changes with you."),
        Exercise(type="recall", prompt="Restore stashed changes (remove from stash).", answers=["git stash pop"],
                 explanation="After finishing your urgent task, pop to resume where you left off."),
        Exercise(type="recall", prompt="See all stashed changes.", answers=["git stash list"],
                 explanation="Forgot what you stashed? List shows everything with branch and commit context."),
        Exercise(type="recall", prompt="Restore stashed changes (keep in stash).", answers=["git stash apply"],
                 explanation="Apply doesn't clean up—useful for testing stashed changes on different branches."),
        Exercise(type="recall", prompt="Stash your work.", answers=["git stash"],
                 explanation="Stashing is reversible—you can always get your work back with pop or apply."),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 18 — Reflog (The Panic Button)
# ═══════════════════════════════════════════════════════════

LEVEL_18 = Level(
    number=18,
    name="Reflog",
    tagline="The panic button. Recover from anything.",
    concept=(
        "git reflog shows EVERY move HEAD has made — even ones 'lost' by reset.\n"
        "If you accidentally git reset --hard, reflog is how you get it back.\n"
        "Reflog is LOCAL only — it records your actions, not remote history."
    ),
    commands_taught=["git reflog"],
    teachings=[
        Teaching(
            command="git reflog",
            syntax="git reflog",
            explanation=(
                "Every time HEAD moves (commit, reset, checkout, merge, rebase), Git\n"
                "records it in the 'reflog' (reference log). Even if you 'delete' commits\n"
                "with 'git reset --hard', they're still in the reflog for about 90 days.\n"
                "\n"
                "The reflog is your safety net. If you ever lose commits, this is how\n"
                "you find them again.\n"
                "\n"
                "Recovery workflow:\n"
                "  1. Run 'git reflog' to find the commit hash you want\n"
                "  2. Run 'git reset --hard <hash>' to go back to that point"
            ),
            example_output=(
                "$ git reflog\n"
                "abc1234 (HEAD -> main) HEAD@{0}: reset: moving to HEAD~3\n"
                "def5678 HEAD@{1}: commit: add feature C\n"
                "ghi9012 HEAD@{2}: commit: add feature B\n"
                "jkl3456 HEAD@{3}: commit: add feature A\n"
                "mno7890 HEAD@{4}: commit: initial commit\n"
                "\n"
                "# Even though we reset past 3 commits, they're still here!\n"
                "$ git reset --hard def5678\n"
                "HEAD is now at def5678 add feature C\n"
                "# All 3 commits recovered!"
            ),
            pro_tip="Reflog is LOCAL only — it only records YOUR actions on YOUR machine. It's not shared with teammates.",
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="View the reflog (every action HEAD has taken).",
            answers=["git reflog"],
            explanation="'git reflog' is your safety net—it shows every HEAD movement. Even 'deleted' commits are here for ~90 days. Use it when you mess up badly.",
            sim_output="$ git reflog\nabc1234 (HEAD -> main) HEAD@{0}: reset: moving to HEAD~1\ndef5678 HEAD@{1}: commit: add feature\nghi9012 HEAD@{2}: commit: initial commit",
        ),
        Exercise(
            type="scenario",
            prompt="You ran 'git reset --hard HEAD~3' and lost 3 commits. How do you find the lost commit hash?",
            answers=["git reflog"],
            explanation="Reflog records the reset action AND the commits before it. Look for the commit hash before the reset—that's what you need to recover.",
            sim_output="$ git reflog\nabc1234 (HEAD -> main) HEAD@{0}: reset: moving to HEAD~3\ndef5678 HEAD@{1}: commit: third commit\nghi9012 HEAD@{2}: commit: second commit\njkl3456 HEAD@{3}: commit: first commit",
            hint="reflog records everything, even resets",
        ),
        Exercise(
            type="scenario",
            prompt="You found the lost commit hash 'def5678' in reflog. How do you recover to that point?",
            answers=["git reset --hard def5678", "git reset def5678"],
            explanation="Once you have the hash from reflog, reset to it. This moves HEAD back to that commit, recovering everything that was 'lost'.",
            sim_output="$ git reset --hard def5678\nHEAD is now at def5678 third commit\n(all 3 commits recovered!)",
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="View the reflog.", answers=["git reflog"],
                 explanation="Reflog = reference log. It tracks every time your HEAD pointer moves."),
        Exercise(type="recall", prompt="See all recent HEAD movements.", answers=["git reflog"],
                 explanation="Check reflog when something goes wrong. It's your history of Git operations."),
        Exercise(type="recall", prompt="Find a commit lost after hard reset.", answers=["git reflog"],
                 explanation="Hard reset looks permanent but reflog keeps everything. Nothing is truly lost."),
        Exercise(type="recall", prompt="Recover to commit abc1234 after a bad reset.", answers=["git reset --hard abc1234"],
                 explanation="Copy the hash from reflog, then reset to it. You can undo almost anything."),
        Exercise(type="recall", prompt="View reflog history.", answers=["git reflog"],
                 explanation="Reflog entries have HEAD@{N} notation. Higher numbers are older actions."),
        Exercise(type="recall", prompt="Recover to commit def5678.", answers=["git reset --hard def5678"],
                 explanation="This is the reflog recovery workflow: reflog → find hash → reset to hash."),
        Exercise(type="recall", prompt="Show every action HEAD has taken.", answers=["git reflog"],
                 explanation="Commits, checkouts, merges, resets, rebases—all recorded. Reflog sees everything."),
        Exercise(type="recall", prompt="Reset to a specific reflog entry.", answers=["git reset --hard <hash>", "git reset --hard abc1234"],
                 explanation="You can also use HEAD@{N} notation: 'git reset --hard HEAD@{2}' goes to the 3rd-most-recent state."),
        Exercise(type="recall", prompt="Use the panic button.", answers=["git reflog"],
                 explanation="Accidentally destroyed commits? Reflog is Git's panic button. Don't panic—check reflog."),
        Exercise(type="recall", prompt="Find lost commits.", answers=["git reflog"],
                 explanation="Commits are only truly deleted after reflog expires (90 days by default). Until then, reflog can save you."),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 19 — Rebase
# ═══════════════════════════════════════════════════════════

LEVEL_19 = Level(
    number=19,
    name="Rebase",
    tagline="Clean, linear history.",
    concept=(
        "git rebase main replays YOUR commits on top of main (while on a feature branch).\n"
        "git rebase -i HEAD~N lets you squash, reword, or reorder commits.\n"
        "GOLDEN RULE: Never rebase commits that have been pushed/shared."
    ),
    commands_taught=["git rebase main", "git rebase -i HEAD~N", "git rebase --continue",
                     "git rebase --abort"],
    teachings=[
        Teaching(
            command="git rebase main",
            syntax="git rebase main",
            explanation=(
                "Merging creates a merge commit and preserves the branch history.\n"
                "Rebasing takes your branch's commits and 'replays' them on top of main,\n"
                "creating a clean, LINEAR history with no merge commits.\n"
                "\n"
                "You must be ON the feature branch when you rebase:\n"
                "  1. git switch feature\n"
                "  2. git rebase main\n"
                "\n"
                "This moves your feature commits to the tip of main."
            ),
            example_output=(
                "$ git switch feature\n"
                "$ git rebase main\n"
                "Successfully rebased and updated refs/heads/feature.\n"
                "\n"
                "$ git log --oneline --graph\n"
                "* abc1234 (HEAD -> feature) add signup\n"
                "* def5678 add login\n"
                "* ghi9012 (main) latest main commit\n"
                "* jkl3456 initial commit"
            ),
            pro_tip="After rebasing, your feature branch is up-to-date with main. You can now merge with a clean fast-forward.",
        ),
        Teaching(
            command="git rebase -i HEAD~N",
            syntax="git rebase -i HEAD~N",
            explanation=(
                "Interactive rebase lets you EDIT your commit history. You can:\n"
                "  • squash  — merge multiple commits into one\n"
                "  • reword  — change a commit message\n"
                "  • reorder — move commits around\n"
                "  • drop    — delete a commit entirely\n"
                "\n"
                "Your editor opens with a list of commits. Change 'pick' to the action you want."
            ),
            example_output=(
                "$ git rebase -i HEAD~3\n"
                "# Editor opens with:\n"
                "pick abc1234 add login page\n"
                "pick def5678 fix typo in login\n"
                "pick ghi9012 add login tests\n"
                "\n"
                "# Change to: (squash the typo fix into the first commit)\n"
                "pick abc1234 add login page\n"
                "squash def5678 fix typo in login\n"
                "pick ghi9012 add login tests"
            ),
            pro_tip="Use interactive rebase to clean up messy commits BEFORE pushing. Never rebase already-pushed commits!",
        ),
        Teaching(
            command="git rebase --continue",
            syntax="git rebase --continue",
            explanation=(
                "If a rebase hits a conflict, it pauses. After you resolve the conflict\n"
                "(edit the file, git add it), run this command to continue the rebase\n"
                "with the remaining commits."
            ),
            example_output=(
                "# After resolving conflict:\n"
                "$ git add app.py\n"
                "$ git rebase --continue\n"
                "Successfully rebased and updated refs/heads/feature."
            ),
        ),
        Teaching(
            command="git rebase --abort",
            syntax="git rebase --abort",
            explanation=(
                "If a rebase goes wrong and you want to cancel the whole thing,\n"
                "this command aborts the rebase and restores everything to the state\n"
                "BEFORE you started rebasing. No changes are lost."
            ),
            example_output=(
                "$ git rebase --abort\n"
                "(rebase cancelled, back to pre-rebase state)"
            ),
            pro_tip="Don't panic during a messy rebase! You can always --abort and try a different approach.",
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="You're on branch 'feature'. Rebase it onto the latest 'main'.",
            answers=["git rebase main"],
            explanation="While on a feature branch, 'git rebase main' replays your commits on top of main's latest changes. Creates clean, linear history without merge commits.",
            sim_output="$ git rebase main\nSuccessfully rebased and updated refs/heads/feature.",
        ),
        Exercise(
            type="recall",
            prompt="Interactively rebase the last 3 commits (to squash, reword, etc.).",
            answers=["git rebase -i HEAD~3"],
            explanation="Interactive rebase (-i) opens an editor where you can squash commits, change messages, reorder, or delete. Perfect for cleaning up messy history before pushing.",
            sim_output="$ git rebase -i HEAD~3\n(editor opens with)\npick abc1234 first commit\npick def5678 second commit\npick ghi9012 third commit\n\n# Commands:\n# p, pick = use commit\n# s, squash = meld into previous commit\n# r, reword = change commit message",
        ),
        Exercise(
            type="scenario",
            prompt="During a rebase, you hit a conflict. After resolving it, what command continues the rebase?",
            answers=["git rebase --continue"],
            explanation="Rebase conflicts work like merge conflicts: edit file, remove markers, 'git add', then '--continue' to proceed with remaining commits.",
            sim_output="$ git rebase --continue\nSuccessfully rebased.",
        ),
        Exercise(
            type="scenario",
            prompt="You're mid-rebase and it's a mess. You want to cancel and go back to before the rebase. What command?",
            answers=["git rebase --abort"],
            explanation="'--abort' cancels the rebase and restores everything to pre-rebase state. Nothing is lost—it's a complete undo. Use this when things go wrong.",
            sim_output="$ git rebase --abort\n(rebase cancelled, back to original state)",
        ),
        Exercise(
            type="multi_choice",
            prompt="The golden rule of rebase is:",
            answers=["a"],
            explanation="NEVER rebase commits that teammates have already pulled. Rebase rewrites history, which breaks their repos. Only rebase local, unpushed work.",
            choices=["a) Never rebase commits that have been pushed/shared", "b) Always rebase instead of merge", "c) Only rebase on main branch"],
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Rebase current branch onto main.", answers=["git rebase main"],
                 explanation="Updates your feature branch with main's changes. Must be ON the feature branch when you run this."),
        Exercise(type="recall", prompt="Interactive rebase last 3 commits.", answers=["git rebase -i HEAD~3"],
                 explanation="Clean up commit history before pushing. Squash tiny commits, fix typos in messages, remove debug commits."),
        Exercise(type="recall", prompt="Continue rebase after resolving conflict.", answers=["git rebase --continue"],
                 explanation="After 'git add'ing the resolved files, continue processes the next commit in the rebase."),
        Exercise(type="recall", prompt="Abort a messy rebase.", answers=["git rebase --abort"],
                 explanation="Escape hatch when rebase goes sideways. Returns to pre-rebase state immediately."),
        Exercise(type="recall", prompt="Rebase feature branch onto main.", answers=["git rebase main"],
                 explanation="Common workflow: update feature with main's changes, then merge back to main with clean fast-forward."),
        Exercise(type="recall", prompt="Squash last 2 commits interactively.", answers=["git rebase -i HEAD~2"],
                 explanation="Change the second commit from 'pick' to 'squash'—it'll merge into the first commit."),
        Exercise(type="recall", prompt="Resume rebase after conflict fix.", answers=["git rebase --continue"],
                 explanation="Rebase can pause multiple times if there are multiple conflicting commits. Keep resolving and continuing."),
        Exercise(type="recall", prompt="Cancel rebase entirely.", answers=["git rebase --abort"],
                 explanation="If you realize mid-rebase this isn't what you wanted, abort saves you."),
        Exercise(type="recall", prompt="Rebase onto main for clean history.", answers=["git rebase main"],
                 explanation="Rebasing keeps project history linear and clean—no merge commit clutter."),
        Exercise(type="recall", prompt="Interactive rebase last 5 commits.", answers=["git rebase -i HEAD~5"],
                 explanation="Before submitting a pull request, clean up your commits so reviewers see clean history."),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 20 — Pro Moves
# ═══════════════════════════════════════════════════════════

LEVEL_20 = Level(
    number=20,
    name="Pro Moves",
    tagline="The final toolkit.",
    concept=(
        "cherry-pick grabs a single commit from another branch.\n"
        "tag marks a specific commit (like a version release).\n"
        "blame shows who wrote each line. amend fixes the last commit. aliases save keystrokes."
    ),
    commands_taught=["git cherry-pick <hash>", "git tag v1.0", "git tag -a v1.0 -m 'msg'",
                     "git blame <file>", "git commit --amend", "git push --force-with-lease",
                     "git config --global alias.st status"],
    teachings=[
        Teaching(
            command="git cherry-pick <hash>",
            syntax="git cherry-pick <commit-hash>",
            explanation=(
                "Sometimes you need just ONE specific commit from another branch, not\n"
                "the whole branch. Cherry-pick copies that single commit and applies it\n"
                "to your current branch.\n"
                "\n"
                "Common use case: A critical bug fix was made on a feature branch,\n"
                "and you need it on main without merging the entire feature."
            ),
            example_output=(
                "$ git cherry-pick abc1234\n"
                "[main xyz9876] fix critical login bug\n"
                " 1 file changed, 2 insertions(+), 1 deletion(-)"
            ),
            pro_tip="Cherry-pick creates a NEW commit with a different hash. The original commit on the other branch is untouched.",
        ),
        Teaching(
            command="git tag",
            syntax="git tag <tag-name>",
            explanation=(
                "Tags mark a specific commit with a readable name, usually for version\n"
                "releases like v1.0, v2.3.1, etc.\n"
                "\n"
                "Two types:\n"
                "  • Lightweight: git tag v1.0 — just a name pointer\n"
                "  • Annotated: git tag -a v1.0 -m 'msg' — includes metadata (author, date, message)"
            ),
            example_output=(
                "$ git tag v1.0\n"
                "$ git tag\n"
                "v1.0\n"
                "\n"
                '$ git tag -a v2.0 -m "Release version 2.0"\n'
                "$ git tag\n"
                "v1.0\n"
                "v2.0"
            ),
            pro_tip="Use 'git push --tags' to push tags to the remote. Tags don't push automatically with 'git push'.",
        ),
        Teaching(
            command="git blame <file>",
            syntax="git blame <filename>",
            explanation=(
                "Shows who last modified each line of a file, with the commit hash and date.\n"
                "Despite the aggressive name, it's incredibly useful for understanding\n"
                "why code was written a certain way — you can trace each line to its commit."
            ),
            example_output=(
                "$ git blame app.py\n"
                "abc1234 (Alice  2026-02-10 14:30:00) import os\n"
                "def5678 (Bob    2026-02-11 09:15:00) import sys\n"
                "abc1234 (Alice  2026-02-10 14:30:00)\n"
                "ghi9012 (Alice  2026-02-12 11:00:00) def main():\n"
                "ghi9012 (Alice  2026-02-12 11:00:00)     print('hello')"
            ),
        ),
        Teaching(
            command="git commit --amend",
            syntax='git commit --amend -m "new message"',
            explanation=(
                "Oops, typo in your commit message? Forgot to stage a file?\n"
                "'git commit --amend' lets you fix the LAST commit. It replaces the\n"
                "most recent commit with a new one.\n"
                "\n"
                "You can:\n"
                "  • Fix the message: git commit --amend -m 'corrected message'\n"
                "  • Add a forgotten file: git add file.py && git commit --amend"
            ),
            example_output=(
                '$ git commit --amend -m "fix: correct typo in login"\n'
                '[main abc1234] fix: correct typo in login\n'
                " Date: Wed Feb 12 12:00:00 2026"
            ),
            pro_tip="Only amend commits that haven't been pushed! Amending a pushed commit rewrites history.",
        ),
        Teaching(
            command="git push --force-with-lease",
            syntax="git push --force-with-lease",
            explanation=(
                "After amending or rebasing, a regular 'git push' will be rejected because\n"
                "the remote has a different version of your branch.\n"
                "\n"
                "'git push --force-with-lease' is a SAFE force push. It checks if anyone\n"
                "else pushed to that branch first. If they did, it fails instead of\n"
                "overwriting their work. Much safer than the dangerous 'git push --force'."
            ),
            example_output=(
                "$ git push --force-with-lease\n"
                "Counting objects: 3, done.\n"
                "To https://github.com/user/project.git\n"
                " + abc1234...def5678 main -> main (forced update)"
            ),
            pro_tip="NEVER use 'git push --force' on shared branches. Always use --force-with-lease instead.",
        ),
        Teaching(
            command="git config alias",
            syntax="git config --global alias.<shortcut> <command>",
            explanation=(
                "Tired of typing long commands? Create aliases — keyboard shortcuts for Git.\n"
                "Once set, they work everywhere on your machine.\n"
                "\n"
                "Popular aliases:\n"
                "  • git st  → git status\n"
                "  • git co  → git checkout\n"
                "  • git br  → git branch\n"
                "  • git ci  → git commit"
            ),
            example_output=(
                "$ git config --global alias.st status\n"
                "$ git config --global alias.co checkout\n"
                "$ git config --global alias.br branch\n"
                "\n"
                "# Now you can use:\n"
                "$ git st\n"
                "On branch main\n"
                "nothing to commit, working tree clean"
            ),
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="Grab ONLY commit abc1234 from another branch and apply it to your current branch.",
            answers=["git cherry-pick abc1234"],
            explanation="Cherry-pick copies a single commit from anywhere to your current branch. Perfect for grabbing a bug fix from a feature branch without merging everything.",
            sim_output="$ git cherry-pick abc1234\n[main xyz9876] cherry-picked feature\n 1 file changed, 10 insertions(+)",
        ),
        Exercise(
            type="recall",
            prompt="Create a lightweight tag called 'v1.0' on the current commit.",
            answers=["git tag v1.0"],
            explanation="Tags mark important commits like releases. 'v1.0' is now a permanent pointer to this commit—much easier to reference than a hash.",
            sim_output="$ git tag v1.0\n(tag created)",
        ),
        Exercise(
            type="recall",
            prompt="Create an annotated tag 'v2.0' with the message 'Release version 2.0'.",
            answers=[
                'git tag -a v2.0 -m "Release version 2.0"',
                "git tag -a v2.0 -m 'Release version 2.0'",
            ],
            explanation="Annotated tags (-a) store metadata: who tagged it, when, and why. Use them for official releases. They're more professional than lightweight tags.",
            sim_output='$ git tag -a v2.0 -m "Release version 2.0"\n(annotated tag created)',
        ),
        Exercise(
            type="recall",
            prompt="See who last modified each line of 'app.py'.",
            answers=["git blame app.py"],
            explanation="'git blame' shows who wrote each line and when. Despite the name, it's for understanding code history, not assigning fault. Great for finding who to ask about mysterious code.",
            sim_output="$ git blame app.py\nabc1234 (Alice 2026-02-10 14:30) import os\ndef5678 (Bob   2026-02-11 09:15) import sys\nabc1234 (Alice 2026-02-10 14:30) \nghi9012 (Alice 2026-02-12 11:00) def main():",
        ),
        Exercise(
            type="recall",
            prompt="Fix the message of your LAST commit (change it to 'fix: correct typo').",
            answers=[
                'git commit --amend -m "fix: correct typo"',
                "git commit --amend -m 'fix: correct typo'",
            ],
            explanation="'--amend' rewrites the last commit. Use it to fix typos in messages or add forgotten files. Only amend commits that haven't been pushed!",
            sim_output='$ git commit --amend -m "fix: correct typo"\n[main abc1234] fix: correct typo',
        ),
        Exercise(
            type="recall",
            prompt="Create a Git alias so 'git st' runs 'git status'.",
            answers=["git config --global alias.st status"],
            explanation="Aliases are keyboard shortcuts. 'git st' is faster than 'git status'. Set them once globally—they work forever.",
            sim_output="$ git config --global alias.st status\n(alias created — now 'git st' works like 'git status')",
        ),
        Exercise(
            type="recall",
            prompt="Force push safely (check if someone else pushed first).",
            answers=["git push --force-with-lease"],
            explanation="After rebase/amend, you need force push. '--force-with-lease' is safe—it fails if someone else pushed, preventing you from overwriting their work. NEVER use plain --force.",
            sim_output="$ git push --force-with-lease\nCounting objects: 3, done.\nTo https://github.com/user/project.git\n + abc1234...def5678 main -> main (forced update)",
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Cherry-pick commit def5678.", answers=["git cherry-pick def5678"],
                 explanation="Cherry-pick is Git's 'copy one commit' command. Useful for selective merging."),
        Exercise(type="recall", prompt="Tag current commit as v1.0.", answers=["git tag v1.0"],
                 explanation="Tag releases so you can always find them. 'git checkout v1.0' jumps to that release."),
        Exercise(type="recall", prompt="Blame file 'server.js'.", answers=["git blame server.js"],
                 explanation="Blame shows commit history per line. Click the hash to see the full commit context."),
        Exercise(type="recall", prompt="Amend last commit message to 'update docs'.",
                 answers=['git commit --amend -m "update docs"', "git commit --amend -m 'update docs'"],
                 explanation="Typo in your commit message? Amend fixes it. Just don't amend pushed commits."),
        Exercise(type="recall", prompt="Safe force push.", answers=["git push --force-with-lease"],
                 explanation="--force-with-lease protects against overwriting teammate's work. It's force push with training wheels."),
        Exercise(type="recall", prompt="Create alias: 'git co' = 'git checkout'.",
                 answers=["git config --global alias.co checkout"],
                 explanation="'co' for checkout, 'br' for branch, 'ci' for commit—build your own Git vocabulary."),
        Exercise(type="recall", prompt="Cherry-pick commit ghi9012.", answers=["git cherry-pick ghi9012"],
                 explanation="Cherry-picking creates a NEW commit—the original stays on its branch."),
        Exercise(type="recall", prompt="Create annotated tag v3.0.",
                 answers=['git tag -a v3.0 -m "Release v3.0"', "git tag -a v3.0 -m 'Release v3.0'",
                          'git tag -a v3.0 -m "v3.0"'],
                 explanation="Annotated tags are richer than lightweight—they include tagger info and messages."),
        Exercise(type="recall", prompt="See who wrote each line of 'utils.py'.", answers=["git blame utils.py"],
                 explanation="Use blame to understand why code exists. Each line traces to a commit explaining the change."),
        Exercise(type="recall", prompt="Fix the last commit message.",
                 answers=["git commit --amend", 'git commit --amend -m "<message>"'],
                 explanation="Without -m, amend opens your editor to change the message. With -m, you replace it inline."),
    ],
)


ADVANCED_LEVELS = {
    15: LEVEL_15,
    16: LEVEL_16,
    17: LEVEL_17,
    18: LEVEL_18,
    19: LEVEL_19,
    20: LEVEL_20,
}
