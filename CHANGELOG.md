# Changelog

All notable changes to the Drupal AI Agent project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-01-15

### 🧹 Major Cleanup & Architecture Improvements

#### Added
- **Unified Entry Point**: Single `main.py` with modular architecture
- **Clean Project Structure**: Organized commands, services, parsers, and utilities
- **Legacy Code Removal**: Eliminated redundant and outdated files
- **Enhanced Documentation**: Updated README with current architecture
- **Development Workflow**: Improved setup and testing procedures

#### Changed
- **main.py**: Replaced with modular architecture version (was `main_modular.py`)
- **requirements.txt**: Updated with comprehensive, modern dependencies
- **Project Structure**: Reorganized for better maintainability
- **Documentation**: Updated all examples and instructions for new architecture

#### Removed
- `main_old.py` - Legacy implementation with embedded classes
- `main_clean.py` - Intermediate cleanup version
- `main_modular.py` - Renamed to `main.py`
- `requirements_modular.txt` - Merged into main requirements.txt
- `test_main.py` - Legacy test file (moved to docs/examples)
- `examples.py` - Moved to docs/examples directory

#### Fixed
- **Import Dependencies**: Resolved circular imports and dependency issues
- **Code Duplication**: Eliminated redundant implementations
- **Project Organization**: Clear separation of concerns across modules

### 🏗️ Architecture Improvements

#### Modular Command Pattern (MCP)
- Clear separation between commands, services, and utilities
- Each command is a self-contained, testable class
- Factory pattern for dynamic command instantiation
- Consistent error handling and response formatting

#### Service Layer
- **AIService**: Multi-provider AI integration with local Ollama support
- **SiteSetupService**: Complete DDEV/Lando lifecycle management
- **DrushService**: Drupal command-line operations
- **GraphQLService**: Advanced query operations
- **JSONAPIService**: Content management operations

#### Enhanced Natural Language Processing
- Regex-based intent parsing with AI fallback
- Flexible command pattern matching
- Parameter extraction and validation
- Comprehensive error messages and suggestions

### 🧪 Testing & Quality

#### Test Coverage
- `test_modular.py`: Architecture validation and integration testing
- Component-level testing for all major services
- Configuration validation and environment testing

#### Code Quality
- Consistent coding standards across all modules
- Type hints and documentation for all public APIs
- Error handling with detailed logging
- Clean import structure and dependency management

### 📚 Documentation Updates

#### README.md
- Complete architecture overview
- Updated installation and setup instructions
- Comprehensive command examples
- Troubleshooting guide with common issues
- Development workflow and contribution guidelines

#### Project Structure
- Clear file organization with purpose-driven directories
- Examples and legacy code moved to appropriate locations
- Clean separation between production and development files

### 🔧 Developer Experience

#### Simplified Setup
1. Single requirements.txt file
2. Streamlined virtual environment setup
3. Automated local AI configuration
4. Comprehensive testing and validation

#### Enhanced Debugging
- Structured logging across all components
- Verbose mode for detailed operation tracing
- Configuration validation and health checks
- Clear error messages with actionable suggestions

## [1.0.0] - 2025-01-10

### Initial Release
- Basic natural language command processing
- Multi-provider AI integration (OpenAI, Anthropic, Ollama)
- DDEV and Lando site management
- Content creation and editing capabilities
- Drush command execution
- JSON:API and GraphQL integration

---

## Migration Guide from v1.x to v2.0

### Breaking Changes
- **Entry Point**: Use `python main.py` instead of `python main_modular.py`
- **Requirements**: Install from `requirements.txt` (no longer need `requirements_modular.txt`)
- **Project Structure**: Files reorganized - update any custom integrations

### Migration Steps
1. **Update Dependencies**: `pip install -r requirements.txt`
2. **Update Scripts**: Change any references from `main_modular.py` to `main.py`
3. **Test Configuration**: Run `python main.py test` to validate setup
4. **Validate Architecture**: Run `python test_modular.py` to ensure everything works

### Backward Compatibility
- All CLI commands remain the same
- Configuration format is unchanged
- API responses maintain the same structure
- Natural language patterns continue to work as before
