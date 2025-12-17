# Git Version Control Guide

Complete guide to using Git for version control and collaboration.

## What is Git?

Git is a distributed version control system that tracks changes in source code during software development.

### Key Concepts

- **Repository (Repo)** - Project folder tracked by Git
- **Commit** - Snapshot of your project at a point in time
- **Branch** - Parallel version of your repository
- **Remote** - Version of your repository hosted on a server (GitHub, Azure DevOps)
- **Pull Request** - Proposal to merge code changes

## Essential Git Commands

### Initial Setup

```bash
# Configure your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"

# View configuration
git config --list
```

### Creating a Repository

```bash
# Initialize a new repository
git init

# Clone an existing repository
git clone https://github.com/username/repository.git
```

### Basic Workflow

```bash
# Check status of files
git status

# Add files to staging area
git add filename.txt          # Add specific file
git add .                     # Add all changed files
git add *.py                  # Add all Python files

# Commit changes
git commit -m "Descriptive commit message"

# Push to remote repository
git push origin main          # Push to main branch
git push origin feature-name  # Push to specific branch

# Pull latest changes
git pull origin main
```

### Branching

```bash
# Create a new branch
git branch feature-name

# Switch to a branch
git checkout feature-name

# Create and switch to new branch
git checkout -b feature-name

# List all branches
git branch -a

# Delete a branch
git branch -d feature-name

# Merge branch into current branch
git merge feature-name
```

### Viewing History

```bash
# View commit history
git log
git log --oneline             # Compact view
git log --graph --all         # Visual graph of branches

# View changes
git diff                      # Unstaged changes
git diff --staged             # Staged changes
git diff branch1..branch2     # Compare branches
```

### Undoing Changes

```bash
# Discard changes in working directory
git checkout -- filename.txt

# Unstage files
git reset HEAD filename.txt

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert a commit (creates new commit)
git revert commit-hash
```

### Remote Repositories

```bash
# Add remote repository
git remote add origin https://github.com/username/repo.git

# View remotes
git remote -v

# Fetch changes from remote
git fetch origin

# Pull and merge changes
git pull origin main
```

## Git Workflow Best Practices

### 1. Commit Messages

Good commit messages should be:
- Clear and descriptive
- In present tense
- Limited to 50 characters for subject
- Include body for complex changes

```bash
# Good examples
git commit -m "Add employee salary calculation feature"
git commit -m "Fix bug in date validation"
git commit -m "Update README with setup instructions"

# Bad examples
git commit -m "fixed stuff"
git commit -m "changes"
git commit -m "asdf"
```

### 2. Branching Strategy

**Feature Branch Workflow:**

```bash
# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/add-employee-search

# Work on feature, make commits
git add .
git commit -m "Implement employee search functionality"

# Push feature branch
git push origin feature/add-employee-search

# Create pull request on GitHub/Azure DevOps
# After approval, merge to main
```

**Common Branch Names:**
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Urgent fixes
- `refactor/description` - Code refactoring
- `docs/description` - Documentation updates

### 3. Gitignore

Create `.gitignore` file to exclude files from version control:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Database
*.db
*.sqlite

# Secrets
.env
secrets.json
appsettings.Development.json

# Build outputs
bin/
obj/
dist/
build/
```

### 4. Working with Team Foundation Server (TFS) / Azure DevOps

```bash
# Clone from Azure DevOps
git clone https://dev.azure.com/organization/project/_git/repository

# Set up branch policies
# - Require pull request reviews
# - Require successful builds
# - Require linked work items

# Link commits to work items
git commit -m "Fix login bug #123"  # Links to work item 123
```

## Common Workflows

### Workflow 1: Daily Development

```bash
# Start of day - get latest changes
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/new-report

# Make changes, commit frequently
git add report.py
git commit -m "Add report generation logic"

git add tests/test_report.py
git commit -m "Add unit tests for report"

# Push to remote
git push origin feature/new-report

# Create pull request for review
```

### Workflow 2: Fixing Merge Conflicts

```bash
# Pull latest changes
git pull origin main

# If conflicts occur
# 1. Git will mark conflicted files
# 2. Open files and resolve conflicts manually
# 3. Look for conflict markers:
#    <<<<<<< HEAD
#    Your changes
#    =======
#    Their changes
#    >>>>>>> branch-name

# After resolving conflicts
git add conflicted-file.py
git commit -m "Resolve merge conflicts"
git push
```

### Workflow 3: Code Review Process

```bash
# 1. Create pull request on GitHub/Azure DevOps
# 2. Add reviewers
# 3. Reviewers comment on code
# 4. Make requested changes

git checkout feature/your-feature
# Make changes
git add .
git commit -m "Address review feedback"
git push origin feature/your-feature

# 5. After approval, merge PR
# 6. Delete feature branch
git branch -d feature/your-feature
git push origin --delete feature/your-feature
```

## Advanced Git Commands

### Stashing Changes

```bash
# Temporarily save uncommitted changes
git stash

# List stashed changes
git stash list

# Apply most recent stash
git stash apply

# Apply and remove stash
git stash pop

# Drop stash
git stash drop
```

### Cherry-picking

```bash
# Apply specific commit from another branch
git cherry-pick commit-hash
```

### Rebasing

```bash
# Rebase current branch onto main
git checkout feature-branch
git rebase main

# Interactive rebase (clean up history)
git rebase -i HEAD~5  # Last 5 commits
```

### Tagging

```bash
# Create tag
git tag v1.0.0

# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tags
git push origin v1.0.0
git push origin --tags  # Push all tags

# List tags
git tag
```

## GitHub / Azure DevOps Features

### Pull Requests
- Code review platform
- Discuss changes
- Run automated tests
- Require approvals before merge

### Branch Policies
- Protect important branches (main, develop)
- Require pull requests
- Require status checks
- Require code reviews

### Continuous Integration
- Automatically build and test code
- Run on every commit/PR
- Prevent breaking changes

## Best Practices Summary

1. ✅ Commit early and often
2. ✅ Write descriptive commit messages
3. ✅ Use branches for features/fixes
4. ✅ Keep branches short-lived
5. ✅ Pull before starting new work
6. ✅ Review code before merging
7. ✅ Use .gitignore appropriately
8. ✅ Never commit sensitive data
9. ✅ Keep commits focused and atomic
10. ✅ Document your workflow

## Troubleshooting

### Problem: Accidentally committed sensitive data
```bash
# Remove file from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch secrets.txt" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin --force --all
```

### Problem: Need to undo last commit
```bash
# Keep changes
git reset --soft HEAD~1

# Discard changes
git reset --hard HEAD~1
```

### Problem: Detached HEAD state
```bash
# Create branch from current state
git checkout -b recovery-branch

# Or return to main
git checkout main
```

## Resources

- **Official Git Documentation**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com
- **Azure DevOps Git**: https://learn.microsoft.com/azure/devops/repos/git
- **Pro Git Book**: https://git-scm.com/book
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
