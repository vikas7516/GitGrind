"""
GitGrind — 5 Boss Fights (multi-step gauntlets).
"""
from content.models import Exercise, BossFight


# ═══════════════════════════════════════════════════════════
#  BOSS FIGHT 1 — The Broken Repo (after Exercise Round 2)
# ═══════════════════════════════════════════════════════════

BOSS_FIGHT_1 = BossFight(
    number=1,
    name="The Broken Repo",
    tagline="You init'd a project but messed up along the way. Fix it.",
    story=(
        "You started a new project, made a few commits, but then realized\n"
        "you accidentally committed node_modules/ and .env into the repo.\n"
        "Your job: clean it up properly."
    ),
    steps=[
        Exercise(
            type="recall",
            prompt="First, check the current state of the repo.",
            answers=["git status"],
            explanation="Always start with 'git status' to understand what you're working with.",
            sim_output="$ git status\nOn branch main\nnothing to commit, working tree clean\n\n(but node_modules/ and .env are tracked!)",
        ),
        Exercise(
            type="scenario",
            prompt="Create a .gitignore file. What pattern ignores the node_modules directory?",
            answers=["node_modules/", "node_modules"],
            explanation="Add this pattern to .gitignore. Future node_modules won't be tracked, but existing ones need manual removal.",
        ),
        Exercise(
            type="scenario",
            prompt="Add the pattern to also ignore .env files.",
            answers=[".env"],
            explanation="Environment files contain secrets—never commit them! Always gitignore .env files.",
        ),
        Exercise(
            type="recall",
            prompt="Untrack node_modules/ (remove from Git tracking, keep on disk).",
            answers=["git rm --cached -r node_modules/", "git rm --cached -r node_modules",
                     "git rm -r --cached node_modules/", "git rm -r --cached node_modules"],
            explanation="'git rm --cached -r' removes a directory from tracking. The -r flag means recursive. The directory stays on disk.",
            sim_output="$ git rm --cached -r node_modules/\nrm 'node_modules/express/index.js'\nrm 'node_modules/express/package.json'\n...",
        ),
        Exercise(
            type="recall",
            prompt="Untrack .env (remove from Git tracking, keep on disk).",
            answers=["git rm --cached .env"],
            explanation="Same concept—remove from tracking but keep the file. Essential for fixing .gitignore mistakes.",
            sim_output="$ git rm --cached .env\nrm '.env'",
        ),
        Exercise(
            type="recall",
            prompt="Stage the .gitignore file.",
            answers=["git add .gitignore"],
            explanation="Now that .gitignore exists and has patterns, stage it so it's part of the repo.",
        ),
        Exercise(
            type="recall",
            prompt="Now stage ALL the changes (removals + gitignore).",
            answers=["git add .", "git add -A"],
            explanation="The removals are changes too. Stage everything to prepare for commit.",
        ),
        Exercise(
            type="recall",
            prompt="Commit with the message 'cleanup: remove tracked junk, add gitignore'.",
            answers=[
                'git commit -m "cleanup: remove tracked junk, add gitignore"',
                "git commit -m 'cleanup: remove tracked junk, add gitignore'",
            ],
            explanation="Descriptive commit message explains what you fixed. Future you will appreciate this.",
            sim_output='$ git commit -m "cleanup: remove tracked junk, add gitignore"\n[main f1x3d01] cleanup: remove tracked junk, add gitignore\n 150 files changed, 0 insertions(+), 15000 deletions(-)',
        ),
        Exercise(
            type="recall",
            prompt="Verify the cleanup with a compact log.",
            answers=["git log --oneline"],
            explanation="Always verify your work. The cleanup commit should be at the top.",
            sim_output="$ git log --oneline\nf1x3d01 (HEAD -> main) cleanup: remove tracked junk, add gitignore\nabc1234 add app\ndef5678 initial commit",
        ),
    ],
)


# ═══════════════════════════════════════════════════════════
#  BOSS FIGHT 2 — The Three-Way Collision (after Exercise Round 3)
# ═══════════════════════════════════════════════════════════

