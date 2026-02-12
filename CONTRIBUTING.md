# Contributing to GitGrind

Thank you for your interest in contributing to GitGrind! This document provides guidelines for contributing to the project.

## 🎯 Ways to Contribute

### 🐛 Report Bugs
- Use the GitHub Issues page
- Include Python version, OS, and error messages
- Provide steps to reproduce the issue
- Include screenshots if applicable

### 💡 Suggest Features
- Open an issue with the `enhancement` label
- Describe the feature and its benefits
- Explain how it fits with GitGrind's educational mission

### 📝 Improve Content
- Submit better exercise explanations
- Add more exercises or levels
- Improve teaching slides
- Fix typos or unclear instructions

### 🔧 Submit Code
- Fork the repository
- Create a feature branch
- Write clean, documented code
- Add tests for new features
- Submit a pull request

## 🛠️ Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/gitgrind.git
cd gitgrind

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest
```

## 📋 Code Guidelines

### Python Style
- Follow PEP 8
- Use type hints where applicable
- Write docstrings for functions and classes
- Keep functions focused and small

### Adding Exercises
When adding exercises, ensure:
- Clear, unambiguous prompts
- Multiple acceptable answers when appropriate
- Contextual explanations that teach WHY
- Appropriate difficulty for the level

Example:
```python
Exercise(
    type="recall",
    prompt="Stage all changes in the current directory.",
    answers=["git add .", "git add -A"],
    explanation="'git add .' stages all files in the current directory. The dot means 'everything here'.",
)
```

### Testing
- Add tests for new validators
- Test edge cases
- Ensure all tests pass before submitting PR

## 📝 Commit Messages

Use clear, descriptive commit messages:
- `feat: Add level 21 - Git hooks`
- `fix: Correct answer validation for rebase exercises`
- `docs: Update installation instructions`
- `refactor: Simplify validator logic`

## 🔄 Pull Request Process

1. **Update Documentation** - If your PR adds features, update README.md
2. **Add Tests** - New features need test coverage
3. **Follow Style** - Match existing code style
4. **Describe Changes** - Explain what and why in PR description
5. **Link Issues** - Reference related issues with `Fixes #123`

## ✅ PR Checklist

Before submitting:
- [ ] Code follows project style guidelines
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts with main
- [ ] Explanation quality matches existing content

## 🎓 Content Contribution Guidelines

### Writing Explanations
Good explanations should:
- Be 1-3 sentences
- Explain WHY, not just WHAT
- Use plain language (no jargon)
- Be specific to the exercise context
- Help users avoid future mistakes

**Good**: "The -d flag safely deletes merged branches. Use -D (capital D) to force-delete unmerged branches."

**Bad**: "Use -d to delete."

### Exercise Design Principles
1. **Progressive Difficulty** - Build on previous knowledge
2. **Clear Prompts** - No ambiguity about what's being asked
3. **Multiple Paths** - Accept equivalent answers
4. **Real-World Relevance** - Teach practical skills
5. **Immediate Value** - Users see why they're learning this

## 🐞 Bug Fix Guidelines

When fixing bugs:
1. Add a test that reproduces the bug
2. Fix the bug
3. Verify the test now passes
4. Document the fix in PR description

## 📞 Getting Help

- **Questions?** Open a GitHub Discussion
- **Stuck?** Comment on your PR
- **Ideas?** Open an issue to discuss first

## 🙏 Thank You!

Every contribution makes GitGrind better for learners worldwide. We appreciate your effort to help others master Git!

---

**Questions?** Open an issue or start a discussion. We're here to help!

