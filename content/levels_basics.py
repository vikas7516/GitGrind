"""
GitGrind — Levels 1-6: Basics (Init through Git Log).
"""
from content.models import Exercise, Level, Teaching


# ═══════════════════════════════════════════════════════════
#  SETUP INTRO LEVEL (Level 0)
# ═══════════════════════════════════════════════════════════

SETUP_LEVEL = Level(
    number=0,
    name="Git Setup",
    tagline="Configure Git before you begin.",
    concept=(
        "Before using Git, you need to set up your identity (name and email).\n"
        "These details get attached to every commit you make, so people know who made changes.\n"
        "You only need to do this once — the settings are saved globally on your computer."
    ),
    commands_taught=["git --version", "git config --global user.name", "git config --global user.email", "git config --list"],
    teachings=[
        Teaching(
            command="git --version",
            syntax="git --version",
            explanation=(
                "This command checks if Git is installed on your system and shows which version you have.\n"
                "If Git is installed, you'll see something like 'git version 2.43.0'.\n"
                "If it says 'command not found', you need to install Git first.\n"
                "\n"
                "Run this anytime you want to verify your Git installation or check the version."
            ),
            example_output=(
                "$ git --version\n"
                "git version 2.43.0.windows.1"
            ),
            pro_tip="If you're getting 'command not found', download Git from git-scm.com and restart your terminal.",
        ),
        Teaching(
            command="git config --global user.name",
            syntax='git config --global user.name "Your Name"',
            explanation=(
                "This sets your name in Git's global configuration.\n"
                "Every commit you make will be tagged with this name, so other developers\n"
                "know who made the changes.\n"
                "\n"
                "The --global flag means this setting applies to ALL repositories on your\n"
                "computer. You only need to set it once.\n"
                "\n"
                "Use your real name or GitHub username — make it professional!"
            ),
            example_output=(
                '$ git config --global user.name "Player One"\n'
                "(no output — config saved)"
            ),
            pro_tip="You can check your current name with: git config user.name",
        ),
        Teaching(
            command="git config --global user.email",
            syntax='git config --global user.email "you@example.com"',
            explanation=(
                "This sets your email address in Git's global configuration.\n"
                "Like your name, this email gets attached to every commit you make.\n"
                "\n"
                "If you're using GitHub, use the SAME email you registered with on GitHub.\n"
                "This ensures your commits are properly linked to your GitHub profile.\n"
                "\n"
                "The --global flag saves it for all your projects on this computer."
            ),
            example_output=(
                '$ git config --global user.email "player@gitgrind.com"\n'
                "(no output — config saved)"
            ),
            pro_tip="If you're worried about privacy, GitHub lets you use a private 'noreply' email address.",
        ),
        Teaching(
            command="git config --list",
            syntax="git config --list",
            explanation=(
                "This displays ALL your Git configuration settings.\n"
                "You'll see your name, email, and many other settings Git uses.\n"
                "\n"
                "Use this to verify your setup or troubleshoot configuration issues.\n"
                "It's also helpful when you forget what email or name you configured."
            ),
            example_output=(
                "$ git config --list\n"
                "user.name=Player One\n"
                "user.email=player@gitgrind.com\n"
                "core.autocrlf=true\n"
                "color.ui=auto\n"
                "..."
            ),
            pro_tip="Too much output? Use 'git config user.name' and 'git config user.email' to check just those specific values.",
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="What command checks if Git is installed on your system?",
            answers=["git --version"],
            hint="Starts with 'git --v...'",
            explanation="'git --version' shows the installed Git version. If Git isn't installed, you'll get an error instead.",
            sim_output="$ git --version\ngit version 2.43.0.windows.1",
        ),
        Exercise(
            type="recall",
            prompt="Set your Git username to 'Player One'.",
            answers=[
                'git config --global user.name "Player One"',
                "git config --global user.name 'Player One'",
                "git config --global user.name Player One",
            ],
            hint="git config --global user.name ...",
            explanation="'git config --global user.name' sets your name for all Git repos on your computer. This name appears on every commit you make.",
            sim_output="$ git config --global user.name \"Player One\"\n(no output — config saved)",
        ),
        Exercise(
            type="recall",
            prompt="Set your Git email to 'player@gitgrind.com'.",
            answers=[
                'git config --global user.email "player@gitgrind.com"',
                "git config --global user.email 'player@gitgrind.com'",
                "git config --global user.email player@gitgrind.com",
            ],
            hint="git config --global user.email ...",
            explanation="'git config --global user.email' sets your email for all repos. Use the same email as your GitHub account to link commits to your profile.",
            sim_output="$ git config --global user.email \"player@gitgrind.com\"\n(no output — config saved)",
        ),
        Exercise(
            type="recall",
            prompt="What command shows all your Git configuration settings?",
            answers=["git config --list", "git config -l"],
            hint="git config --l...",
            explanation="'git config --list' displays all config settings. Great for verifying your setup or troubleshooting.",
            sim_output="$ git config --list\nuser.name=Player One\nuser.email=player@gitgrind.com\ncore.autocrlf=true\n...",
        ),
    ],
    drills=[
        Exercise(
            type="recall",
            prompt="Check your Git version.",
            answers=["git --version"],
            explanation="Shows the version of Git installed on your system.",
            sim_output="git version 2.43.0.windows.1"
        ),
        Exercise(
            type="recall",
            prompt="Set your name to 'Alex Dev'.",
            answers=['git config --global user.name "Alex Dev"', "git config --global user.name 'Alex Dev'", "git config --global user.name Alex Dev"],
            explanation="Configures your identity for all commits.",
            sim_output="(config saved)"
        ),
        Exercise(
            type="recall",
            prompt="List all Git settings.",
            answers=["git config --list", "git config -l"],
            explanation="Shows everything Git has configured.",
            sim_output="user.name=Alex Dev\nuser.email=alex@example.com\n..."
        ),
        Exercise(
            type="recall",
            prompt="Verify Git is installed.",
            answers=["git --version"],
            explanation="Confirms Git is available on your system.",
            sim_output="git version 2.43.0"
        ),
        Exercise(
            type="recall",
            prompt="Set email to 'dev@example.com'.",
            answers=['git config --global user.email "dev@example.com"', "git config --global user.email 'dev@example.com'", "git config --global user.email dev@example.com"],
            explanation="Sets your email globally.",
            sim_output="(config saved)"
        ),
        Exercise(
            type="recall",
            prompt="Show all config values.",
            answers=["git config --list", "git config -l"],
            explanation="Displays your entire Git configuration.",
            sim_output="user.name=...\nuser.email=...\ncore.autocrlf=..."
        ),
        Exercise(
            type="recall",
            prompt="Configure username to 'Sam'.",
            answers=['git config --global user.name "Sam"', "git config --global user.name 'Sam'", "git config --global user.name Sam"],
            explanation="Sets your global username.",
            sim_output="(config saved)"
        ),
        Exercise(
            type="recall",
            prompt="Check Git version number.",
            answers=["git --version"],
            explanation="Shows which version of Git you have.",
            sim_output="git version 2.43.0.windows.1"
        ),
        Exercise(
            type="recall",
            prompt="View configuration list.",
            answers=["git config --list", "git config -l"],
            explanation="Lists all Git settings you've configured.",
            sim_output="user.name=Sam\nuser.email=dev@example.com\n..."
        ),
        Exercise(
            type="recall",
            prompt="Set email to 'you@mail.com'.",
            answers=['git config --global user.email "you@mail.com"', "git config --global user.email 'you@mail.com'", "git config --global user.email you@mail.com"],
            explanation="Configures your global email address.",
            sim_output="(config saved)"
        ),
    ],
    drill_pass=(6, 8),  # Lighter requirement for setup level
)