BOSS_FIGHT_2 = BossFight(
    number=2,
    name="The Three-Way Collision",
    tagline="3 branches all edited the same file. Merge them one by one.",
    story=(
        "You have 3 feature branches: feature-a, feature-b, and feature-c.\n"
        "All three modified app.py. You need to merge them all into main.\n"
        "Expect conflicts. Stay cool."
    ),
    steps=[
        Exercise(
            type="recall",
            prompt="You're on main. First, merge feature-a (this one will be clean).",
            answers=["git merge feature-a"],
            explanation="First merge should be straightforward—no conflicts yet. Make sure you're ON main before merging.",
            sim_output="$ git merge feature-a\nMerge made by the 'ort' strategy.\n app.py | 5 +++++\n 1 file changed, 5 insertions(+)",
        ),
        Exercise(
            type="recall",
            prompt="Good. Now merge feature-b.",
            answers=["git merge feature-b"],
            explanation="Second merge hits a conflict because feature-b also changed app.py. This is where it gets real.",
            sim_output="$ git merge feature-b\nAuto-merging app.py\nCONFLICT (content): Merge conflict in app.py\nAutomatic merge failed; fix conflicts and then commit the result.",
        ),
        Exercise(
            type="scenario",
            prompt="Conflict! You've resolved the conflict in app.py manually. Now stage the resolved file.",
            answers=["git add app.py"],
            explanation="After resolving conflicts (removing <<<< ==== >>>> markers), stage the fixed file. This marks it as resolved.",
        ),
        Exercise(
            type="recall",
            prompt="Complete the merge commit.",
            answers=["git commit"],
            explanation="No need for -m during merge resolution—Git auto-generates a merge commit message.",
            sim_output="$ git commit\n[main m3rg301] Merge branch 'feature-b'",
        ),
        Exercise(
            type="recall",
            prompt="Now merge the last one: feature-c.",
            answers=["git merge feature-c"],
            explanation="Third merge. Brace yourself—multiple files conflicting this time.",
            sim_output="$ git merge feature-c\nAuto-merging app.py\nCONFLICT (content): Merge conflict in app.py\nAuto-merging utils.py\nCONFLICT (content): Merge conflict in utils.py\nAutomatic merge failed; fix conflicts and then commit the result.",
        ),
        Exercise(
            type="recall",
            prompt="Two files have conflicts this time! After resolving both, stage everything.",
            answers=["git add .", "git add -A", "git add app.py utils.py"],
            explanation="When multiple files have conflicts, resolve each one, then stage them all at once.",
        ),
        Exercise(
            type="recall",
            prompt="Complete the final merge commit.",
            answers=["git commit"],
            explanation="Final merge commit. Three branches successfully integrated despite conflicts.",
            sim_output="$ git commit\n[main m3rg302] Merge branch 'feature-c'",
        ),
        Exercise(
            type="recall",
            prompt="Verify the merge graph.",
            answers=["git log --oneline --graph", "git log --oneline --graph --all"],
            explanation="The graph shows how all three branches merged into main. Complex but beautiful when you see it working.",
            sim_output="$ git log --oneline --graph --all\n*   m3rg302 (HEAD -> main) Merge branch 'feature-c'\n|\\  \n| * ccc3333 (feature-c) add feature c\n* |   m3rg301 Merge branch 'feature-b'\n|\\ \\  \n| * | bbb2222 (feature-b) add feature b\n|/ /\n* | aaa1111 Merge branch 'feature-a'\n|\\ \n| * aaa0000 (feature-a) add feature a\n|/\n* 0000000 initial commit",
        ),
        Exercise(
            type="recall",
            prompt="Clean up: delete all 3 feature branches. Use one command per branch (separate with &&).",
            answers=[
                "git branch -d feature-a && git branch -d feature-b && git branch -d feature-c",
            ],
            explanation="After merging, delete the feature branches to keep things tidy. The work is preserved in main's history.",
            sim_output="Deleted branch feature-a\nDeleted branch feature-b\nDeleted branch feature-c",
        ),
        Exercise(
            type="recall",
            prompt="CURVEBALL: Run 'git branch' to verify. Is everything clean?",
            answers=["git branch"],
            explanation="Always verify your cleanup. Sometimes surprises lurk in your branch list.",
            sim_output="$ git branch\n  experiment\n* main\n\nWait... 'experiment' branch is still there!",
        ),
        Exercise(
            type="recall",
            prompt="There's a stray 'experiment' branch! Delete it.",
            answers=["git branch -d experiment", "git branch -D experiment"],
            explanation="Found a stray branch. Clean it up. May need -D if it was never merged.",
            sim_output="$ git branch -d experiment\nDeleted branch experiment.",
        ),
    ],
)


