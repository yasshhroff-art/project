# Contributing to Google Ads Campaign Manager

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/google-ads-campaign-manager.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests (if available)
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

Follow the instructions in README.md to set up your development environment.

Quick start:
```bash
./setup.sh
```

## Code Style

### Python (Backend)

- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use docstrings for functions and classes
- Type hints are encouraged

Example:
```python
def create_campaign(data: dict) -> Campaign:
    """
    Create a new campaign in the database.
    
    Args:
        data: Dictionary containing campaign details
        
    Returns:
        Created Campaign object
        
    Raises:
        ValueError: If data validation fails
    """
    pass
```

### JavaScript/React (Frontend)

- Use ES6+ features
- Use 2 spaces for indentation
- Use semicolons
- Use arrow functions for components
- Use meaningful variable names

Example:
```javascript
const CampaignForm = ({ onSuccess }) => {
  const [loading, setLoading] = useState(false);
  
  const handleSubmit = async (data) => {
    // Implementation
  };
  
  return (
    // JSX
  );
};
```

## Commit Messages

Follow the Conventional Commits specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add campaign template support
fix: resolve CORS issue in production
docs: update API documentation
refactor: extract validation logic to utility
```

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the DESIGN_NOTES.md if architectural changes are made
3. Ensure all tests pass (when test suite is available)
4. Get approval from at least one maintainer
5. Squash commits if requested

## Testing

When adding new features:

1. Add unit tests for new functions
2. Add integration tests for new endpoints
3. Update manual testing guide in TESTING_GUIDE.md
4. Test in multiple browsers (Chrome, Firefox, Safari)

## Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, Python version, Node version, Browser
6. **Logs**: Relevant error messages or logs
7. **Screenshots**: If applicable

Example:
```markdown
**Bug**: Campaign publish fails with 401 error

**Steps to Reproduce**:
1. Create a campaign locally
2. Click "Publish" button
3. Error appears

**Expected**: Campaign publishes to Google Ads

**Actual**: 401 Unauthorized error

**Environment**:
- OS: macOS 14.0
- Python: 3.11
- Node: 18.0
- Browser: Chrome 120

**Logs**:
```
[ERROR] Google Ads API error: UNAUTHORIZED
```

**Screenshots**: [Attach screenshot]
```

## Feature Requests

When requesting features, please include:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: Other ways to solve the problem
4. **Additional Context**: Any other relevant information

## Areas for Contribution

Here are some areas where contributions are welcome:

### Backend

- [ ] Add unit tests for models and services
- [ ] Implement campaign templates
- [ ] Add bulk campaign operations
- [ ] Improve error handling and validation
- [ ] Add API rate limiting
- [ ] Implement caching layer
- [ ] Add background job support (Celery)

### Frontend

- [ ] Add state management (Redux/Zustand)
- [ ] Implement form validation with Yup
- [ ] Add loading skeletons
- [ ] Improve responsive design
- [ ] Add dark mode support
- [ ] Implement keyboard shortcuts
- [ ] Add campaign search and filtering

### Google Ads Integration

- [ ] Support more campaign types (Search, Shopping, Video)
- [ ] Add campaign performance metrics
- [ ] Implement A/B testing
- [ ] Add budget optimization
- [ ] Support MCC account management

### DevOps

- [ ] Add CI/CD pipeline (GitHub Actions)
- [ ] Implement automated testing
- [ ] Add Docker production configuration
- [ ] Create Kubernetes manifests
- [ ] Add monitoring and alerting

### Documentation

- [ ] Add API documentation (Swagger/OpenAPI)
- [ ] Create video tutorials
- [ ] Add more code examples
- [ ] Improve troubleshooting guide
- [ ] Translate to other languages

## Code Review Guidelines

When reviewing code:

1. **Be Respectful**: Provide constructive feedback
2. **Be Specific**: Point to exact lines and explain issues
3. **Ask Questions**: If something is unclear, ask
4. **Suggest Improvements**: Offer alternative solutions
5. **Approve Quickly**: Don't hold up good PRs

## Questions?

If you have questions:

1. Check the README.md and DESIGN_NOTES.md
2. Search existing issues
3. Open a new issue with the "question" label
4. Join our community chat (if available)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual identity.

### Our Standards

**Positive behaviors**:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Unacceptable behaviors**:
- Harassment or discriminatory language
- Trolling or insulting comments
- Publishing others' private information
- Other conduct that would be inappropriate in a professional setting

### Enforcement

Instances of abusive behavior may be reported to the project maintainers. All complaints will be reviewed and investigated.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
