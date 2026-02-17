"""
GitGrind — Git Terminology Glossary.
Plain-English explanations of essential Git jargon.
Shown on first launch and accessible from the main menu.
"""

# Each category is a (category_name, list_of_(term, explanation)) tuple.
GIT_GLOSSARY = [
    ("Core Concepts", [
        (
            "Repository (Repo)",
            "A folder that Git is tracking. It contains all your project files "
            "plus an invisible `.git` folder where Git stores every change ever made."
        ),
        (
            "Commit",
            "A snapshot of your project at a specific moment. Think of it like "
            "pressing 'Save' in a video game — you can always come back to it."
        ),
        (
            "Branch",
            "A parallel timeline of your project. You can create a branch to "
            "experiment with new features without messing up the main code."
        ),
        (
            "Merge",
            "Combining changes from one branch into another. Git figures out "
            "what changed in each branch and weaves them together."
        ),
        (
            "Clone",
            "Making a full copy of a remote repository onto your computer. "
            "You get all the files, all the history — everything."
        ),
    ]),

    ("Working Areas", [
        (
            "Working Directory",
            "The actual files and folders you see and edit on your computer. "
            "This is where you write code before telling Git about it."
        ),
        (
            "Staging Area (Index)",
            "A preparation zone between your working directory and a commit. "
            "You pick which changes to include in the next commit by 'staging' them with `git add`."
        ),
        (
            "HEAD",
            "A pointer to the commit you're currently looking at. Usually it points "
            "to the latest commit on your current branch. If you 'check out' an older commit, "
            "HEAD moves there (this is called 'detached HEAD')."
        ),
    ]),

    ("Everyday Actions", [
        (
            "Push",
            "Uploading your local commits to a remote server (like GitHub). "
            "Other people can then see and pull your changes."
        ),
        (
            "Pull",
            "Downloading new commits from a remote server AND automatically merging "
            "them into your current branch. It's `git fetch` + `git merge` in one step."
        ),
        (
            "Fetch",
            "Downloading new commits from a remote server WITHOUT merging them. "
            "You get to review what changed before deciding to merge."
        ),
        (
            "Checkout / Switch",
            "Moving to a different branch or a specific commit. Think of it as "
            "teleporting to a different timeline of your project."
        ),
        (
            "Stash",
            "Temporarily shelving uncommitted changes so you can work on something else. "
            "Like putting your half-finished work in a drawer — you can take it back out later."
        ),
    ]),

    ("History & Debugging", [
        (
            "Log",
            "A list of all commits in your project, from newest to oldest. "
            "Each entry shows who made the change, when, and a short description."
        ),
        (
            "Diff",
            "A side-by-side comparison showing exactly what lines were added, "
            "removed, or modified between two versions of your code."
        ),
        (
            "Blame",
            "Shows who last edited each line of a file and when. Despite the name, "
            "it's mostly used to understand context, not to blame anyone!"
        ),
        (
            "Reflog",
            "Git's private diary — it records every move HEAD has made. Even if you "
            "accidentally delete a branch, reflog can help you recover it."
        ),
    ]),

    ("Advanced Concepts", [
        (
            "Rebase",
            "Re-applying your commits on top of someone else's work, creating a "
            "clean, linear history. It's like rewriting history to look as if you started "
            "your work after their latest changes."
        ),
        (
            "Cherry-pick",
            "Grabbing a single commit from another branch and applying it to your "
            "current branch. Useful when you only need one specific change, not the whole branch."
        ),
        (
            "Tag",
            "A named label attached to a specific commit, usually used to mark "
            "release versions (e.g., v1.0, v2.3). Unlike branches, tags don't move."
        ),
        (
            "Origin / Remote",
            "A nickname for a remote server where your repo lives (e.g., GitHub). "
            "'Origin' is the default name Git gives to the server you cloned from."
        ),
        (
            "Merge Conflict",
            "When two branches changed the same lines in a file and Git can't "
            "figure out which version to keep. You have to manually pick the right code."
        ),
    ]),
]
