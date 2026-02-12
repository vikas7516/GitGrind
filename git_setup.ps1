#!/usr/bin/env pwsh
# Git setup and push script

Write-Host "=== GitGrind - Git Setup and Push ===" -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
Set-Location "C:\Users\Asus\Desktop\GitGrind"

# Configure git
Write-Host "[1/6] Configuring git user..." -ForegroundColor Yellow
git config user.name "vikas7516"
git config user.email "vikaslavaniya6666@gmail.com"
Write-Host "  Done" -ForegroundColor Green

# Check if git is initialized
Write-Host "[2/6] Checking git repository..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    Write-Host "  Initializing git repository..." -ForegroundColor Yellow
    git init
    git branch -M main
    Write-Host "  Repository initialized" -ForegroundColor Green
} else {
    Write-Host "  Repository already initialized" -ForegroundColor Green
}

# Add all files
Write-Host "[3/6] Adding files to git..." -ForegroundColor Yellow
git add .
Write-Host "  Files staged" -ForegroundColor Green

# Show status
Write-Host "[4/6] Git status:" -ForegroundColor Yellow
git status --short

# Commit changes
Write-Host "[5/6] Committing changes..." -ForegroundColor Yellow
$commitMsg = "Fixed critical bugs and completed code audit

- Fixed AttributeError with Stage objects (stage.data_key)
- Removed unnecessary hasattr checks
- Added validation script
- Updated .gitignore to exclude save files
- Added audit documentation"

git commit -m $commitMsg
Write-Host "  Committed" -ForegroundColor Green

# Instructions for GitHub push
Write-Host ""
Write-Host "[6/6] Ready to push to GitHub!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Create a new repository on GitHub at: https://github.com/new"
Write-Host "2. Name it 'GitGrind' (or any name you prefer)"
Write-Host "3. Do NOT initialize with README, .gitignore, or license"
Write-Host "4. Then run these commands:"
Write-Host ""
Write-Host "   git remote add origin https://github.com/vikas7516/GitGrind.git" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "Or if you want to push to an existing repository, run:" -ForegroundColor Yellow
Write-Host "   git remote add origin <YOUR_REPO_URL>" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Cyan