# ═══════════════════════════════════════════════════════════
#  BOSS FIGHT 3 — The Sync Disaster (after Exercise Round 4)
# ═══════════════════════════════════════════════════════════

BOSS_FIGHT_3 = BossFight(
    number=3,
    name="The Sync Disaster",
    tagline="Your local and remote diverged. Untangle it.",
    story=(
        "You have local commits. Your teammate also pushed commits to main.\n"
        "Your push is rejected. You need to sync everything up cleanly."
    ),
    steps=[
        Exercise(
            type="recall",
            prompt="Try to push your commits.",
            answers=["git push", "git push origin main"],
            explanation="First push attempt will fail because remote has commits you don't have. This is a common situation in team projects.",
            sim_output="$ git push\n ! [rejected]        main -> main (non-fast-forward)\nerror: failed to push some refs\nhint: Updates were rejected because the remote contains work you don't have.",
        ),
        Exercise(
            type="recall",
            prompt="Push rejected! First, fetch to see what's on the remote.",
            answers=["git fetch", "git fetch origin"],
            explanation="Fetch downloads the remote commits without merging. Always fetch first to inspect what you're about to merge.",
            sim_output="$ git fetch origin\nremote: Counting objects: 5, done.\nFrom https://github.com/team/project\n   abc1234..def5678  main -> origin/main",
        ),
        Exercise(
            type="recall",
            prompt="Compare your local main log with the remote. Check remote first.",
            answers=["git log origin/main --oneline", "git log --oneline origin/main"],
            explanation="After fetching, you can inspect 'origin/main' to see what your teammate pushed. This helps you understand the incoming changes.",
            sim_output="$ git log origin/main --oneline\ndef5678 teammate's bugfix    <-- you don't have this\nabc1234 initial commit",
        ),
        Exercise(
            type="recall",
            prompt="Now pull to merge the remote changes into your local branch.",
            answers=["git pull", "git pull origin main"],
            explanation="Pull = fetch + merge. Since both you and teammate changed the same file, expect a conflict.",
            sim_output="$ git pull origin main\nAuto-merging app.py\nCONFLICT (content): Merge conflict in app.py\nAutomatic merge failed; fix conflicts and then commit the result.",
        ),
        Exercise(
            type="recall",
            prompt="Conflict during pull! After resolving, stage the file.",
            answers=["git add app.py", "git add .", "git add -A"],
            explanation="Pull conflicts are just like merge conflicts. Resolve, stage, commit.",
        ),
        Exercise(
            type="recall",
            prompt="Complete the merge commit.",
            answers=["git commit"],
            explanation="This merge commit combines your work with your teammate's. Now you're synced.",
            sim_output="$ git commit\n[main syn3c01] Merge branch 'main' of origin",
        ),
        Exercise(
            type="recall",
            prompt="Now try pushing again.",
            answers=["git push", "git push origin main"],
            explanation="After merging, your push will succeed. You have all remote commits plus your new merge commit.",
            sim_output="$ git push\nCounting objects: 8, done.\nTo https://github.com/team/project.git\n   def5678..syn3c01  main -> main",
        ),
        Exercise(
            type="scenario",
            prompt="CURVEBALL: You realize the commit message from the merge was wrong. Fix it.",
            answers=[
                'git commit --amend -m "merge: sync with teammate bugfix"',
                "git commit --amend -m 'merge: sync with teammate bugfix'",
                "git commit --amend",
            ],
            explanation="Amend fixes the last commit. But since you already pushed, you'll need to force push next.",
            sim_output='$ git commit --amend -m "merge: sync with teammate bugfix"\n[main syn3c02] merge: sync with teammate bugfix',
        ),
        Exercise(
            type="recall",
            prompt="After amending, push again (you need to force since you rewrote history).",
            answers=["git push --force-with-lease"],
            explanation="Amending rewrites history. Use --force-with-lease to safely force push. It fails if someone else pushed since your last fetch.",
            sim_output="$ git push --force-with-lease\n + syn3c01...syn3c02 main -> main (forced update)",
        ),
    ],
)


