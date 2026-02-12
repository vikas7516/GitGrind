"""
GitGrind — Levels 11-14: Remote Operations (Remotes, Clone, Push, Pull).
"""
from content.models import Exercise, Level, Teaching


# ═══════════════════════════════════════════════════════════
#  LEVEL 11 — Remotes & Origin
# ═══════════════════════════════════════════════════════════

LEVEL_11 = Level(
    number=11,
    name="Remotes & Origin",
    tagline="Connect your local repo to the cloud.",
    concept=(
        "A remote is a copy of your repo hosted elsewhere (like GitHub).\n"
        "'origin' is just the conventional name for your main remote.\n"
        "git remote add connects them. git remote -v shows the URLs."
    ),
    commands_taught=["git remote add origin <url>", "git remote -v", "git remote set-url"],
    teachings=[
        Teaching(
            command="git remote add origin <url>",
            syntax="git remote add origin <url>",
            explanation=(
                "So far everything you've done is LOCAL — it only exists on your machine.\n"
                "A 'remote' is a copy of your repository hosted on a server like GitHub,\n"
                "GitLab, or Bitbucket.\n"
                "\n"
                "The name 'origin' is just a convention — it's what everyone calls the\n"
                "primary remote. You could name it anything, but 'origin' is standard.\n"
                "\n"
                "This command creates the connection. It doesn't upload anything yet."
            ),
            example_output=(
                "$ git remote add origin https://github.com/user/project.git\n"
                "(no output — remote added)\n"
                "\n"
                "$ git remote -v\n"
                "origin  https://github.com/user/project.git (fetch)\n"
                "origin  https://github.com/user/project.git (push)"
            ),
            pro_tip="You need to create the repository on GitHub first (empty, no README), then connect it with this command.",
        ),
        Teaching(
            command="git remote -v",
            syntax="git remote -v",
            explanation=(
                "The -v flag means 'verbose'. It shows the full URLs of all configured\n"
                "remotes. Each remote has two URLs — one for 'fetch' (downloading) and\n"
                "one for 'push' (uploading). They're usually the same URL."
            ),
            example_output=(
                "$ git remote -v\n"
                "origin  https://github.com/user/project.git (fetch)\n"
                "origin  https://github.com/user/project.git (push)"
            ),
        ),
        Teaching(
            command="git remote set-url",
            syntax="git remote set-url origin <new-url>",
            explanation=(
                "Made a typo in the URL? Moved the repo to a different account?\n"
                "Use 'set-url' to change the URL of an existing remote.\n"
                "This is also useful when switching from HTTPS to SSH."
            ),
            example_output=(
                "$ git remote set-url origin https://github.com/user/correct-repo.git\n"
                "(URL updated)\n"
                "\n"
                "$ git remote -v\n"
                "origin  https://github.com/user/correct-repo.git (fetch)\n"
                "origin  https://github.com/user/correct-repo.git (push)"
            ),
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="Add a remote called 'origin' pointing to 'https://github.com/user/project.git'.",
            answers=[
                "git remote add origin https://github.com/user/project.git",
            ],
            explanation="'git remote add origin <url>' connects your local repo to a server. 'origin' is the standard name for your main remote—everyone uses it.",
            sim_output="$ git remote add origin https://github.com/user/project.git\n(remote added)",
        ),
        Exercise(
            type="recall",
            prompt="Verify your remote is set up correctly.",
            answers=["git remote -v"],
            explanation="'git remote -v' shows the URLs for all remotes. The -v (verbose) flag displays both fetch and push URLs. Essential for debugging connection issues.",
            sim_output="$ git remote -v\norigin  https://github.com/user/project.git (fetch)\norigin  https://github.com/user/project.git (push)",
        ),
        Exercise(
            type="scenario",
            prompt="You set the wrong URL for origin. Change it to 'https://github.com/user/correct-repo.git'.",
            answers=["git remote set-url origin https://github.com/user/correct-repo.git"],
            explanation="'git remote set-url' updates the URL of an existing remote. Use this to fix typos or switch between HTTPS and SSH.",
            sim_output="(remote URL updated)",
        ),
        Exercise(
            type="multi_choice",
            prompt="What is 'origin'?",
            answers=["b"],
            explanation="'origin' is just a conventional NAME for your primary remote. It's not special—you could call it 'github' or 'server', but everyone uses 'origin'.",
            choices=["a) A special Git keyword", "b) A conventional name for the default remote", "c) The name of the main branch"],
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Add a remote named 'origin'.",
                 answers=["git remote add origin <url>", "git remote add origin https://github.com/user/repo.git"],
                 explanation="This creates the connection between your local repo and a remote server. Run it once when setting up GitHub/GitLab."),
        Exercise(type="recall", prompt="Show configured remotes with URLs.", answers=["git remote -v"],
                 explanation="Always check this after adding a remote to verify the URL is correct."),
        Exercise(type="recall", prompt="Change the URL of origin.",
                 answers=["git remote set-url origin <url>", "git remote set-url origin https://github.com/user/repo.git"],
                 explanation="Use set-url when you move your repo to a different account or fix a typo in the URL."),
        Exercise(type="recall", prompt="Verify remote setup.", answers=["git remote -v"],
                 explanation="The -v flag is crucial—without it you only see names, not URLs."),
        Exercise(type="recall", prompt="Add a remote called 'upstream'.",
                 answers=["git remote add upstream <url>", "git remote add upstream https://github.com/original/repo.git"],
                 explanation="'upstream' is conventional for the original repo when you've forked a project. You can have multiple remotes!"),
        Exercise(type="recall", prompt="List all configured remotes.", answers=["git remote -v", "git remote"],
                 explanation="Without -v you see just names. With -v you see URLs. Both are useful."),
        Exercise(type="recall", prompt="Add remote 'origin' pointing to a GitHub URL.",
                 answers=["git remote add origin <url>", "git remote add origin https://github.com/user/repo.git"],
                 explanation="This is typically the first command after creating an empty repo on GitHub."),
        Exercise(type="recall", prompt="Check remote URLs.", answers=["git remote -v"],
                 explanation="Run this whenever push/pull fails to verify the remote URL is what you expect."),
        Exercise(type="recall", prompt="Fix a wrong remote URL.",
                 answers=["git remote set-url origin <url>", "git remote set-url origin https://github.com/user/repo.git"],
                 explanation="Common when switching from HTTPS (password required) to SSH (key-based)."),
        Exercise(type="recall", prompt="Show remotes.", answers=["git remote -v", "git remote"],
                 explanation="Quick check: 'git remote' for names, 'git remote -v' for full details."),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 12 — Clone
# ═══════════════════════════════════════════════════════════

LEVEL_12 = Level(
    number=12,
    name="Clone",
    tagline="Download a remote repo to your machine.",
    concept=(
        "git clone downloads a full copy of a remote repository.\n"
        "It automatically sets up 'origin' pointing to where you cloned from.\n"
        "You get the full history, all branches, everything."
    ),
    commands_taught=["git clone <url>"],
    teachings=[
        Teaching(
            command="git clone <url>",
            syntax="git clone <repository-url>",
            explanation=(
                "Unlike 'git init' which starts a NEW repo from scratch, 'git clone'\n"
                "downloads an EXISTING repo from a remote server (like GitHub).\n"
                "\n"
                "When you clone:\n"
                "  • A new folder is created with the repo name\n"
                "  • ALL commit history is downloaded\n"
                "  • ALL branches are available\n"
                "  • A remote called 'origin' is automatically set up\n"
                "\n"
                "This is how you start contributing to an existing project."
            ),
            example_output=(
                "$ git clone https://github.com/user/project.git\n"
                "Cloning into 'project'...\n"
                "remote: Enumerating objects: 47, done.\n"
                "remote: Counting objects: 100% (47/47), done.\n"
                "Receiving objects: 100% (47/47), 12.3 KiB, done.\n"
                "Resolving deltas: 100% (15/15), done.\n"
                "\n"
                "$ cd project\n"
                "$ git remote -v\n"
                "origin  https://github.com/user/project.git (fetch)\n"
                "origin  https://github.com/user/project.git (push)"
            ),
            pro_tip="You DON'T need 'git init' after cloning — the repo is already initialized. Running init after clone is a common beginner mistake.",
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="Clone the repo at 'https://github.com/user/project.git'.",
            answers=["git clone https://github.com/user/project.git"],
            explanation="'git clone <url>' downloads a complete copy of a remote repo—all history, branches, and commits. It creates a folder and sets up 'origin' automatically.",
            sim_output="$ git clone https://github.com/user/project.git\nCloning into 'project'...\nremote: Enumerating objects: 47, done.\nremote: Counting objects: 100% (47/47), done.\nremote: Compressing objects: 100% (31/31), done.\nReceiving objects: 100% (47/47), 12.3 KiB, done.\nResolving deltas: 100% (15/15), done.",
        ),
        Exercise(
            type="scenario",
            prompt="After cloning, what TWO commands would you run to verify the remote is set up and see the history?",
            answers=[
                "git remote -v && git log --oneline",
                "git remote -v && git log",
            ],
            explanation="After cloning, check 'git remote -v' to verify the origin connection, and 'git log' to see the commit history. These confirm the clone was successful.",
            sim_output="$ git remote -v\norigin  https://github.com/user/project.git (fetch)\norigin  https://github.com/user/project.git (push)\n\n$ git log --oneline\nabc1234 latest feature\ndef5678 initial commit",
        ),
        Exercise(
            type="multi_choice",
            prompt="What does 'git clone' automatically set up?",
            answers=["c"],
            explanation="Cloning auto-configures 'origin' to point back to the source URL. That's why you can push/pull immediately after cloning without running 'git remote add'.",
            choices=["a) A new branch called 'clone'", "b) A .gitignore file", "c) A remote called 'origin' pointing to the source URL"],
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Clone a repo from a URL.",
                 answers=["git clone <url>", "git clone https://github.com/user/repo.git"],
                 explanation="This is how you join existing projects. Clone once, then work inside the created folder."),
        Exercise(type="recall", prompt="Clone 'https://github.com/team/app.git'.",
                 answers=["git clone https://github.com/team/app.git"],
                 explanation="Replace the URL with any GitHub/GitLab/Bitbucket repository URL. Works for public and private repos (if you have access)."),
        Exercise(type="recall", prompt="Download a remote repository to your machine.",
                 answers=["git clone <url>", "git clone https://github.com/user/repo.git"],
                 explanation="'Download' = 'clone' in Git terminology. You get the full repo, not just the current files."),
        Exercise(type="recall", prompt="Clone a project from GitHub.",
                 answers=["git clone <url>", "git clone https://github.com/user/repo.git"],
                 explanation="Get the clone URL from the green 'Code' button on GitHub. Use HTTPS or SSH depending on your setup."),
        Exercise(type="recall", prompt="Get a copy of a remote repo.",
                 answers=["git clone <url>", "git clone https://github.com/user/repo.git"],
                 explanation="Unlike downloading a ZIP, cloning gives you the full Git history so you can commit and push changes."),
        Exercise(type="recall", prompt="Clone 'https://github.com/org/lib.git'.",
                 answers=["git clone https://github.com/org/lib.git"],
                 explanation="Works for organizations and personal accounts. The URL structure is always github.com/owner/repo.git."),
        Exercise(type="recall", prompt="Download a repo from GitHub.",
                 answers=["git clone <url>", "git clone https://github.com/user/repo.git"],
                 explanation="Don't confuse with GitHub's 'Download ZIP'—cloning keeps Git functionality, ZIP doesn't."),
        Exercise(type="recall", prompt="Clone a teammate's repository.",
                 answers=["git clone <url>", "git clone https://github.com/user/repo.git"],
                 explanation="Collaboration starts with cloning. Make sure you have permission to access the repo (public or added as collaborator)."),
        Exercise(type="recall", prompt="Copy a remote repo locally.",
                 answers=["git clone <url>", "git clone https://github.com/user/repo.git"],
                 explanation="'Local copy' with full history. You can work offline and sync later."),
        Exercise(type="recall", prompt="Clone 'https://github.com/user/api.git'.",
                 answers=["git clone https://github.com/user/api.git"],
                 explanation="After cloning, cd into the created directory to start working."),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 13 — Push
# ═══════════════════════════════════════════════════════════

LEVEL_13 = Level(
    number=13,
    name="Push",
    tagline="Send your commits to the remote.",
    concept=(
        "git push uploads your local commits to the remote repository.\n"
        "First push: git push -u origin main (sets upstream tracking).\n"
        "After that, just 'git push' is enough."
    ),
    commands_taught=["git push -u origin main", "git push", "git push origin <branch>",
                     "git push origin --delete <branch>", "git branch -r"],
    teachings=[
        Teaching(
            command="git push -u origin main",
            syntax="git push -u origin main",
            explanation=(
                "This is the command you run the FIRST time you push to a remote.\n"
                "It does two things:\n"
                "  1. Uploads your 'main' branch to the 'origin' remote\n"
                "  2. Sets up 'upstream tracking' (-u flag) so Git remembers the connection\n"
                "\n"
                "After this, you can just type 'git push' without specifying origin/main."
            ),
            example_output=(
                "$ git push -u origin main\n"
                "Enumerating objects: 15, done.\n"
                "Counting objects: 100% (15/15), done.\n"
                "Writing objects: 100% (15/15), 3.2 KiB, done.\n"
                "Branch 'main' set up to track remote branch 'main' from 'origin'."
            ),
            pro_tip="You only need -u once per branch. After that, just 'git push' works.",
        ),
        Teaching(
            command="git push",
            syntax="git push",
            explanation=(
                "Once upstream tracking is set up (via -u), you can just type 'git push'\n"
                "to upload all new commits from your current branch to the remote.\n"
                "\n"
                "This is the command you'll use most often in daily work."
            ),
            example_output=(
                "$ git push\n"
                "Enumerating objects: 3, done.\n"
                "Writing objects: 100% (3/3), 312 bytes, done.\n"
                "   abc1234..def5678  main -> main"
            ),
        ),
        Teaching(
            command="git push origin <branch>",
            syntax="git push origin <branch-name>",
            explanation=(
                "Push a specific branch to the remote. This is how you share a feature\n"
                "branch with your team. On GitHub, this also makes it available for\n"
                "creating Pull Requests."
            ),
            example_output=(
                "$ git push origin feature-login\n"
                " * [new branch]  feature-login -> feature-login\n"
                "remote: Create a pull request on GitHub:\n"
                "remote:   https://github.com/user/project/pull/new/feature-login"
            ),
        ),
        Teaching(
            command="git push origin --delete <branch>",
            syntax="git push origin --delete <branch-name>",
            explanation=(
                "Deletes a branch on the REMOTE server. This is different from\n"
                "'git branch -d' which only deletes the LOCAL branch.\n"
                "\n"
                "Use this after merging a feature branch to clean up the remote."
            ),
            example_output=(
                "$ git push origin --delete old-feature\n"
                "To https://github.com/user/project.git\n"
                " - [deleted]  old-feature"
            ),
        ),
        Teaching(
            command="git branch -r",
            syntax="git branch -r",
            explanation=(
                "Lists all remote-tracking branches. These are local copies of what\n"
                "exists on the remote. They update when you fetch or pull."
            ),
            example_output=(
                "$ git branch -r\n"
                "  origin/main\n"
                "  origin/feature-login\n"
                "  origin/dev"
            ),
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="Push your local 'main' branch to remote for the first time (set upstream tracking).",
            answers=["git push -u origin main"],
            explanation="The -u flag (--set-upstream) links your local 'main' to 'origin/main'. After this, plain 'git push' knows where to go. Run this once per branch.",
            sim_output="$ git push -u origin main\nEnumerating objects: 15, done.\nCounting objects: 100% (15/15), done.\nWriting objects: 100% (15/15), 3.2 KiB, done.\nBranch 'main' set up to track remote branch 'main' from 'origin'.",
        ),
        Exercise(
            type="recall",
            prompt="Push your commits (upstream already set).",
            answers=["git push"],
            explanation="After setting upstream with -u, just 'git push' is enough. Git remembers which remote and branch to push to.",
            sim_output="$ git push\nEverything up-to-date",
        ),
        Exercise(
            type="recall",
            prompt="Push a branch called 'feature-login' to the remote.",
            answers=["git push origin feature-login"],
            explanation="Pushing a branch makes it available on GitHub/GitLab for others to see and for creating Pull Requests. The branch must exist locally first.",
            sim_output="$ git push origin feature-login\nTotal 3 (delta 1), reused 0\nremote: Create a pull request for 'feature-login' on GitHub by visiting:\nremote:   https://github.com/user/project/pull/new/feature-login\n * [new branch]      feature-login -> feature-login",
        ),
        Exercise(
            type="recall",
            prompt="Delete a remote branch called 'old-feature'.",
            answers=["git push origin --delete old-feature"],
            explanation="'git push origin --delete <branch>' removes the branch from the remote server. Your local copy remains until you run 'git branch -d'. Clean up merged feature branches this way.",
            sim_output="$ git push origin --delete old-feature\nTo https://github.com/user/project.git\n - [deleted]         old-feature",
        ),
        Exercise(
            type="recall",
            prompt="List all remote-tracking branches.",
            answers=["git branch -r"],
            explanation="The -r flag shows remote branches. These are local references to what's on the server—they update when you fetch or pull.",
            sim_output="$ git branch -r\n  origin/main\n  origin/feature-login",
        ),
        Exercise(
            type="error_fix",
            prompt="You ran 'git push' and got this error. What happened and what should you do?",
            error_output="$ git push\nTo https://github.com/user/project.git\n ! [rejected]        main -> main (non-fast-forward)\nerror: failed to push some refs\nhint: Updates were rejected because the remote contains work that you do not have locally.",
            answers=["git pull", "git pull origin main"],
            hint="Your remote has commits you don't have locally. Pull first.",
            explanation="This happens when someone else pushed while you were working. The remote has commits you don't have. Pull their changes first, then push again.",
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="First push to origin main.", answers=["git push -u origin main"],
                 explanation="The first push needs -u to set up tracking. After that, you can just use 'git push'."),
        Exercise(type="recall", prompt="Push commits (upstream set).", answers=["git push"],
                 explanation="This uploads all new local commits to the tracked remote branch."),
        Exercise(type="recall", prompt="Push branch 'feature-chat' to remote.", answers=["git push origin feature-chat"],
                 explanation="Share your feature branch with the team. They can then checkout or review it."),
        Exercise(type="recall", prompt="Delete remote branch 'stale-branch'.", answers=["git push origin --delete stale-branch"],
                 explanation="After merging a feature, delete the remote branch to keep things tidy."),
        Exercise(type="recall", prompt="List remote branches.", answers=["git branch -r"],
                 explanation="See what branches exist on the remote. Useful for finding feature branches to checkout."),
        Exercise(type="recall", prompt="Push to origin main (first time).", answers=["git push -u origin main"],
                 explanation="Always use -u on the first push of any branch to set up tracking."),
        Exercise(type="recall", prompt="Upload local commits to remote.", answers=["git push"],
                 explanation="Push regularly to back up your work and share progress with the team."),
        Exercise(type="recall", prompt="Push branch 'hotfix' to remote.", answers=["git push origin hotfix"],
                 explanation="Hotfix branches should be pushed so others can review before deployment."),
        Exercise(type="recall", prompt="Delete remote branch 'old-dev'.", answers=["git push origin --delete old-dev"],
                 explanation="Clean up old branches on the server just like you clean up local branches with 'git branch -d'."),
        Exercise(type="recall", prompt="Push all local commits.", answers=["git push"],
                 explanation="Commits are local until you push. Push frequently to avoid losing work if your machine fails."),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 14 — Pull & Fetch
# ═══════════════════════════════════════════════════════════

LEVEL_14 = Level(
    number=14,
    name="Pull & Fetch",
    tagline="Get changes from the remote.",
    concept=(
        "git fetch downloads remote changes WITHOUT merging them.\n"
        "git pull = git fetch + git merge (downloads AND merges).\n"
        "Use fetch when you want to inspect before merging. Use pull for quick sync."
    ),
    commands_taught=["git fetch origin", "git pull", "git pull origin main"],
    teachings=[
        Teaching(
            command="git fetch origin",
            syntax="git fetch origin",
            explanation=(
                "Downloads new commits from the remote server but does NOT change your\n"
                "working files. It's like checking your mailbox without opening the letters.\n"
                "\n"
                "After fetching, you can inspect what's new using:\n"
                "  git log origin/main --oneline\n"
                "\n"
                "Then decide if you want to merge those changes into your branch."
            ),
            example_output=(
                "$ git fetch origin\n"
                "remote: Enumerating objects: 5, done.\n"
                "remote: Counting objects: 100% (5/5), done.\n"
                "From https://github.com/user/project\n"
                "   abc1234..def5678  main -> origin/main\n"
                "\n"
                "$ git log origin/main --oneline\n"
                "def5678 teammate added new feature\n"
                "abc1234 initial commit"
            ),
            pro_tip="Fetch is safe — it never changes your working files. Use it when you want to look before you leap.",
        ),
        Teaching(
            command="git pull",
            syntax="git pull",
            explanation=(
                "This is a shortcut that combines two commands:\n"
                "  1. git fetch (download new commits)\n"
                "  2. git merge (merge them into your current branch)\n"
                "\n"
                "It's the quickest way to sync your local repo with the remote.\n"
                "Use this when you trust the incoming changes and just want to update."
            ),
            example_output=(
                "$ git pull\n"
                "remote: Enumerating objects: 3, done.\n"
                "From https://github.com/user/project\n"
                "   abc1234..def5678  main -> origin/main\n"
                "Updating abc1234..def5678\n"
                "Fast-forward\n"
                " app.py | 3 +++\n"
                " 1 file changed, 3 insertions(+)"
            ),
        ),
        Teaching(
            command="git pull origin main",
            syntax="git pull origin main",
            explanation=(
                "Explicitly pull from 'origin' remote, 'main' branch. This is useful when:\n"
                "  • Upstream tracking isn't set up yet\n"
                "  • You want to pull from a specific branch\n"
                "  • You want to be explicit about where you're pulling from\n"
                "\n"
                "Once tracking is set up, 'git pull' alone does the same thing."
            ),
            example_output=(
                "$ git pull origin main\n"
                "From https://github.com/user/project\n"
                " * branch  main -> FETCH_HEAD\n"
                "Updating abc1234..def5678\n"
                "Fast-forward\n"
                " app.py | 3 +++\n"
                " 1 file changed, 3 insertions(+)"
            ),
            pro_tip="If 'git pull' causes a conflict, resolve it the same way you would a merge conflict.",
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="Download remote changes without merging them.",
            answers=["git fetch", "git fetch origin"],
            explanation="'git fetch' downloads new commits from the remote but doesn't touch your working files. It's the safe way to see what's new before deciding to merge.",
            sim_output="$ git fetch origin\nremote: Enumerating objects: 5, done.\nremote: Counting objects: 100% (5/5), done.\nFrom https://github.com/user/project\n   abc1234..def5678  main -> origin/main",
        ),
        Exercise(
            type="recall",
            prompt="Download AND merge remote changes from 'origin main'.",
            answers=["git pull origin main", "git pull"],
            explanation="'git pull' = fetch + merge. It downloads new commits and immediately merges them into your current branch. Quick but less cautious than fetch.",
            sim_output="$ git pull origin main\nFrom https://github.com/user/project\n * branch  main -> FETCH_HEAD\nUpdating abc1234..def5678\nFast-forward\n app.py | 3 +++\n 1 file changed, 3 insertions(+)",
        ),
        Exercise(
            type="scenario",
            prompt="Your teammate pushed 2 new commits. You want to SEE what changed before merging. What command downloads without merging?",
            answers=["git fetch", "git fetch origin"],
            explanation="Use fetch when you want to inspect changes before merging. After fetching, use 'git log origin/main' to see what's new, then 'git merge origin/main' if you want it.",
            sim_output="(changes downloaded but not merged)",
        ),
        Exercise(
            type="scenario",
            prompt="After fetching, how do you see the new commits on the remote 'main' branch?",
            answers=["git log origin/main --oneline", "git log origin/main", "git log --oneline origin/main"],
            explanation="'origin/main' is a local reference to the remote's main branch. After fetching, check 'git log origin/main' to see what's new before merging.",
            sim_output="$ git log origin/main --oneline\ndef5678 teammate's new feature\nabc1234 initial commit",
        ),
        Exercise(
            type="multi_choice",
            prompt="What's the difference between fetch and pull?",
            answers=["b"],
            explanation="Fetch is safe—it downloads without changing your files. Pull is convenient—it downloads AND merges. Choose based on whether you want to inspect first.",
            choices=["a) fetch is faster", "b) fetch downloads without merging; pull downloads AND merges", "c) pull only works on main"],
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Download remote changes without merging.", answers=["git fetch", "git fetch origin"],
                 explanation="Fetch is your safety net—see what's coming before it hits your code."),
        Exercise(type="recall", prompt="Download and merge remote changes.", answers=["git pull", "git pull origin main"],
                 explanation="Pull is the fast path—when you trust the incoming changes and just want to sync."),
        Exercise(type="recall", prompt="Fetch from origin.", answers=["git fetch origin", "git fetch"],
                 explanation="Run fetch regularly to keep your local tracking branches up-to-date with the server."),
        Exercise(type="recall", prompt="Pull latest from main.", answers=["git pull origin main", "git pull"],
                 explanation="Start your workday with a pull to get everyone else's changes."),
        Exercise(type="recall", prompt="Get remote updates (don't merge yet).", answers=["git fetch", "git fetch origin"],
                 explanation="Fetch before important merges to review what you're about to integrate."),
        Exercise(type="recall", prompt="Sync local with remote (fetch + merge).", answers=["git pull", "git pull origin main"],
                 explanation="Pull can cause merge conflicts if you and a teammate edited the same lines. Be ready to resolve them."),
        Exercise(type="recall", prompt="Download remote commits.", answers=["git fetch", "git fetch origin"],
                 explanation="After fetching, your remote-tracking branches (origin/main, etc) are updated."),
        Exercise(type="recall", prompt="Pull remote changes into your branch.", answers=["git pull", "git pull origin main"],
                 explanation="If pull says 'Already up to date', it means you have all remote commits already."),
        Exercise(type="recall", prompt="Fetch updates from origin.", answers=["git fetch origin", "git fetch"],
                 explanation="Fetch doesn't require a clean working directory—it never touches your local changes."),
        Exercise(type="recall", prompt="Quick sync with remote.", answers=["git pull", "git pull origin main"],
                 explanation="Pull before you push to avoid 'rejected' errors from the server."),
    ],
)


REMOTE_LEVELS = {
    11: LEVEL_11,
    12: LEVEL_12,
    13: LEVEL_13,
    14: LEVEL_14,
}