# Keep backwards compatibility for old code that references SETUP_EXERCISES
SETUP_EXERCISES = SETUP_LEVEL.exercises


# ═══════════════════════════════════════════════════════════
#  LEVEL 1 — Init & Status
# ═══════════════════════════════════════════════════════════

LEVEL_1 = Level(
    number=1,
    name="Init & Status",
    tagline="Create a repo and check its state.",
    concept=(
        "git init creates a new Git repository in your current folder by adding a hidden .git directory.\n"
        "git status shows the current state — what's tracked, staged, or untracked.\n"
        "These two commands are your starting point for every project."
    ),
    commands_taught=["git init", "git status"],
    teachings=[
        Teaching(
            command="git init",
            syntax="git init",
            explanation=(
                "This is the very first command you run when starting a new project with Git.\n"
                "It creates a hidden .git folder inside your current directory. That folder is\n"
                "where Git stores ALL version history, branches, and configuration for your project.\n"
                "You only need to run this once per project."
            ),
            example_output=(
                "$ mkdir my-project\n"
                "$ cd my-project\n"
                "$ git init\n"
                "Initialized empty Git repository in /home/user/my-project/.git/"
            ),
            pro_tip="Running 'git init' in a folder that already has a .git is safe — it won't overwrite anything.",
        ),
        Teaching(
            command="git status",
            syntax="git status",
            explanation=(
                "This shows you the current state of your repository. It tells you:\n"
                "  • Which branch you're on\n"
                "  • Which files have been modified but not staged\n"
                "  • Which files are staged and ready to commit\n"
                "  • Which files are brand new and not tracked yet\n"
                "You'll use this command constantly — it's your dashboard."
            ),
            example_output=(
                "$ git status\n"
                "On branch main\n"
                "\n"
                "No commits yet\n"
                "\n"
                "Untracked files:\n"
                "  (use \"git add <file>...\" to include in what will be committed)\n"
                "        app.py\n"
                "        README.md\n"
                "\n"
                "nothing added to commit but untracked files present"
            ),
            pro_tip="Run 'git status' before every add/commit to make sure you're staging exactly what you intend.",
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="What command creates a new Git repository in the current folder?",
            answers=["git init"],
            hint="Starts with 'git i...'",
            explanation="'git init' initializes (starts) a new Git repository. It creates the .git folder where all your version history is stored. This is always the first command you run in a new project.",
            sim_output="$ git init\nInitialized empty Git repository in /home/user/project/.git/",
        ),
        Exercise(
            type="recall",
            prompt="What command shows the current state of your repository?",
            answers=["git status"],
            hint="Starts with 'git s...'",
            explanation="'git status' shows what's happening in your repo right now: which files are modified, which are staged for commit, and which branch you're on. Use it constantly!",
            sim_output="$ git status\nOn branch main\n\nNo commits yet\n\nnothing to commit (create/copy files and use \"git add\" to track)",
        ),
        Exercise(
            type="multi_choice",
            prompt="What does 'git init' create?",
            answers=["b"],
            explanation="'git init' creates a hidden .git folder in your current directory. This folder stores all version history, branches, and config. GitHub is separate—you'd use 'git remote' to connect to it later.",
            choices=["a) A remote repository on GitHub", "b) A hidden .git folder in your project", "c) A new branch called 'init'"],
        ),
        Exercise(
            type="scenario",
            prompt="You just created a new project folder called 'myapp'. What's the FIRST git command you run inside it?",
            answers=["git init"],
            explanation="Always run 'git init' first to initialize Git tracking. Until you run this, the folder is just a regular folder—Git won't track any changes.",
            sim_output="$ git init\nInitialized empty Git repository in /home/user/myapp/.git/",
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Initialize a new git repository.", answers=["git init"],
                 explanation="'git init' creates the .git folder to start tracking your project.",
                 sim_output="Initialized empty Git repository in /project/.git/"),
        Exercise(type="recall", prompt="Check the state of your repo.", answers=["git status"],
                 explanation="'git status' shows what files are modified, staged, or untracked.",
                 sim_output="On branch main\nnothing to commit, working tree clean"),
        Exercise(type="recall", prompt="Create a new git repo in this folder.", answers=["git init"],
                 explanation="'git init' is always the first step to enable Git in a folder.",
                 sim_output="Initialized empty Git repository in /project/.git/"),
        Exercise(type="recall", prompt="Show what's tracked, staged, or untracked.", answers=["git status"],
                 explanation="'git status' is your dashboard—it shows exactly what's happening in your repo.",
                 sim_output="On branch main\nUntracked files:\n  app.py\n  README.md"),
        Exercise(type="recall", prompt="Start version control for this project.", answers=["git init"],
                 explanation="Version control begins with 'git init'—it sets up the infrastructure to track changes.",
                 sim_output="Initialized empty Git repository in /project/.git/"),
        Exercise(type="recall", prompt="What's the current state of the repo?", answers=["git status"],
                 explanation="'git status' tells you about uncommitted changes, staged files, and your current branch.",
                 sim_output="On branch main\nChanges not staged for commit:\n  modified: app.py"),
        Exercise(type="recall", prompt="Initialize git tracking.", answers=["git init"],
                 explanation="'git init' initializes the repository so Git can track file changes.",
                 sim_output="Initialized empty Git repository in /project/.git/"),
        Exercise(type="recall", prompt="See which files are modified or untracked.", answers=["git status"],
                 explanation="'git status' lists which files have changes and which aren't being tracked yet.",
                 sim_output="On branch main\nUntracked files:\n  index.html"),
        Exercise(type="recall", prompt="Begin a new git repository.", answers=["git init"],
                 explanation="Every Git project starts with 'git init'—think of it as flipping the 'start tracking' switch.",
                 sim_output="Initialized empty Git repository in /project/.git/"),
        Exercise(type="recall", prompt="Check if there are any uncommitted changes.", answers=["git status"],
                 explanation="'git status' shows if you have work that hasn't been committed yet.",
                 sim_output="On branch main\nnothing to commit, working tree clean"),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 2 — Staging Files
# ═══════════════════════════════════════════════════════════

LEVEL_2 = Level(
    number=2,
    name="Staging Files",
    tagline="Move files into the staging area.",
    concept=(
        "Git has 3 zones: Working Directory → Staging Area → Repository.\n"
        "git add moves files from working directory to the staging area.\n"
        "Only staged files get included in the next commit."
    ),
    commands_taught=["git add <file>", "git add ."],
    teachings=[
        Teaching(
            command="git add <file>",
            syntax="git add <filename>",
            explanation=(
                "Git doesn't automatically save your changes. You have to explicitly CHOOSE\n"
                "which changes to include in the next snapshot (commit). This is called 'staging'.\n"
                "\n"
                "Think of it like packing a box before shipping. 'git add' puts a file into the box.\n"
                "Only what's in the box will be saved when you commit."
            ),
            example_output=(
                "$ git add app.py\n"
                "(no output — file staged)\n"
                "\n"
                "$ git status\n"
                "Changes to be committed:\n"
                "  new file:   app.py\n"
                "\n"
                "Changes not staged for commit:\n"
                "  modified:   README.md"
            ),
            pro_tip="You can stage specific files to make focused, clean commits instead of dumping everything in one go.",
        ),
        Teaching(
            command="git add .",
            syntax="git add .",
            explanation=(
                "The dot '.' means 'everything in the current directory and all subdirectories'.\n"
                "This stages ALL changes at once — new files, modified files, and deleted files.\n"
                "\n"
                "It's convenient when you want to commit everything, but be careful — make sure\n"
                "you're not accidentally staging files you don't want (check with 'git status' first!)."
            ),
            example_output=(
                "$ git add .\n"
                "(no output — all files staged)\n"
                "\n"
                "$ git status\n"
                "Changes to be committed:\n"
                "  new file:   app.py\n"
                "  new file:   README.md\n"
                "  new file:   style.css"
            ),
            pro_tip="Always run 'git status' before 'git add .' to make sure you're not staging junk files.",
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="Stage a file called 'app.py' for commit.",
            answers=["git add app.py"],
            hint="git add <filename>",
            explanation="'git add app.py' stages only that file. Staging lets you control exactly what goes into the next commit.",
            sim_output="$ git add app.py\n(no output — file staged)\n\n$ git status\nChanges to be committed:\n  new file: app.py",
        ),
        Exercise(
            type="recall",
            prompt="Stage ALL changed files in the current directory.",
            answers=["git add .", "git add -A", "git add --all"],
            hint="Use a dot to mean 'everything'",
            explanation="The dot stages all changes from your current directory downward. Use 'git status' first so you don't stage accidental files.",
            sim_output="$ git add .\n(no output — all files staged)",
        ),
        Exercise(
            type="scenario",
            prompt="You edited app.py, style.css, and test.py. You only want to stage style.css. What command?",
            answers=["git add style.css"],
            explanation="Use file-specific staging when you want a focused commit. 'git add style.css' stages only style.css and leaves other edits unstaged.",
            sim_output="$ git add style.css\n\n$ git status\nChanges to be committed:\n  modified: style.css\n\nChanges not staged for commit:\n  modified: app.py\n  modified: test.py",
        ),
        Exercise(
            type="multi_choice",
            prompt="'git add .' stages:",
            answers=["c"],
            explanation="'git add .' stages new, modified, and deleted files in the current directory and subdirectories.",
            choices=["a) Only new files", "b) Only modified files", "c) All changes in current directory and subdirectories"],
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Stage the file 'index.html'.", answers=["git add index.html"],
                 explanation="'git add <filename>' stages that specific file for the next commit.",
                 sim_output="(file staged)"),
        Exercise(type="recall", prompt="Stage everything.", answers=["git add .", "git add -A", "git add --all"],
                 explanation="'git add .' stages all changes at once—new, modified, and deleted files.",
                 sim_output="(all files staged)"),
        Exercise(type="recall", prompt="Stage the file 'server.js'.", answers=["git add server.js"],
                 explanation="Type the exact filename after 'git add' to stage it.",
                 sim_output="(file staged)"),
        Exercise(type="recall", prompt="Stage all changes in this directory.", answers=["git add .", "git add -A"],
                 explanation="The dot '.' is shorthand for 'current directory and everything inside'.",
                 sim_output="(all files staged)"),
        Exercise(type="recall", prompt="Stage 'README.md'.", answers=["git add README.md", "git add readme.md"],
                 explanation="File names are case-sensitive on some systems, but Git often handles both.",
                 sim_output="(file staged)"),
        Exercise(type="recall", prompt="Add 'config.json' to the staging area.", answers=["git add config.json"],
                 explanation="'Staging area' and 'index' mean the same thing—it's where files wait before committing.",
                 sim_output="(file staged)"),
        Exercise(type="recall", prompt="Stage all files at once.", answers=["git add .", "git add -A", "git add --all"],
                 explanation="Use 'git add .' when you want to stage everything in one command.",
                 sim_output="(all files staged)"),
        Exercise(type="recall", prompt="Stage the file 'utils.py'.", answers=["git add utils.py"],
                 explanation="'git add' followed by a filename stages just that file.",
                 sim_output="(file staged)"),
        Exercise(type="recall", prompt="Add 'main.css' to staging.", answers=["git add main.css"],
                 explanation="Staging prepares files for the next commit—think of it as packing a box.",
                 sim_output="(file staged)"),
        Exercise(type="recall", prompt="Stage every change in the project.", answers=["git add .", "git add -A"],
                 explanation="'git add .' from the project root stages everything, everywhere.",
                 sim_output="(all files staged)"),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 3 — Committing
# ═══════════════════════════════════════════════════════════

LEVEL_3 = Level(
    number=3,
    name="Committing",
    tagline="Save snapshots of your code.",
    concept=(
        "git commit saves a snapshot of everything in the staging area.\n"
        "Always use -m to add a message describing what changed.\n"
        "git log shows the history of all commits."
    ),
    commands_taught=["git commit -m", "git log", "git log --oneline"],
    teachings=[
        Teaching(
            command="git commit -m",
            syntax='git commit -m "your message here"',
            explanation=(
                "A commit is a permanent snapshot of your staged changes. Think of it as a save\n"
                "point in a video game — you can always go back to it later.\n"
                "\n"
                "The -m flag lets you write a short description of what you changed. This message\n"
                "is extremely important — it helps you (and your team) understand what each change\n"
                "was about when you look at the history later."
            ),
            example_output=(
                '$ git commit -m "add login page"\n'
                "[main a1b2c3d] add login page\n"
                " 2 files changed, 48 insertions(+)\n"
                " create mode 100644 login.html\n"
                " create mode 100644 login.css"
            ),
            pro_tip="Write commit messages in the imperative: 'add feature' not 'added feature'. Keep them short but descriptive.",
        ),
        Teaching(
            command="git log",
            syntax="git log",
            explanation=(
                "This shows you the full history of all commits in the current branch.\n"
                "For each commit, you'll see:\n"
                "  • The commit hash (a unique ID like a1b2c3d...)\n"
                "  • The author name and email\n"
                "  • The date and time\n"
                "  • The commit message\n"
                "\n"
                "Press 'q' to exit the log viewer if the history is long."
            ),
            example_output=(
                "$ git log\n"
                "commit a1b2c3d (HEAD -> main)\n"
                "Author: Player One <player@gitgrind.com>\n"
                "Date:   Wed Feb 12 12:00:00 2026\n"
                "\n"
                "    add login page\n"
                "\n"
                "commit e4f5g6h\n"
                "Author: Player One <player@gitgrind.com>\n"
                "Date:   Wed Feb 12 11:00:00 2026\n"
                "\n"
                "    initial commit"
            ),
            pro_tip="Press 'q' to exit the log if it takes over the terminal. Don't panic!",
        ),
        Teaching(
            command="git log --oneline",
            syntax="git log --oneline",
            explanation=(
                "This is a compact version of 'git log'. Instead of showing full details for each\n"
                "commit, it shows just the short hash and the commit message — one line per commit.\n"
                "\n"
                "This is the version you'll use most often in practice because it's fast and scannable."
            ),
            example_output=(
                "$ git log --oneline\n"
                "a1b2c3d (HEAD -> main) add login page\n"
                "e4f5g6h initial commit"
            ),
            pro_tip="Combine with other flags: 'git log --oneline --graph' shows branches visually.",
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="Commit staged files with the message 'initial commit'.",
            answers=[
                'git commit -m "initial commit"',
                "git commit -m 'initial commit'",
            ],
            hint="git commit -m \"message\"",
            explanation="'git commit -m' saves a snapshot of everything already staged. The message should clearly describe the change.",
            sim_output="$ git commit -m \"initial commit\"\n[main (root-commit) a1b2c3d] initial commit\n 3 files changed, 42 insertions(+)\n create mode 100644 app.py\n create mode 100644 README.md\n create mode 100644 .gitignore",
        ),
        Exercise(
            type="recall",
            prompt="View the full commit history.",
            answers=["git log"],
            explanation="'git log' shows full commit metadata: hash, author, date, and message. It's your timeline of repository history.",
            sim_output="$ git log\ncommit a1b2c3d (HEAD -> main)\nAuthor: Player One <player@gitgrind.com>\nDate:   Wed Feb 12 12:00:00 2026\n\n    initial commit",
        ),
        Exercise(
            type="recall",
            prompt="View commit history in compact one-line format.",
            answers=["git log --oneline"],
            explanation="'git log --oneline' is the quickest way to scan history: one line per commit with short hash + message.",
            sim_output="$ git log --oneline\na1b2c3d (HEAD -> main) initial commit",
        ),
        Exercise(
            type="error_fix",
            prompt="You ran 'git commit -m \"fix bug\"' but got this error. What did you forget to do?",
            answers=["git add .", "git add <file>", "git add"],
            error_output="$ git commit -m \"fix bug\"\nOn branch main\nnothing to commit, working tree clean",
            hint="Files need to be staged before committing",
            explanation="Commit only includes staged changes. If nothing is staged, Git says 'nothing to commit'. Run 'git add' first.",
        ),
        Exercise(
            type="scenario",
            prompt="You edited app.py. Commit it with the message 'fix login bug'. What TWO commands do you run (separated by &&)?",
            answers=[
                'git add app.py && git commit -m "fix login bug"',
                "git add app.py && git commit -m 'fix login bug'",
                "git add . && git commit -m \"fix login bug\"",
                "git add . && git commit -m 'fix login bug'",
            ],
            explanation="The standard flow is stage first, then commit. You can stage a single file for precision or all files if intended.",
            sim_output="$ git add app.py\n$ git commit -m \"fix login bug\"\n[main e4f5g6h] fix login bug\n 1 file changed, 5 insertions(+), 2 deletions(-)",
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Commit with message 'add homepage'.",
                 answers=['git commit -m "add homepage"', "git commit -m 'add homepage'"],
                 explanation="Write descriptive commit messages that explain what you changed. Use -m to add the message inline.",
                 sim_output="[main abc1234] add homepage"),
        Exercise(type="recall", prompt="View commit history.", answers=["git log"],
                 explanation="'git log' shows all commits in chronological order (newest first). Essential for seeing project history.",
                 sim_output="commit abc1234 (HEAD -> main)\n..."),
        Exercise(type="recall", prompt="Commit with message 'fix navbar'.",
                 answers=['git commit -m "fix navbar"', "git commit -m 'fix navbar'"],
                 explanation="Commit messages should be concise but clear. 'fix navbar' tells you exactly what this commit does.",
                 sim_output="[main def5678] fix navbar"),
        Exercise(type="recall", prompt="View compact log.", answers=["git log --oneline"],
                 explanation="--oneline is the most commonly used log format—quick to read, shows the essentials.",
                 sim_output="def5678 fix navbar\nabc1234 add homepage"),
        Exercise(type="recall", prompt="Commit with message 'update readme'.",
                 answers=['git commit -m "update readme"', "git commit -m 'update readme'"],
                 explanation="Every commit needs a message. Make it descriptive enough that you'll understand it months later.",
                 sim_output="[main ghi9012] update readme"),
        Exercise(type="recall", prompt="Show all previous commits.", answers=["git log"],
                 explanation="'git log' is how you review what work has been done. Think of it as reading your project's diary.",
                 sim_output="commit ghi9012 (HEAD -> main)\n..."),
        Exercise(type="recall", prompt="Commit with message 'add tests'.",
                 answers=['git commit -m "add tests"', "git commit -m 'add tests'"],
                 explanation="Commit after each logical unit of work. 'add tests' is a perfect example—one clear purpose.",
                 sim_output="[main jkl3456] add tests"),
        Exercise(type="recall", prompt="See history in one-line format.", answers=["git log --oneline"],
                 explanation="When you need to quickly scan history, --oneline is your best friend. One commit = one line.",
                 sim_output="jkl3456 add tests\nghi9012 update readme\ndef5678 fix navbar\nabc1234 add homepage"),
        Exercise(type="recall", prompt="Commit with message 'refactor auth'.",
                 answers=['git commit -m "refactor auth"', "git commit -m 'refactor auth'"],
                 explanation="'refactor' is a great word for commits where you improved code without changing functionality.",
                 sim_output="[main mno7890] refactor auth"),
        Exercise(type="recall", prompt="Commit with message 'initial setup'.",
                 answers=['git commit -m "initial setup"', "git commit -m 'initial setup'"],
                 explanation="The first commit is often called 'initial commit' or 'initial setup'. It's tradition!",
                 sim_output="[main pqr1234] initial setup"),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 4 — .gitignore
# ═══════════════════════════════════════════════════════════

LEVEL_4 = Level(
    number=4,
    name=".gitignore",
    tagline="Tell Git what to never track.",
    concept=(
        "A .gitignore file lists patterns of files Git should ignore.\n"
        "Common patterns: *.log, node_modules/, .env, __pycache__/\n"
        "If a file is already tracked, gitignore won't help — you need git rm --cached first."
    ),
    commands_taught=[".gitignore", "git rm --cached"],
    teachings=[
        Teaching(
            command=".gitignore",
            syntax="Create a file called .gitignore in your project root",
            explanation=(
                "Some files should NEVER be committed to Git:\n"
                "  • Secrets: .env files with API keys and passwords\n"
                "  • Dependencies: node_modules/, vendor/ (too large, can be reinstalled)\n"
                "  • Build artifacts: dist/, __pycache__/, *.pyc\n"
                "  • OS junk: .DS_Store, Thumbs.db\n"
                "\n"
                "The .gitignore file is a plain text file where each line is a pattern.\n"
                "Git will completely ignore any files matching these patterns."
            ),
            example_output=(
                "$ cat .gitignore\n"
                "# Dependencies\n"
                "node_modules/\n"
                "\n"
                "# Environment files\n"
                ".env\n"
                "\n"
                "# Logs\n"
                "*.log\n"
                "\n"
                "# Python cache\n"
                "__pycache__/\n"
                "*.pyc\n"
                "\n"
                "# OS files\n"
                ".DS_Store"
            ),
            pro_tip="Create .gitignore BEFORE your first commit. It's much easier than un-tracking files later.",
        ),
        Teaching(
            command="git rm --cached",
            syntax="git rm --cached <file>",
            explanation=(
                "What if you already committed a file and THEN added it to .gitignore?\n"
                "The .gitignore rule won't help — Git is already tracking that file.\n"
                "\n"
                "Use 'git rm --cached <file>' to STOP tracking it without deleting the actual file\n"
                "from your disk. The file stays on your computer but Git forgets about it.\n"
                "After this, the .gitignore rule will take effect."
            ),
            example_output=(
                "$ git rm --cached .env\n"
                "rm '.env'\n"
                "\n"
                "$ git status\n"
                "Changes to be committed:\n"
                "  deleted:   .env       (removed from tracking, file still on disk)\n"
                "\n"
                "Untracked files:\n"
                "  .env                  (now ignored by .gitignore)"
            ),
            pro_tip="Without --cached, 'git rm' deletes the file from BOTH Git AND your disk. Always use --cached to keep the file.",
        ),
    ],
    exercises=[
        Exercise(
            type="scenario",
            prompt="You want Git to ignore all .log files. What line do you add to .gitignore?",
            answers=["*.log"],
            explanation="'*.log' is a wildcard pattern meaning any filename ending in .log should be ignored.",
            sim_output=".gitignore:\n*.log\n\n$ git status\n(log files no longer show as untracked)",
        ),
        Exercise(
            type="scenario",
            prompt="You want to ignore the entire node_modules/ directory. What pattern?",
            answers=["node_modules/", "node_modules"],
            explanation="Directory patterns like 'node_modules/' prevent huge dependency folders from polluting commits.",
            sim_output=".gitignore:\nnode_modules/\n\n$ git status\n(node_modules no longer listed)",
        ),
        Exercise(
            type="scenario",
            prompt="You want to ignore .env files (they contain secrets). What pattern?",
            answers=[".env"],
            explanation="'.env' files often contain API keys and credentials, so they should never be version-controlled.",
            sim_output=".gitignore:\n.env",
        ),
        Exercise(
            type="error_fix",
            prompt="You added .env to .gitignore but 'git status' STILL shows it as tracked. It was committed before you added the rule. How do you fix this?",
            answers=["git rm --cached .env"],
            error_output="$ git status\nChanges not staged for commit:\n  modified: .env",
            hint="You need to remove it from tracking (but keep the file on disk)",
            explanation=".gitignore only affects untracked files. For already-tracked files, remove from index with 'git rm --cached'.",
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Ignore pattern for all .log files.", answers=["*.log"],
                 explanation="'*.log' uses wildcard matching—the * means 'any filename' ending in .log."),
        Exercise(type="recall", prompt="Ignore pattern for node_modules directory.", answers=["node_modules/", "node_modules"],
                 explanation="node_modules/ can be huge (thousands of files). Always gitignore it—you can reinstall dependencies anytime."),
        Exercise(type="recall", prompt="Ignore pattern for .env file.", answers=[".env"],
                 explanation=".env files contain secrets like API keys. Committing them is a security risk. Always ignore them!"),
        Exercise(type="recall", prompt="Ignore pattern for Python cache.", answers=["__pycache__/", "__pycache__"],
                 explanation="__pycache__/ is Python's compiled bytecode. It's auto-generated, so no need to track it."),
        Exercise(type="recall", prompt="Untrack a file called 'secrets.txt' that's already been committed (keep file on disk).",
                 answers=["git rm --cached secrets.txt"],
                 explanation="The --cached flag means 'remove from Git but keep the actual file'. Without it, the file gets deleted!",
                 sim_output="rm 'secrets.txt'\n(file removed from tracking, still exists on disk)"),
        Exercise(type="recall", prompt="Ignore all .tmp files.", answers=["*.tmp"],
                 explanation="Temporary files (*.tmp) are often created by programs and should never be committed."),
        Exercise(type="recall", prompt="Ignore pattern for the dist/ build folder.", answers=["dist/", "dist"],
                 explanation="Build outputs like dist/ are generated from source code, so they don't belong in version control."),
        Exercise(type="recall", prompt="Untrack the already-committed file '.env' (keep on disk).",
                 answers=["git rm --cached .env"],
                 explanation="Common mistake: committing .env by accident. Use 'git rm --cached' to fix it without losing the file.",
                 sim_output="rm '.env'"),
        Exercise(type="recall", prompt="Ignore all files ending in .pyc.", answers=["*.pyc"],
                 explanation=".pyc files are Python compiled bytecode. They're regenerated automatically, so ignore them."),
        Exercise(type="recall", prompt="Ignore pattern for .DS_Store (macOS junk).", answers=[".DS_Store"],
                 explanation=".DS_Store is a macOS system file that stores folder view preferences. It's useless in Git."),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 5 — Seeing Changes (git diff)
# ═══════════════════════════════════════════════════════════

LEVEL_5 = Level(
    number=5,
    name="Seeing Changes",
    tagline="What changed? Where? How?",
    concept=(
        "git diff shows line-by-line changes in your working directory (unstaged).\n"
        "git diff --staged shows changes that are staged and ready to commit.\n"
        "Lines starting with + are additions, - are deletions."
    ),
    commands_taught=["git diff", "git diff --staged"],
    teachings=[
        Teaching(
            command="git diff",
            syntax="git diff",
            explanation=(
                "This shows you exactly what changed in your files, line by line.\n"
                "It compares your working directory (what you've edited) against the staging area.\n"
                "\n"
                "In the output:\n"
                "  • Lines starting with '+' (green) are lines you ADDED\n"
                "  • Lines starting with '-' (red) are lines you DELETED\n"
                "  • Lines with no prefix are unchanged context lines\n"
                "\n"
                "If you see no output, it means either there are no changes, or all changes\n"
                "are already staged (use --staged to see those)."
            ),
            example_output=(
                "$ git diff\n"
                "diff --git a/app.py b/app.py\n"
                "--- a/app.py\n"
                "+++ b/app.py\n"
                "@@ -1,3 +1,4 @@\n"
                " import os\n"
                "+import sys\n"
                " \n"
                " def main():\n"
                "-    print('hello')\n"
                "+    print('hello world')"
            ),
            pro_tip="Use 'git diff' before 'git add' to review exactly what you're about to stage.",
        ),
        Teaching(
            command="git diff --staged",
            syntax="git diff --staged",
            explanation=(
                "After you run 'git add', your changes move to the staging area.\n"
                "Regular 'git diff' won't show them anymore because they're staged.\n"
                "\n"
                "Use 'git diff --staged' to see what's about to go into the next commit.\n"
                "This is your final review before committing — think of it as a preview."
            ),
            example_output=(
                "$ git diff --staged\n"
                "diff --git a/app.py b/app.py\n"
                "--- a/app.py\n"
                "+++ b/app.py\n"
                "@@ -1,3 +1,4 @@\n"
                " import os\n"
                "+import sys"
            ),
            pro_tip="'git diff --cached' does the exact same thing — it's just an alias for --staged.",
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="View unstaged changes in your files.",
            answers=["git diff"],
            hint="Just two words...",
            explanation="'git diff' shows edits in your working directory that are not staged yet.",
            sim_output="$ git diff\ndiff --git a/app.py b/app.py\n--- a/app.py\n+++ b/app.py\n@@ -1,3 +1,4 @@\n import os\n+import sys\n \n def main():\n-    print('hello')\n+    print('hello world')",
        ),
        Exercise(
            type="recall",
            prompt="View changes that are already staged (ready to be committed).",
            answers=["git diff --staged", "git diff --cached"],
            explanation="Use '--staged' (or '--cached') to preview exactly what will be included in the next commit.",
            sim_output="$ git diff --staged\ndiff --git a/app.py b/app.py\n--- a/app.py\n+++ b/app.py\n@@ -1,3 +1,4 @@\n+import sys",
        ),
        Exercise(
            type="scenario",
            prompt="You modified a file and staged it. Now you want to see what will go into the next commit. What command?",
            answers=["git diff --staged", "git diff --cached"],
            explanation="Once staged, regular 'git diff' won't show it. Use 'git diff --staged' for the commit preview.",
            sim_output="(shows staged diff)",
        ),
        Exercise(
            type="multi_choice",
            prompt="In diff output, what does a line starting with '+' mean?",
            answers=["b"],
            explanation="A '+' line is an added line in the new version of the file. '-' lines are deletions.",
            choices=["a) The line was deleted", "b) The line was added", "c) The line was unchanged"],
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Show unstaged changes.", answers=["git diff"],
                 explanation="Unstaged = modified but not added yet. 'git diff' shows these."),
        Exercise(type="recall", prompt="Show staged changes.", answers=["git diff --staged", "git diff --cached"],
                 explanation="Staged = already added and waiting to commit. Use --staged to see them."),
        Exercise(type="recall", prompt="See what's changed but not yet staged.", answers=["git diff"],
                 explanation="'git diff' is perfect for reviewing your edits before deciding what to stage."),
        Exercise(type="recall", prompt="See what's about to be committed.", answers=["git diff --staged", "git diff --cached"],
                 explanation="Always check --staged before committing to make sure you're not committing something by mistake."),
        Exercise(type="recall", prompt="View line-by-line changes in working directory.", answers=["git diff"],
                 explanation="'git diff' shows exactly which lines changed, making it easy to spot typos or bugs."),
        Exercise(type="recall", prompt="View changes in the staging area.", answers=["git diff --staged", "git diff --cached"],
                 explanation="The staging area is like a preview. --staged shows what that preview looks like."),
        Exercise(type="recall", prompt="What's different since my last add?", answers=["git diff"],
                 explanation="If you edited files after running 'git add', 'git diff' shows the new changes."),
        Exercise(type="recall", prompt="Show what I've staged so far.", answers=["git diff --staged", "git diff --cached"],
                 explanation="Staging is deliberate—you choose what to commit. --staged lets you verify your choices."),
        Exercise(type="recall", prompt="Check for modifications before staging.", answers=["git diff"],
                 explanation="Smart workflow: edit → diff (review) → add → diff --staged (final review) → commit."),
        Exercise(type="recall", prompt="Preview what the next commit will contain.", answers=["git diff --staged", "git diff --cached"],
                 explanation="Think of --staged as a 'commit preview'. It shows exactly what will be saved."),
    ],
)


# ═══════════════════════════════════════════════════════════
#  LEVEL 6 — Reading History (git log deep-dive)
# ═══════════════════════════════════════════════════════════

LEVEL_6 = Level(
    number=6,
    name="Reading History",
    tagline="git log has many faces. Learn them all.",
    concept=(
        "git log is your most-used investigation tool.\n"
        "Flags like --oneline, --graph, --author, --since, --grep, --stat\n"
        "let you slice and filter commit history in powerful ways."
    ),
    commands_taught=["git log --oneline", "git log --graph", "git log --author", "git log --since", "git log --grep", "git log --stat"],
    teachings=[
        Teaching(
            command="git log --stat",
            syntax="git log --stat",
            explanation=(
                "The --stat flag adds a summary of which files changed in each commit\n"
                "and how many lines were added or deleted. It's great for understanding\n"
                "the scope of changes without reading the full diff."
            ),
            example_output=(
                "$ git log --stat\n"
                "commit a1b2c3d (HEAD -> main)\n"
                "Author: Player One <player@gitgrind.com>\n"
                "\n"
                "    fix login bug\n"
                "\n"
                " app.py  | 5 +++--\n"
                " test.py | 3 +++\n"
                " 2 files changed, 6 insertions(+), 2 deletions(-)"
            ),
        ),
        Teaching(
            command="git log --graph",
            syntax="git log --oneline --graph",
            explanation=(
                "The --graph flag draws a text-based visual of your branch structure.\n"
                "Combined with --oneline, it gives you a compact, visual overview of\n"
                "how branches diverged and merged. Essential when working with branches."
            ),
            example_output=(
                "$ git log --oneline --graph --all\n"
                "* a1b2c3d (HEAD -> main) merge feature\n"
                "|\\  \n"
                "| * d4e5f6g (feature) add signup\n"
                "| * h8i9j0k add login\n"
                "|/  \n"
                "* e4f5g6h add homepage\n"
                "* i7j8k9l initial commit"
            ),
            pro_tip="Add --all to see ALL branches, not just the current one.",
        ),
        Teaching(
            command="git log --author",
            syntax='git log --author="name"',
            explanation=(
                "Filter commits by author name. Useful in team projects when you want\n"
                "to see only your own commits, or review what a teammate did.\n"
                "The filter uses partial matching — 'John' matches 'John Doe'."
            ),
            example_output=(
                '$ git log --author="Alice"\n'
                "commit x9y8z7w\n"
                "Author: Alice <alice@team.com>\n"
                "\n"
                "    add user dashboard\n"
                "\n"
                "commit p3q2r1s\n"
                "Author: Alice <alice@team.com>\n"
                "\n"
                "    fix navbar styling"
            ),
        ),
        Teaching(
            command="git log --since",
            syntax='git log --since="time expression"',
            explanation=(
                "Filter commits by date. You can use natural language expressions like:\n"
                "  • '2 weeks ago'\n"
                "  • 'yesterday'\n"
                "  • '2026-01-01'\n"
                "\n"
                "Great for standup meetings — 'what did I do since yesterday?'"
            ),
            example_output=(
                '$ git log --since="yesterday"\n'
                "commit a1b2c3d\n"
                "    fix login bug\n"
                "\n"
                "commit e4f5g6h\n"
                "    add signup page"
            ),
        ),
        Teaching(
            command="git log --grep",
            syntax='git log --grep="search text"',
            explanation=(
                "Search through commit MESSAGES for a keyword. This is how you find\n"
                "when a specific feature or bug fix was committed.\n"
                "\n"
                "Only matches against the commit message text, not the code changes."
            ),
            example_output=(
                '$ git log --grep="fix"\n'
                "commit a1b2c3d\n"
                "    fix login bug\n"
                "\n"
                "commit x9y8z7w\n"
                "    fix navbar alignment"
            ),
            pro_tip="Combine flags: git log --oneline --author='Alice' --since='1 week ago' to narrow results.",
        ),
    ],
    exercises=[
        Exercise(
            type="recall",
            prompt="Show commit history with each commit on a single line.",
            answers=["git log --oneline"],
            explanation="'--oneline' compresses each commit into short hash + message, ideal for quick scans.",
            sim_output="$ git log --oneline\na1b2c3d fix login\ne4f5g6h add homepage\ni7j8k9l initial commit",
        ),
        Exercise(
            type="recall",
            prompt="Show commit history with a visual branch graph.",
            answers=["git log --oneline --graph", "git log --oneline --graph --all", "git log --graph"],
            explanation="'--graph' draws branch/merge lines so you can understand divergence and merge points.",
            sim_output="$ git log --oneline --graph --all\n* a1b2c3d (HEAD -> main) fix login\n| * d4e5f6g (feature) add signup\n|/\n* e4f5g6h add homepage\n* i7j8k9l initial commit",
        ),
        Exercise(
            type="fill_blank",
            prompt="Show commits by a specific author.",
            blank_template='git log --____="John"',
            answers=["author"],
            explanation="The '--author' filter narrows history to commits created by a specific person.",
            sim_output='$ git log --author="John"\ncommit abc...\nAuthor: John <john@mail.com>',
        ),
        Exercise(
            type="fill_blank",
            prompt="Show commits from the last 2 weeks.",
            blank_template='git log --____="2 weeks ago"',
            answers=["since"],
            explanation="Use '--since' with natural time strings to focus on recent work windows.",
        ),
        Exercise(
            type="fill_blank",
            prompt="Search commit messages for the word 'fix'.",
            blank_template='git log --____="fix"',
            answers=["grep"],
            explanation="'--grep' searches commit messages for keywords, perfect for finding bug-fix commits quickly.",
            sim_output='$ git log --grep="fix"\ncommit a1b2c3d\n    fix login bug\ncommit x9y8z7w\n    fix navbar alignment',
        ),
        Exercise(
            type="recall",
            prompt="Show commit history with file change statistics (how many files changed, insertions, deletions).",
            answers=["git log --stat"],
            explanation="'--stat' summarizes scope per commit without showing full patches, useful for quick impact review.",
            sim_output="$ git log --stat\ncommit a1b2c3d\n    fix login\n\n app.py | 5 +++--\n 1 file changed, 3 insertions(+), 2 deletions(-)",
        ),
    ],
    drills=[
        Exercise(type="recall", prompt="Compact one-line log.", answers=["git log --oneline"],
                 explanation="--oneline is your go-to format for quickly scanning history."),
        Exercise(type="recall", prompt="Log with branch graph.", answers=["git log --oneline --graph", "git log --graph", "git log --oneline --graph --all"],
                 explanation="The graph shows branch structure visually—essential when working with multiple branches."),
        Exercise(type="recall", prompt="Log filtered by author 'Alice'.", answers=['git log --author="Alice"', "git log --author=Alice", "git log --author='Alice'"],
                 explanation="Filter by author to see contributions from specific team members."),
        Exercise(type="recall", prompt="Log of commits from the last week.", answers=['git log --since="1 week ago"', "git log --since='1 week ago'"],
                 explanation="Time filters like --since are perfect for status updates: 'What did I do this week?'"),
        Exercise(type="recall", prompt="Search log for messages containing 'refactor'.", answers=['git log --grep="refactor"', "git log --grep=refactor", "git log --grep='refactor'"],
                 explanation="grep searches commit messages, making it easy to find when specific work was done."),
        Exercise(type="recall", prompt="Log with file change stats.", answers=["git log --stat"],
                 explanation="--stat gives you a bird's-eye view of what changed without reading the full diff."),
        Exercise(type="recall", prompt="One-line log with graph for all branches.", answers=["git log --oneline --graph --all"],
                 explanation="Combining --oneline, --graph, and --all gives you the complete picture of your repo's history."),
        Exercise(type="recall", prompt="Find commits by author 'Bob'.", answers=['git log --author="Bob"', "git log --author=Bob"],
                 explanation="Great for code reviews—see everything a teammate has committed recently."),
        Exercise(type="recall", prompt="Commits since yesterday.", answers=['git log --since="yesterday"', "git log --since=yesterday"],
                 explanation="Natural language dates like 'yesterday' make --since intuitive and powerful."),
        Exercise(type="recall", prompt="Search commit messages for 'bug'.", answers=['git log --grep="bug"', "git log --grep=bug"],
                 explanation="Tracking bug fixes is easy with --grep. Search for 'fix', 'bug', or issue numbers."),
    ],
)


# ── Export all basics levels ─────────────────────────────

BASICS_LEVELS = {
    0: SETUP_LEVEL,  # Setup is treated as Level 0
    1: LEVEL_1,
    2: LEVEL_2,
    3: LEVEL_3,
    4: LEVEL_4,
    5: LEVEL_5,
    6: LEVEL_6,
}