# ═══════════════════════════════════════════════════════════
#  BOSS FIGHT 4 — The Detached HEAD Nightmare (after Exercise Round 5)
# ═══════════════════════════════════════════════════════════

BOSS_FIGHT_4 = BossFight(
    number=4,
    name="The Detached HEAD Nightmare",
    tagline="You accidentally checked out a commit hash. Recover.",
    story=(
        "You ran 'git checkout abc1234' to look at an old commit.\n"
        "Now you're in 'detached HEAD' state. You made 2 commits here.\n"
        "If you just switch branches, those commits will be LOST. Save them."
    ),
    steps=[
        Exercise(
            type="recall",
            prompt="Check your current state. What command shows you're in detached HEAD?",
            answers=["git status"],
            explanation="Detached HEAD means you're not on any branch—you're on a specific commit. Dangerous because commits made here can be lost.",
            sim_output="$ git status\nHEAD detached at abc1234\nnothing to commit, working tree clean",
        ),
        Exercise(
            type="scenario",
            prompt="You've made 2 commits while detached. Create a branch called 'rescue' to save them.",
            answers=["git switch -c rescue", "git checkout -b rescue", "git branch rescue"],
            explanation="Creating a branch while detached saves those commits. The branch points to them so they won't be lost.",
            sim_output="$ git switch -c rescue\nSwitched to a new branch 'rescue'",
        ),
        Exercise(
            type="recall",
            prompt="Good, your commits are saved on 'rescue'. Now switch to main.",
            answers=["git switch main", "git checkout main"],
            explanation="Now that commits are safe on 'rescue', you can return to main.",
            sim_output="$ git switch main\nSwitched to branch 'main'",
        ),
        Exercise(
            type="recall",
            prompt="View the log to find the commit hashes on 'rescue'.",
            answers=["git log rescue --oneline", "git log --oneline rescue"],
            explanation="Check what commits are on 'rescue' so you can cherry-pick the ones you need.",
            sim_output="$ git log rescue --oneline\nxyz9876 second emergency fix\nwvu5432 first emergency fix\nabc1234 original commit",
        ),
        Exercise(
            type="scenario",
            prompt="Cherry-pick the first rescue commit (wvu5432) onto main.",
            answers=["git cherry-pick wvu5432"],
            explanation="Cherry-pick copies a commit from 'rescue' to main. Better than merging if you only want specific commits.",
            sim_output="$ git cherry-pick wvu5432\n[main che1234] first emergency fix\n 1 file changed, 3 insertions(+)",
        ),
        Exercise(
            type="scenario",
            prompt="Cherry-pick the second rescue commit (xyz9876) — CURVEBALL: this one has a conflict!",
            answers=["git cherry-pick xyz9876"],
            explanation="Cherry-picking can cause conflicts just like merge. When it does, resolve and continue.",
            sim_output="$ git cherry-pick xyz9876\nAuto-merging app.py\nCONFLICT (content): Merge conflict in app.py\nerror: could not apply xyz9876",
        ),
        Exercise(
            type="recall",
            prompt="Resolve the conflict (already done). Stage the fixed file.",
            answers=["git add app.py", "git add .", "git add -A"],
            explanation="After resolving cherry-pick conflicts, stage like normal.",
        ),
        Exercise(
            type="recall",
            prompt="Continue the cherry-pick after resolving.",
            answers=["git cherry-pick --continue"],
            explanation="--continue completes the cherry-pick after conflict resolution.",
            sim_output="$ git cherry-pick --continue\n[main che5678] second emergency fix",
        ),
        Exercise(
            type="recall",
            prompt="Now delete the rescue branch — it's been cherry-picked.",
            answers=["git branch -d rescue", "git branch -D rescue"],
            explanation="Once you've cherry-picked what you needed, the rescue branch can be deleted. The commits are now on main.",
            sim_output="$ git branch -d rescue\nDeleted branch rescue.",
        ),
        Exercise(
            type="recall",
            prompt="Verify everything with the log graph.",
            answers=["git log --oneline --graph", "git log --oneline --graph --all", "git log --oneline"],
            explanation="Always verify your recovery worked. The cherry-picked commits should be on main.",
            sim_output="$ git log --oneline --graph\n* che5678 (HEAD -> main) second emergency fix\n* che1234 first emergency fix\n* original commits...",
        ),
    ],
)


