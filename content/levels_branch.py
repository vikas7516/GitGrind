"""
GitGrind — Levels 7-10: Branching (Branch, Switch, Merge, Conflicts).
"""
from content.models import Exercise, Level, Teaching


# ═══════════════════════════════════════════════════════════
#  LEVEL 7 — Branching
# ═══════════════════════════════════════════════════════════

LEVEL_7 = Level(
    number=7,
    name="Branching",
    tagline="Parallel universes for your code.",
    concept=(
        "A branch is an independent line of development.\n"
        "git branch <name> creates a new branch. git branch lists them all.\n"
        "The * marker shows which branch you're currently on."
    ),
    commands_taught=["git branch <name>", "git branch", "git branch -a"],
    teachings=[
        Teaching(
            command="git branch <name>",
            syntax="git branch <branch-name>",
            explanation=(
                "A branch is like a parallel universe for your code. You can work on a new\n"
                "feature in a branch without affecting the main codebase at all.\n"
                "\n"
                "When you create a branch, it starts as an exact copy of whatever branch\n"
                "you're currently on. From that point, the two branches evolve independently.\n"
                "\n"
                "Note: This command only CREATES the branch — it doesn't switch to it."
            ),
            example_output=(
                "$ git branch feature-login\n"
                "(no output — branch created)\n"
                "\n"
                "$ git branch\n"
                "  feature-login\n"
                "* main"
            ),
            pro_tip="Use descriptive branch names like 'feature-login', 'bugfix-header', 'hotfix-crash'. Avoid generic names like 'test' or 'branch1'.",
        ),
        Teaching(
            command="git branch",
            syntax="git branch",
            explanation=(
                "With no arguments, this lists all LOCAL branches in your repository.\n"
                "The branch marked with * is the one you're currently on.\n"
                "\n"
                "This is a quick way to check which branches exist and where you are."
            ),
            example_output=(
                "$ git branch\n"
                "  dev\n"
                "  feature-login\n"
                "* main\n"
                "  hotfix"
            ),
        ),
        Teaching(
            command="git branch -a",
            syntax="git branch -a",
            explanation=(
                "The -a flag shows ALL branches — both local and remote-tracking branches.\n"
                "Remote-tracking branches (like remotes/origin/main) are copies of what's\n"
                "on the remote server. This is useful when you want to see everything."
            ),
            example_output=(
                "$ git branch -a\n"
                "  feature-login\n"
                "* main\n"
                "  remotes/origin/main\n"
                "  remotes/origin/feature-login"
            ),
            pro_tip="Use 'git branch -r' to see ONLY remote branches.",
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="Create a new branch called 'feature-login'.",
            answers=["git branch feature-login"],
            explanation="'git branch <name>' creates a new branch but doesn't switch to it. The branch starts as a copy of where you currently are.",
            sim_output="$ git branch feature-login\n(branch created)\n\n$ git branch\n  feature-login\n* main",
        ),
        Exercise(
            type="recall",
            prompt="List all local branches.",
            answers=["git branch"],
            explanation="'git branch' with no arguments lists all local branches. The * shows which one you're on. Essential for knowing where you are!",
            sim_output="$ git branch\n  feature-login\n* main",
        ),
        Exercise(
            type="recall",
            prompt="List ALL branches including remote-tracking branches.",
            answers=["git branch -a", "git branch --all"],
            explanation="The -a flag (--all) shows local branches AND remote-tracking branches. Remote branches are prefixed with 'remotes/origin/'.",
            sim_output="$ git branch -a\n  feature-login\n* main\n  remotes/origin/main",
        ),
        Exercise(
            type="multi_choice",
            prompt="In the output of 'git branch', what does the * mean?",
            answers=["a"],
            explanation="The asterisk (*) marks your current branch—where new commits will go. It's your 'you are here' marker.",
            choices=["a) The branch you're currently on", "b) The branch with the most commits", "c) A protected branch"],
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Create branch 'feature-signup'.", answers=["git branch feature-signup"],
                 explanation="Use 'git branch <name>' to create new branches. Choose descriptive names that explain what the branch is for."),
        Exercise(type="recall", prompt="List all local branches.", answers=["git branch"],
                 explanation="Run this anytime you forget which branches exist or which one you're on."),
        Exercise(type="recall", prompt="Create branch 'hotfix'.", answers=["git branch hotfix"],
                 explanation="'hotfix' is a common name for branches that fix critical bugs in production."),
        Exercise(type="recall", prompt="Create branch 'dev'.", answers=["git branch dev"],
                 explanation="Many teams use a 'dev' or 'develop' branch for ongoing development work."),
        Exercise(type="recall", prompt="List all branches (local + remote).", answers=["git branch -a", "git branch --all"],
                 explanation="-a shows everything: your local branches and copies of remote branches."),
        Exercise(type="recall", prompt="Create branch 'bugfix-header'.", answers=["git branch bugfix-header"],
                 explanation="Prefixes like 'bugfix-', 'feature-', 'hotfix-' make it clear what type of work the branch contains."),
        Exercise(type="recall", prompt="See all local branches.", answers=["git branch"],
                 explanation="This is one of the most-run Git commands. Check it constantly to stay oriented."),
        Exercise(type="recall", prompt="Create branch 'experiment'.", answers=["git branch experiment"],
                 explanation="Branches are cheap! Create one for experiments so you can easily throw away failed attempts."),
        Exercise(type="recall", prompt="Create branch 'release-v2'.", answers=["git branch release-v2"],
                 explanation="Release branches (like 'release-v2') are often used to prepare a specific version for deployment."),
        Exercise(type="recall", prompt="List every branch you have.", answers=["git branch"],
                 explanation="Simple 'git branch' shows your local branches. Add -a to also see remote ones."),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 8 — Switching Branches
# ═══════════════════════════════════════════════════════════

LEVEL_8 = Level(
    number=8,
    name="Switching Branches",
    tagline="Move between realities.",
    concept=(
        "git switch <branch> moves you to a different branch.\n"
        "git switch -c <name> creates a new branch AND switches to it in one step.\n"
        "The older way is git checkout / git checkout -b (still works)."
    ),
    commands_taught=["git switch <branch>", "git switch -c <name>", "git checkout <branch>", "git checkout -b <name>"],
    teachings=[
        Teaching(
            command="git switch <branch>",
            syntax="git switch <branch-name>",
            explanation=(
                "This moves you from your current branch to another existing branch.\n"
                "When you switch, Git updates all your working files to match the state\n"
                "of that branch. It's like teleporting to a different version of your project.\n"
                "\n"
                "Important: Commit or stash your changes before switching! Uncommitted\n"
                "changes can cause conflicts when switching branches."
            ),
            example_output=(
                "$ git switch feature-login\n"
                "Switched to branch 'feature-login'"
            ),
            pro_tip="'git switch' is newer and recommended. 'git checkout' does the same thing but is older.",
        ),
        Teaching(
            command="git switch -c <name>",
            syntax="git switch -c <new-branch-name>",
            explanation=(
                "The -c flag means 'create'. This creates a NEW branch AND switches to it\n"
                "in a single command. It's a shortcut that combines:\n"
                "  1. git branch <name>   (create)\n"
                "  2. git switch <name>   (switch)\n"
                "\n"
                "This is the most common way to start working on a new feature."
            ),
            example_output=(
                "$ git switch -c feature-signup\n"
                "Switched to a new branch 'feature-signup'\n"
                "\n"
                "$ git branch\n"
                "* feature-signup\n"
                "  main"
            ),
        ),
        Teaching(
            command="git checkout <branch>",
            syntax="git checkout <branch-name>",
            explanation=(
                "This is the older command for switching branches. It does the same thing\n"
                "as 'git switch' but has been around since Git's early days.\n"
                "\n"
                "You'll see it in tutorials and Stack Overflow answers everywhere.\n"
                "Both 'git switch' and 'git checkout' work — use whichever you prefer."
            ),
            example_output=(
                "$ git checkout main\n"
                "Switched to branch 'main'"
            ),
        ),
        Teaching(
            command="git checkout -b <name>",
            syntax="git checkout -b <new-branch-name>",
            explanation=(
                "The older version of 'git switch -c'. Creates a new branch AND switches\n"
                "to it in one command. Uses -b instead of -c.\n"
                "\n"
                "  • git switch -c  = new way (recommended)\n"
                "  • git checkout -b = old way (still works everywhere)"
            ),
            example_output=(
                "$ git checkout -b dark-mode\n"
                "Switched to a new branch 'dark-mode'"
            ),
            pro_tip="In job interviews and team settings, both are accepted. Know both, prefer 'git switch'.",
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="Switch to the branch called 'feature-login'.",
            answers=["git switch feature-login", "git checkout feature-login"],
            explanation="'git switch <branch>' moves you to an existing branch. All your files change to match that branch's state. Modern way: 'git switch'. Old way: 'git checkout'.",
            sim_output="$ git switch feature-login\nSwitched to branch 'feature-login'",
        ),
        Exercise(
            type="recall",
            prompt="Create a new branch called 'feature-signup' AND switch to it in one command.",
            answers=["git switch -c feature-signup", "git checkout -b feature-signup"],
            explanation="The -c flag (or -b with checkout) creates the branch and switches to it in one step. This is the most common way to start new work.",
            sim_output="$ git switch -c feature-signup\nSwitched to a new branch 'feature-signup'",
        ),
        Exercise(
            type="recall",
            prompt="Switch back to the main branch.",
            answers=["git switch main", "git checkout main"],
            explanation="You'll switch back to 'main' often—to merge finished features, to start new work, or to check the stable codebase.",
            sim_output="$ git switch main\nSwitched to branch 'main'",
        ),
        Exercise(
            type="scenario",
            prompt="You're on 'main' and need to start working on a new feature called 'dark-mode'. Create the branch and switch to it with ONE command.",
            answers=["git switch -c dark-mode", "git checkout -b dark-mode"],
            explanation="Creating + switching in one command is faster than running two separate commands. Use -c (or -b) for this.",
            sim_output="Switched to a new branch 'dark-mode'",
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Switch to branch 'dev'.", answers=["git switch dev", "git checkout dev"],
                 explanation="Switching between branches is instant—Git just updates your files to match the branch."),
        Exercise(type="recall", prompt="Create + switch to 'feature-chat'.", answers=["git switch -c feature-chat", "git checkout -b feature-chat"],
                 explanation="The one-command create-and-switch is what you'll use 90% of the time when starting new work."),
        Exercise(type="recall", prompt="Go back to 'main'.", answers=["git switch main", "git checkout main"],
                 explanation="Return to 'main' when you need to merge work or start a fresh feature branch."),
        Exercise(type="recall", prompt="Switch to 'hotfix'.", answers=["git switch hotfix", "git checkout hotfix"],
                 explanation="Hotfix branches are for urgent production bugs. Switch to them when you need to fix something fast."),
        Exercise(type="recall", prompt="Create + switch to 'experiment'.", answers=["git switch -c experiment", "git checkout -b experiment"],
                 explanation="Experiment branches let you try risky ideas without affecting the main code."),
        Exercise(type="recall", prompt="Switch to 'feature-login'.", answers=["git switch feature-login", "git checkout feature-login"],
                 explanation="When you switch, Git saves your current branch state and loads the target branch."),
        Exercise(type="recall", prompt="Create + switch to 'bugfix-nav'.", answers=["git switch -c bugfix-nav", "git checkout -b bugfix-nav"],
                 explanation="Bugfix branches isolate your fixes so they don't interfere with other ongoing work."),
        Exercise(type="recall", prompt="Switch to 'main'.", answers=["git switch main", "git checkout main"],
                 explanation="'main' (or 'master' in older repos) is typically the stable, deployable version of your code."),
        Exercise(type="recall", prompt="Create + switch to 'release-v3'.", answers=["git switch -c release-v3", "git checkout -b release-v3"],
                 explanation="Release branches freeze features for a specific version while development continues elsewhere."),
        Exercise(type="recall", prompt="Switch to 'dev'.", answers=["git switch dev", "git checkout dev"],
                 explanation="Many teams use 'dev' as an integration branch where features are tested before going to 'main'."),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 9 — Merging
# ═══════════════════════════════════════════════════════════

LEVEL_9 = Level(
    number=9,
    name="Merging",
    tagline="Combine branch work back together.",
    concept=(
        "git merge <branch> merges another branch INTO your current branch.\n"
        "You must be ON the branch you want to merge INTO (usually main).\n"
        "After merging, you can delete the merged branch with git branch -d."
    ),
    commands_taught=["git merge <branch>", "git branch -d <name>", "git log --oneline --graph"],
    teachings=[
        Teaching(
            command="git merge <branch>",
            syntax="git merge <branch-name>",
            explanation=(
                "Merging takes the commits from one branch and combines them into your\n"
                "current branch. The most common workflow is:\n"
                "  1. Switch to 'main'\n"
                "  2. Run 'git merge feature-login'\n"
                "\n"
                "This brings all the feature work into main. The key rule:\n"
                "You must be ON the branch you want the changes to go INTO."
            ),
            example_output=(
                "$ git switch main\n"
                "Switched to branch 'main'\n"
                "\n"
                "$ git merge feature-login\n"
                "Merge made by the 'ort' strategy.\n"
                " login.html | 45 +++++++++++++++++++\n"
                " login.css  | 23 ++++++++++\n"
                " 2 files changed, 68 insertions(+)"
            ),
            pro_tip="Always switch to the target branch FIRST, then merge the source branch INTO it.",
        ),
        Teaching(
            command="git branch -d <name>",
            syntax="git branch -d <branch-name>",
            explanation=(
                "After merging a branch, it's good practice to delete it. The -d flag\n"
                "stands for 'delete' and only works if the branch has been fully merged.\n"
                "\n"
                "This keeps your branch list clean. Don't worry — the commits from\n"
                "that branch are preserved in the merge history."
            ),
            example_output=(
                "$ git branch -d feature-login\n"
                "Deleted branch feature-login (was abc1234)."
            ),
            pro_tip="Use -D (capital) to force-delete a branch that hasn't been merged. Be careful with this!",
        ),
        Teaching(
            command="git log --oneline --graph",
            syntax="git log --oneline --graph",
            explanation=(
                "After merging, it's useful to see the visual history of how branches\n"
                "came together. The --graph flag draws a text-based branch diagram\n"
                "showing merges, forks, and the overall shape of your history."
            ),
            example_output=(
                "$ git log --oneline --graph\n"
                "*   m3rg3id (HEAD -> main) Merge branch 'feature-login'\n"
                "|\\  \n"
                "| * abc1234 add login page\n"
                "| * def5678 add auth module\n"
                "|/  \n"
                "* ghi9012 initial commit"
            ),
        ),
    ],
    exercises=[
        Exercise(
            type="scenario",
            prompt="You're on 'main'. Merge the branch 'feature-login' into main.",
            answers=["git merge feature-login"],
            explanation="'git merge <branch>' brings that branch's commits INTO your current branch. You must be on the target branch (main) first!",
            sim_output="$ git merge feature-login\nMerge made by the 'ort' strategy.\n app.py | 25 +++++++++++++\n 1 file changed, 25 insertions(+)",
        ),
        Exercise(
            type="recall",
            prompt="View the commit graph to verify the merge.",
            answers=["git log --oneline --graph", "git log --oneline --graph --all"],
            explanation="After merging, use --graph to visually see how the branches came together. The lines show where branches diverged and merged.",
            sim_output="$ git log --oneline --graph\n*   m3rg3id (HEAD -> main) Merge branch 'feature-login'\n|\\  \n| * abc1234 add login page\n| * def5678 add auth module\n|/\n* ghi9012 initial commit",
        ),
        Exercise(
            type="recall",
            prompt="Delete the branch 'feature-login' after it's been merged.",
            answers=["git branch -d feature-login"],
            explanation="'git branch -d' safely deletes a merged branch. The -d won't work if the branch isn't merged (use -D to force). The commits stay in history.",
            sim_output="$ git branch -d feature-login\nDeleted branch feature-login (was abc1234).",
        ),
        Exercise(
            type="multi_choice",
            prompt="After merging 'feature' into 'main', which branch has the new commits?",
            answers=["b"],
            explanation="Merging brings commits INTO the current branch. If you're on 'main' and merge 'feature', main gets the commits. Think: 'merge feature INTO main'.",
            choices=["a) feature", "b) main", "c) both"],
        ),
        Exercise(
            type="scenario",
            prompt="Full workflow: create + switch to branch 'fix-typo', then switch back to main, merge it, and delete it. Write all 4 commands separated by &&.\n(Note: Assume the branch already has commits from prior work.)",
            answers=[
                "git switch -c fix-typo && git switch main && git merge fix-typo && git branch -d fix-typo",
                "git checkout -b fix-typo && git checkout main && git merge fix-typo && git branch -d fix-typo",
                "git checkout -b fix-typo && git switch main && git merge fix-typo && git branch -d fix-typo",
                "git switch -c fix-typo && git checkout main && git merge fix-typo && git branch -d fix-typo",
            ],
            explanation="This is the complete feature branch workflow: create, work on it, return to main, merge, cleanup. Master this pattern—you'll use it constantly!",
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Merge 'feature-chat' into current branch.", answers=["git merge feature-chat"],
                 explanation="Remember: you're merging the named branch INTO wherever you currently are. Check 'git branch' first!"),
        Exercise(type="recall", prompt="Delete merged branch 'feature-chat'.", answers=["git branch -d feature-chat"],
                 explanation="Cleaning up merged branches keeps your branch list manageable. The work is preserved in history."),
        Exercise(type="recall", prompt="Merge 'hotfix' into current branch.", answers=["git merge hotfix"],
                 explanation="Hotfix branches are usually merged directly into 'main' to fix production bugs quickly."),
        Exercise(type="recall", prompt="View merge graph.", answers=["git log --oneline --graph", "git log --oneline --graph --all"],
                 explanation="The graph view is essential after merges—it shows you the 'shape' of your project's history."),
        Exercise(type="recall", prompt="Delete merged branch 'hotfix'.", answers=["git branch -d hotfix"],
                 explanation="After a hotfix is deployed, delete the branch. You can always create a new one if needed."),
        Exercise(type="recall", prompt="Merge 'dev' into current branch.", answers=["git merge dev"],
                 explanation="'dev' branches often collect multiple features before being merged into 'main' for release."),
        Exercise(type="recall", prompt="Delete merged branch 'dev'.", answers=["git branch -d dev"],
                 explanation="Some teams keep 'dev' as a long-lived branch, others delete and recreate it per release cycle."),
        Exercise(type="recall", prompt="Merge 'bugfix-nav' into current branch.", answers=["git merge bugfix-nav"],
                 explanation="Bug fixes follow the same workflow as features: branch, fix, merge, delete."),
        Exercise(type="recall", prompt="Delete branch 'bugfix-nav'.", answers=["git branch -d bugfix-nav"],
                 explanation="Short-lived branches (bugfixes, features) should be deleted after merging to keep things clean."),
        Exercise(type="recall", prompt="Merge 'experiment' into current branch.", answers=["git merge experiment"],
                 explanation="Even experimental branches can be merged if the experiment succeeded!"),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 10 — Merge Conflicts
# ═══════════════════════════════════════════════════════════

LEVEL_10 = Level(
    number=10,
    name="Merge Conflicts",
    tagline="When two branches edit the same line.",
    concept=(
        "A merge conflict happens when two branches change the same lines.\n"
        "Git marks the conflict with <<<<<<< , ======= , and >>>>>>>.\n"
        "You manually pick what to keep, then git add + git commit to finish."
    ),
    commands_taught=["conflict resolution", "git add <file>"],
    teachings=[
        Teaching(
            command="conflict resolution",
            syntax="Manual editing → git add → git commit",
            explanation=(
                "When you merge two branches that changed the SAME lines in the SAME file,\n"
                "Git can't decide which version to keep. This is called a MERGE CONFLICT.\n"
                "\n"
                "Git marks the conflicting section in your file like this:\n"
                "  <<<<<<< HEAD\n"
                "  your changes on the current branch\n"
                "  =======\n"
                "  incoming changes from the branch being merged\n"
                "  >>>>>>> feature-branch\n"
                "\n"
                "To resolve it:\n"
                "  1. Open the file and find the conflict markers\n"
                "  2. Decide which version to keep (or combine both)\n"
                "  3. Delete ALL the conflict markers (<<<, ===, >>>)\n"
                "  4. Save the file"
            ),
            example_output=(
                "$ git merge feature\n"
                "Auto-merging app.py\n"
                "CONFLICT (content): Merge conflict in app.py\n"
                "Automatic merge failed; fix conflicts and then commit.\n"
                "\n"
                "# Inside app.py you'll see:\n"
                "<<<<<<< HEAD\n"
                "    print('Welcome back!')\n"
                "=======\n"
                "    print('Hello, new user!')\n"
                ">>>>>>> feature"
            ),
            pro_tip="Don't panic! Conflicts are normal. Open the file, pick the right code, remove the markers, and continue.",
        ),
        Teaching(
            command="Completing the merge",
            syntax="git add <resolved-file> && git commit",
            explanation=(
                "After you manually fix the conflict and save the file, you need to\n"
                "tell Git that you've resolved it. Do this by:\n"
                "  1. 'git add <file>' — stages the resolved file\n"
                "  2. 'git commit' — completes the merge with a merge commit\n"
                "\n"
                "Git will auto-generate a merge commit message for you."
            ),
            example_output=(
                "# After editing app.py to resolve the conflict:\n"
                "$ git add app.py\n"
                "$ git commit\n"
                "[main m3rg3id] Merge branch 'feature'"
            ),
        ),
    ],
    exercises=[
        Exercise(
            type="scenario",
            prompt="You ran 'git merge feature' and got a conflict. After manually editing the file to resolve it, what TWO commands finish the merge?",
            answers=[
                "git add <file> && git commit",
                "git add . && git commit",
            ],
            sim_output="$ git add app.py\n$ git commit\n[main m3rg3id] Merge branch 'feature'",
            hint="Stage the resolved file, then commit",
        ),
        Exercise(
            type="multi_choice",
            prompt="In a conflict file, what does the ======= line separate?",
            answers=["c"],
            choices=["a) Two different files", "b) Old code and new code", "c) Your changes (above) and incoming changes (below)"],
        ),
        Exercise(
            type="scenario",
            prompt="You see conflict markers in a file during a merge. After manually resolving the conflict (editing the file and removing markers), what two commands do you run?",
            answers=["git add <file> && git commit", "git add . && git commit",
                     "git add app.py && git commit"],
            hint="Stage the resolved file, then commit to finalize the merge",
            sim_output="$ git add app.py\n$ git commit\n[main m3rg3id] Merge branch 'feature'",
        ),
        Exercise(
            type="recall",
            prompt="After resolving a conflict and staging the file, what command completes the merge?",
            answers=["git commit"],
            sim_output="$ git commit\n[main m3rg3id] Merge branch 'feature'",
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="After fixing a conflict in app.py, stage it.", answers=["git add app.py"],
                 explanation="Staging tells Git 'I fixed this conflict, this version is correct'. It's how you mark conflicts as resolved."),
        Exercise(type="recall", prompt="After staging a resolved conflict, finish the merge.", answers=["git commit"],
                 explanation="The final 'git commit' creates a merge commit. No need for -m—Git provides a default merge message."),
        Exercise(type="recall", prompt="Stage all resolved conflicts.", answers=["git add .", "git add -A"],
                 explanation="If you have multiple conflicted files, 'git add .' stages them all at once after you've resolved each one."),
        Exercise(type="recall", prompt="Complete a merge after resolving conflicts.", answers=["git commit"],
                 explanation="This commit combines the two branches. The merge is incomplete until you run this!"),
        Exercise(type="recall", prompt="Stage resolved file 'index.html'.", answers=["git add index.html"],
                 explanation="Each resolved file must be staged individually (or use 'git add .' for all)."),
        Exercise(type="recall", prompt="After fixing conflicts and staging, commit the merge.", answers=["git commit"],
                 explanation="The merge commit has two parents—it joins the two branch histories together."),
        Exercise(type="recall", prompt="Stage resolved conflict in 'style.css'.", answers=["git add style.css"],
                 explanation="Don't forget to remove ALL conflict markers (<<<< ==== >>>>) before staging!"),
        Exercise(type="recall", prompt="Complete the merge commit.", answers=["git commit"],
                 explanation="Until you commit, the merge is in a 'mid-merge' state. Committing completes it."),
        Exercise(type="recall", prompt="Stage all resolved files at once.", answers=["git add .", "git add -A"],
                 explanation="After manually resolving all conflicts, staging them all is the quickest way to proceed."),
        Exercise(type="recall", prompt="Finalize a conflict resolution.", answers=["git commit"],
                 explanation="The merge commit is what brings the two branches together. It's the final step in resolution."),
    ],
)


BRANCH_LEVELS = {
    7: LEVEL_7,
    8: LEVEL_8,
    9: LEVEL_9,
    10: LEVEL_10,
}
