# Contributing to BasicChatBot_AINews

Thank you for considering contributing to this project! This document provides guidelines for contributing to the BasicChatBot_AINews project.

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Git
- conda or pip
- Required API keys (GROQ, Tavily, etc.)

### Development Setup

1. **Fork and clone the repository:**
```bash
git clone https://github.com/yourusername/BasicChatBot_AINews.git
cd BasicChatBot_AINews
```

2. **Create a development environment:**
```bash
# Using conda (recommended)
conda env create -f environment.yml
conda activate LangGraphBasicChatBot

# Or using pip
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the application:**
```bash
streamlit run app/main.py
```

## 📋 Development Guidelines

### Code Style

We follow Python best practices and maintain high code quality:

- **Type Hints**: All functions should include proper type annotations
- **Docstrings**: Use Google-style docstrings for classes and functions
- **Error Handling**: Implement graceful error handling with proper logging
- **Naming**: Use descriptive variable and function names

#### Code Formatting
```bash
# Format code
black app/
isort app/

# Type checking
mypy app/

# Linting
flake8 app/
```

### Project Structure

Please maintain the existing architecture:

```
app/
├── newsbot/
│   ├── core/              # Configuration and utilities
│   ├── features/          # Feature implementations
│   │   ├── common/        # Shared base classes
│   │   ├── chat/          # Chat functionality
│   │   └── ai_news/       # AI news processing
│   └── ui/                # Streamlit UI components
```

### Key Architectural Patterns

1. **Abstract Base Classes**: Use for shared interfaces
2. **Pydantic Models**: For data validation and configuration
3. **LangGraph State**: TypedDict for workflow state management
4. **Error Handling**: Comprehensive exception handling with logging

## 🐛 Bug Reports

When filing bug reports, please include:

1. **Environment Information:**
   - Python version
   - Operating system
   - Package versions (from `pip list` or `conda list`)

2. **Steps to Reproduce:**
   - Clear, numbered steps
   - Expected vs actual behavior
   - Error messages and stack traces

3. **Configuration:**
   - LLM provider and model used
   - Relevant configuration settings
   - API key status (don't include actual keys!)

## ✨ Feature Requests

For new features, please:

1. **Check existing issues** to avoid duplicates
2. **Describe the use case** and motivation
3. **Provide examples** of expected behavior
4. **Consider implementation** complexity and impact

## 🔧 Pull Request Process

### Before Submitting

1. **Create a feature branch:**
```bash
git checkout -b feature/amazing-feature
```

2. **Write tests** for new functionality
3. **Update documentation** as needed
4. **Ensure code quality:**
```bash
black app/
isort app/
mypy app/
```

5. **Test thoroughly:**
```bash
# Run the application
streamlit run app/main.py

# Test both chat and AI news features
# Verify with different LLM providers
```

### Pull Request Guidelines

1. **Title**: Clear, descriptive title
2. **Description**: 
   - What does this PR do?
   - Why is this change needed?
   - How was it tested?
   - Any breaking changes?

3. **Code Review Checklist:**
   - [ ] Code follows project style guidelines
   - [ ] Tests pass (if applicable)
   - [ ] Documentation updated
   - [ ] No breaking changes (or documented)
   - [ ] Error handling implemented
   - [ ] Type hints included

## 🏗️ Architecture Contributions

### Adding New LLM Providers

1. Update `LLMProvider` enum in `core/config/config_manager.py`
2. Add provider configuration in `uiconfig.yml`
3. Implement provider-specific logic in LLM classes
4. Test with various models from the provider

### Adding New Features

1. Create feature directory under `features/`
2. Implement following components as needed:
   - Agent (orchestrator)
   - LLM (language model wrapper)
   - Graph Builder (workflow)
   - Nodes (processing units)
   - State (TypedDict)
3. Add UI components in `ui/`
4. Update main application flow

### Adding New Tools

1. Implement tool wrapper in appropriate feature
2. Follow LangChain tool interface patterns
3. Add proper error handling and validation
4. Include in graph builder tool lists

## 🧪 Testing

### Manual Testing

1. **Chat Feature:**
   - Test conversation flow
   - Verify tool usage (search)
   - Check error handling
   - Test different LLM providers

2. **AI News Feature:**
   - Test news fetching
   - Verify summarization quality
   - Check file output
   - Test different time frames

### Automated Testing (Future)

When adding tests, focus on:
- Unit tests for individual components
- Integration tests for workflows
- Mocking external API calls
- Configuration validation

## 📚 Documentation

### Code Documentation

- **Classes**: Describe purpose, key methods, usage patterns
- **Functions**: Parameters, return values, side effects
- **Complex Logic**: Inline comments explaining non-obvious code

### README Updates

When adding features, update:
- Feature descriptions
- Usage instructions
- Configuration options
- API requirements

## 🤝 Community

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help newcomers learn
- Focus on technical merit

### Communication

- Use GitHub issues for bugs and features
- Be clear and concise in communications
- Provide context and examples
- Follow up on discussions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🎉 Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes for significant contributions
- Special recognition for major features

## ❓ Questions?

If you have questions about contributing:
1. Check existing issues and discussions
2. Create a new issue with the "question" label
3. Be specific about what you want to contribute

Thank you for helping make BasicChatBot_AINews better! 🚀