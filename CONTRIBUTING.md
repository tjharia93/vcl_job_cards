# Contributing to VCL Job Cards

Thank you for your interest in contributing to the VCL Job Cards app! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites
- Python 3.10+
- Node.js 14+
- Frappe Framework
- ERPNext

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/tjharia93/vcl_job_cards.git
cd vcl_job_cards
```

2. **Install dependencies:**
```bash
pip install -e .
```

3. **Set up development environment:**
```bash
# Create a new Frappe site for development
bench new-site dev-site
bench --site dev-site install-app vcl_job_cards
```

## Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Follow Frappe Framework coding standards
- Add comprehensive docstrings
- Include validation for all user inputs
- Test your changes thoroughly

### 3. Commit Your Changes
```bash
git add .
git commit -m "feat: Add your feature description

- What was added/changed
- Why it was needed
- Any breaking changes"
```

### 4. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```
Then create a pull request on GitHub.

## Code Standards

### Python Code
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all classes and methods
- Include type hints where appropriate

### JavaScript Code
- Use ES6+ features
- Follow consistent naming conventions
- Add comments for complex logic
- Handle errors gracefully

### DocType Configuration
- Use descriptive field names
- Set appropriate field types and validation
- Configure permissions properly
- Add helpful field descriptions

## Testing

### Running Tests
```bash
# Run all tests
bench --site [sitename] run-tests --app vcl_job_cards

# Run specific test
bench --site [sitename] run-tests --app vcl_job_cards --test test_file.py
```

### Test Coverage
- Write tests for all new features
- Test edge cases and error conditions
- Ensure existing functionality still works

## Documentation

### Code Documentation
- Add docstrings to all Python functions and classes
- Document complex JavaScript functions
- Update README.md for new features

### User Documentation
- Update usage guides for new features
- Add screenshots for UI changes
- Document configuration requirements

## Commit Message Guidelines

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

Examples:
```
feat: Add Dies DocType with auto-population
fix: Correct validation error in label specifications
docs: Update installation instructions
```

## Pull Request Process

1. **Ensure your PR:**
   - Has a clear title and description
   - References any related issues
   - Includes tests for new features
   - Updates documentation as needed

2. **PR Review Process:**
   - Code will be reviewed by maintainers
   - Address any feedback or requested changes
   - Once approved, PR will be merged

## Issue Reporting

When reporting bugs or requesting features:

1. **Check existing issues** to avoid duplicates
2. **Use issue templates** when available
3. **Provide detailed information:**
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Screenshots if applicable

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn and contribute
- Maintain professional communication

## Getting Help

- **Documentation**: Check README.md and inline code documentation
- **Issues**: Search existing issues or create new ones
- **Discussions**: Use GitHub Discussions for questions
- **Email**: tanuj@vimitconverters.com for direct support

Thank you for contributing to VCL Job Cards! 🚀