# ═══════════════════════════════════════════════════════════
#  BOSS FIGHT 5 — THE FINAL BOSS (last stage)
# ═══════════════════════════════════════════════════════════

BOSS_FIGHT_5 = BossFight(
    number=5,
    name="THE FINAL BOSS",
    tagline="Full team workflow. Clone to release.",
    story=(
        "You just joined a team. Your task: add an auth feature.\n"
        "Clone the repo, branch, commit, sync with remote, rebase, squash,\n"
        "push, merge, cleanup, and tag the release.\n\n"
        "14 steps. No hints. This is everything you've learned."
    ),
    steps=[
        Exercise(
            type="recall",
            prompt="Step 1: Clone the team repo.",
            answers=["git clone <url>", "git clone https://github.com/team/project.git"],
            explanation="Clone downloads the entire project with history. This is how you join existing projects.",
            sim_output="Cloning into 'project'...\ndone.",
        ),
        Exercise(
            type="recall",
            prompt="Step 2: Create a feature branch 'feature/auth' and switch to it.",
            answers=["git switch -c feature/auth", "git checkout -b feature/auth"],
            explanation="Feature branches isolate your work from main. Use descriptive names that explain what you're building.",
            sim_output="Switched to a new branch 'feature/auth'",
        ),
        Exercise(
            type="recall",
            prompt="Step 3: The project has no .gitignore! Add one and commit it.\nWhat ignore pattern for node_modules?",
            answers=["node_modules/", "node_modules"],
            explanation="First thing in any project: set up .gitignore. Prevents committing dependencies and secrets.",
        ),
        Exercise(
            type="recall",
            prompt="Step 4: Stage and commit the .gitignore with message 'add gitignore'.",
            answers=[
                'git add .gitignore && git commit -m "add gitignore"',
                "git add . && git commit -m 'add gitignore'",
                'git add . && git commit -m "add gitignore"',
            ],
            explanation="Separate commits for infrastructure (like .gitignore) and features make history cleaner.",
            sim_output='[feature/auth abc0001] add gitignore',
        ),
        Exercise(
            type="recall",
            prompt="Step 5: You built the auth feature. Stage all and commit with 'add auth module'.",
            answers=[
                'git add . && git commit -m "add auth module"',
                "git add . && git commit -m 'add auth module'",
                'git add -A && git commit -m "add auth module"',
            ],
            explanation="Main feature commit. Keep it focused on one thing.",
            sim_output='[feature/auth abc0002] add auth module',
        ),
        Exercise(
            type="recall",
            prompt="Step 6: Make one more commit: 'add auth tests'.",
            answers=[
                'git add . && git commit -m "add auth tests"',
                "git add . && git commit -m 'add auth tests'",
            ],
            explanation="Tests deserve their own commit. Makes it clear what's production code vs. test code.",
            sim_output='[feature/auth abc0003] add auth tests',
        ),
        Exercise(
            type="recall",
            prompt="Step 7: Fetch — your teammate pushed to main while you were working.",
            answers=["git fetch", "git fetch origin"],
            explanation="Always fetch before rebasing. This downloads remote changes without affecting your work.",
            sim_output="From https://github.com/team/project\n   000000..111111  main -> origin/main",
        ),
        Exercise(
            type="recall",
            prompt="Step 8: Rebase your feature branch onto the updated remote main.\n(Remember: you fetched but didn't pull, so local main is outdated.)",
            answers=["git rebase origin/main"],
            explanation="Rebase onto origin/main (not local main) because you fetched but didn't pull. This replays your commits on top of the latest remote changes.",
            sim_output="$ git rebase origin/main\nCONFLICT (content): Merge conflict in config.js\nerror: could not apply abc0002",
        ),
        Exercise(
            type="recall",
            prompt="Step 9: Conflict during rebase! After resolving and staging, what continues the rebase?",
            answers=["git rebase --continue"],
            explanation="Rebase conflicts are common when team members touch the same files. Resolve, stage, continue.",
            sim_output="$ git rebase --continue\nSuccessfully rebased and updated refs/heads/feature/auth.",
        ),
        Exercise(
            type="recall",
            prompt="Step 10: Squash your 3 commits into 1 clean commit using interactive rebase.",
            answers=["git rebase -i HEAD~3"],
            explanation="Before submitting a PR, squash messy WIP commits into one clean commit. Makes review easier and history cleaner.",
            sim_output="(editor: pick first, squash the other 2, save)\n[feature/auth sqsh001] add auth feature with tests",
        ),
        Exercise(
            type="recall",
            prompt="Step 11: Push your feature branch to the remote.",
            answers=["git push origin feature/auth", "git push -u origin feature/auth"],
            explanation="Push the branch so teammates can review it and create a Pull Request on GitHub.",
            sim_output="To https://github.com/team/project.git\n * [new branch]      feature/auth -> feature/auth",
        ),
        Exercise(
            type="recall",
            prompt="Step 12: PR is merged! Switch to main and pull the latest.",
            answers=[
                "git switch main && git pull",
                "git checkout main && git pull",
                "git switch main && git pull origin main",
                "git checkout main && git pull origin main",
            ],
            explanation="After PR merges, update your local main. You'll see your feature now integrated into main.",
            sim_output="Switched to branch 'main'\nUpdating... Fast-forward.\n auth.py | 50 +++\n 1 file changed",
        ),
        Exercise(
            type="recall",
            prompt="Step 13: Delete feature/auth locally AND on the remote (separate with &&).",
            answers=[
                "git branch -d feature/auth && git push origin --delete feature/auth",
            ],
            explanation="Clean up merged branches both locally and remotely. Keeps the repo tidy.",
            sim_output="Deleted branch feature/auth.\nTo https://github.com/team/project.git\n - [deleted]  feature/auth",
        ),
        Exercise(
            type="recall",
            prompt="Step 14: Tag this release as 'v2.0' with message 'Auth feature release' and push the tag.",
            answers=[
                'git tag -a v2.0 -m "Auth feature release" && git push origin v2.0',
                "git tag -a v2.0 -m 'Auth feature release' && git push origin v2.0",
            ],
            explanation="Tags mark important releases. Push them separately—they don't go with regular pushes. You did it! Full professional workflow complete.",
            sim_output='$ git tag -a v2.0 -m "Auth feature release"\n$ git push origin v2.0\n * [new tag]  v2.0 -> v2.0\n\n🎉 RELEASE COMPLETE!',
        ),
    ],
)


