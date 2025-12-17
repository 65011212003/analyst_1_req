# Common Git commands and workflows for quick reference

## Daily Commands

# Check what changed
git status

# Add files to staging
git add filename.txt
git add .

# Commit changes
git commit -m "Your message"

# Push to remote
git push origin branch-name

# Pull latest changes
git pull origin main

## Branching

# Create new branch
git checkout -b feature/my-feature

# Switch branches
git checkout main

# List branches
git branch -a

# Delete branch
git branch -d feature/my-feature

## Undo Changes

# Discard local changes
git checkout -- filename.txt

# Unstage file
git reset HEAD filename.txt

# Undo last commit (keep changes)
git reset --soft HEAD~1

## History

# View commit log
git log --oneline

# View changes
git diff

# See file history
git log --follow filename.txt

## Stash (temporary save)

# Save current changes
git stash

# List stashes
git stash list

# Restore stashed changes
git stash pop

## Working with Remotes

# Add remote
git remote add origin URL

# View remotes
git remote -v

# Fetch changes
git fetch origin

# Pull and merge
git pull origin main