# ═══════════════════════════════════════════════════════════
#  BOSS FIGHT 6 — COMMAND ARENA (ultimate final)
# ═══════════════════════════════════════════════════════════

BOSS_FIGHT_6 = BossFight(
    number=6,
    name="COMMAND ARENA — GRAND FINAL",
    tagline="Three phases. Mixed command recall under pressure.",
    story=(
        "This is the final certification gauntlet.\n"
        "Phase 1 checks daily fundamentals, Phase 2 checks collaboration workflows,\n"
        "Phase 3 checks recovery/debugging and release operations.\n"
        "Every step must be correct."
    ),
    steps=[
        Exercise(type="recall", prompt="Phase 1/3 — Foundations: Check repository state.",
                 answers=["git status"], explanation="Always orient yourself first with status."),
        Exercise(type="recall", prompt="Phase 1/3 — Stage all current changes.",
                 answers=["git add .", "git add -A"], explanation="Stage all intended edits before commit."),
        Exercise(type="recall", prompt="Phase 1/3 — Commit with message 'feat: prep release'.",
                 answers=['git commit -m "feat: prep release"', "git commit -m 'feat: prep release'"],
                 explanation="Commit snapshots should have clear intent."),
        Exercise(type="recall", prompt="Phase 1/3 — Show compact history.",
                 answers=["git log --oneline"], explanation="Fast history scan."),
        Exercise(type="recall", prompt="Phase 1/3 — Create and switch to branch feature/finalize.",
                 answers=["git switch -c feature/finalize", "git checkout -b feature/finalize"],
                 explanation="Standard feature branch start."),

        Exercise(type="recall", prompt="Phase 2/3 — Verify remotes with URLs.",
                 answers=["git remote -v"], explanation="Confirm remote wiring before push/pull."),
        Exercise(type="recall", prompt="Phase 2/3 — Fetch and prune stale remote refs.",
                 answers=["git fetch --prune"], explanation="Sync + cleanup remote-tracking refs."),
        Exercise(type="recall", prompt="Phase 2/3 — Rebase onto latest origin/main.",
                 answers=["git rebase origin/main"], explanation="Replay local commits on top of latest remote base."),
        Exercise(type="recall", prompt="Phase 2/3 — Rebase conflict resolved and staged. Continue.",
                 answers=["git rebase --continue"], explanation="Continue rebase after conflict fixes."),
        Exercise(type="recall", prompt="Phase 2/3 — Push feature/finalize and set upstream.",
                 answers=["git push -u origin feature/finalize", "git push origin feature/finalize"],
                 explanation="Publish branch for review."),
        Exercise(type="scenario", prompt="Phase 2/3 — Next team step after push?",
                 answers=["open pull request", "open a pull request", "create pull request", "create a pull request"],
                 explanation="Team workflow goes through PR review."),

        Exercise(type="recall", prompt="Phase 3/3 — Start bisect and mark current as bad.",
                 answers=["git bisect start && git bisect bad"], explanation="Start binary search for regression."),
        Exercise(type="recall", prompt="Phase 3/3 — Mark known good commit a1b2c3d.",
                 answers=["git bisect good a1b2c3d"], explanation="Bisect needs one good and one bad boundary."),
        Exercise(type="recall", prompt="Phase 3/3 — Exit bisect mode.",
                 answers=["git bisect reset"], explanation="Return repository to normal state."),
        Exercise(type="recall", prompt="Phase 3/3 — Squash merge feature/finalize into current branch.",
                 answers=["git merge --squash feature/finalize"], explanation="Integrate many commits as one clean commit."),
        Exercise(type="recall", prompt="Phase 3/3 — Tag release v3.0 with message 'Grand final release'.",
                 answers=['git tag -a v3.0 -m "Grand final release"', "git tag -a v3.0 -m 'Grand final release'"],
                 explanation="Annotated tags mark official releases."),
        Exercise(type="recall", prompt="Phase 3/3 — Push the v3.0 tag to origin.",
                 answers=["git push origin v3.0", "git push --tags"], explanation="Tags are pushed explicitly."),
        Exercise(type="recall", prompt="Phase 3/3 — Final verification command for branch graph.",
                 answers=["git log --oneline --graph", "git log --oneline --graph --all"],
                 explanation="Visual confirmation of final history state.",
                 sim_output="🏆 Certification complete. You cleared the full Git command arena."),
    ],
)


ALL_BOSS_FIGHTS = {
    1: BOSS_FIGHT_1,
    2: BOSS_FIGHT_2,
    3: BOSS_FIGHT_3,
    4: BOSS_FIGHT_4,
    5: BOSS_FIGHT_5,
    6: BOSS_FIGHT_6,
}
