# 🤖 Drupal AI Agent

A powerful **modular Python-based AI agent** designed to manage Drupal websites using **natural language commands**. Built with the **Modular Command Pattern (MCP)** and integrated with leading AI providers including **local AI support** for privacy-focused development.

## ✨ Features

### 🎯 Core Capabilities
- **Natural Language Processing**: Execute Drupal tasks using plain English commands
- **AI-Powered Content Generation**: Create content using local AI (Ollama) or cloud providers (OpenAI, Anthropic)
- **Modular Command Pattern**: Each operation is a separate, maintainable class
- **Privacy-First AI**: Defaults to local Ollama for secure, offline content generation
- **Comprehensive Drupal Integration**: JSON:API, GraphQL, and Drush command execution
- **Local Development Tools**: Create, start, stop, restart, and manage sites with DDEV or Lando
- **Multi-Format Output**: JSON, text, or table format responses perfect for automation

### 🚀 Site Lifecycle Management
- **Site Creation**: Scaffold new Drupal sites with DDEV or Lando
- **Site Operations**: Start, stop, restart, and check status of local sites
- **Platform Detection**: Auto-detects DDEV or Lando configurations
- **Environment Management**: Full site lifecycle control with natural language

### 🧠 Advanced AI Integration
- **Local AI Support**: Ollama integration for offline, privacy-focused content generation
- **Multi-Provider Support**: OpenAI, Anthropic, and local models
- **Smart Provider Selection**: Automatic fallback and provider switching
- **Optimized Performance**: Efficient model selection and timeout handling

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd drupal-management-ai-agent

# Install dependencies
pip install -r requirements.txt

# Activate virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate     # On Windows
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Initialize configuration
python main.py setup

# Set up local AI (recommended for privacy and cost-effectiveness)
chmod +x setup_ollama.sh
./setup_ollama.sh

# Edit the generated .env file with your settings
nano .env
```

### 3. Test Your Setup

```bash
# Test configuration and services
python main.py test

# Validate modular architecture
python test_modular.py

# Try your first commands (uses local Ollama by default)
python main.py execute "Create site named test-site"
python main.py execute "Status of site test-site"
python main.py execute "Start site test-site"
python main.py execute "Stop site test-site"
```

## 📋 Configuration (.env)

```env
# Drupal Configuration
DRUPAL_BASE_URL=http://localhost:8080
DRUPAL_USERNAME=admin
DRUPAL_PASSWORD=admin

# GraphQL Configuration
GRAPHQL_ENDPOINT=/graphql

# Local AI (Ollama) - Default Provider (Recommended)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
OLLAMA_TIMEOUT=60
DEFAULT_AI_PROVIDER=ollama

# Cloud AI Providers (optional - require API keys)
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Development Tools
DRUSH_PATH=drush
DDEV_PATH=ddev
LANDO_PATH=lando

# Site Setup
DEFAULT_SITE_DIRECTORY=./sites
DEFAULT_DRUPAL_VERSION=drupal10
```

## 🤖 Local AI Setup (Recommended)

The system defaults to using **Ollama** for privacy-focused, offline AI content generation. **No API keys required** and no data leaves your machine!

### Quick Setup

```bash
# Run the automated setup script
chmod +x setup_ollama.sh
./setup_ollama.sh
```

### Manual Setup

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the recommended efficient model (3B parameters)
ollama pull llama3.2:3b

# Alternative: smaller model for lower-end hardware
ollama pull llama3.2:1b

# Start Ollama service
ollama serve
```

### Benefits of Local AI
- **Complete Privacy**: No data sent to external APIs
- **Cost-Free**: No API usage charges
- **Always Available**: Works offline
- **Fast**: Local inference, no network latency
- **Customizable**: Use any Ollama-compatible model

The system will automatically detect when Ollama is running and use it for all AI operations.

## 💬 Natural Language Commands

## 💬 Natural Language Commands

### Content Management

```bash
# Create AI-generated blog posts (uses local Ollama by default)
python main.py execute "Create a blog post about AI in Drupal"
python main.py execute "Generate an article about the future of headless CMS"

# Use specific cloud AI provider
python main.py execute "Generate an article using Anthropic about accessibility in web design"
python main.py execute "Create content with OpenAI about Drupal performance optimization"

# Edit existing content
python main.py execute "Edit the title of node 45 to 'Headless CMS in 2025'"

# Upload media with alt text
python main.py execute "Upload header.jpg to media library with alt text 'Homepage Banner'"
```

### Site Maintenance

```bash
# Cache management
python main.py execute "Clear Drupal cache"
python main.py execute "Rebuild cache"
python main.py execute "Clear cache and run cron"

# Module management
python main.py execute "Enable module webform"
python main.py execute "Disable module devel"

# Custom Drush commands
python main.py execute "Run drush status"
python main.py execute "Export configuration"
python main.py execute "Import configuration"
python main.py execute "Update database"
```

### Site Creation & Management

```bash
# Create new Drupal sites
python main.py execute "Create new Drupal site named 'ai-blog'"
python main.py execute "Create site named 'headless-drupal' using Lando"
python main.py execute "Create site named 'my-project' using DDEV"

# Site lifecycle management
python main.py execute "Start site ai-blog"
python main.py execute "Stop site ai-blog" 
python main.py execute "Restart site ai-blog"
python main.py execute "Status of site ai-blog"

# Alternative command formats
python main.py execute "start ai-blog"
python main.py execute "stop site ai-blog"
python main.py execute "restart ai-blog site"
python main.py execute "status of site ai-blog"
```

### Content Queries (GraphQL)

```bash
# Query latest content
python main.py execute "Show me the latest 10 blog posts"
python main.py execute "Get the latest 5 articles"

# Search content
python main.py execute "Find posts about AI"
python main.py execute "Search for content about headless CMS"
python main.py execute "Fetch article bodies containing the word Drupal"

# User queries
python main.py execute "Get all users with role editor"
python main.py execute "Show users with role admin"
python main.py execute "List all authors"

# Content type queries
python main.py execute "Query nodes of type page"
python main.py execute "Get nodes tagged with 'tutorial'"
```

## 🏗️ Architecture

### Modular Command Pattern (MCP)

Each operation is implemented as a separate command class for maintainability and extensibility:

```
├── commands/
│   ├── base_command.py        # Abstract base class
│   ├── create_post.py         # AI-powered content creation
│   ├── create_site.py         # Site scaffolding with DDEV/Lando
│   └── site_management.py     # Start/stop/restart/status operations
├── services/
│   ├── ai_service.py          # Multi-provider AI integration
│   ├── drush_service.py       # Drush command execution
│   ├── jsonapi_service.py     # Drupal JSON:API operations
│   ├── graphql_service.py     # GraphQL query execution
│   └── site_setup_service.py  # DDEV/Lando site management
├── parsers/
│   ├── intent_parser.py       # Natural language to intent mapping
│   └── parameter_extractor.py # Parameter validation and extraction
└── utils/
    ├── logger.py              # Logging utilities
    └── output_formatter.py    # Multi-format output (JSON/text/table)
```

### Command Classes

- **CreateSiteCommand**: Site creation and scaffolding
- **StartSiteCommand**: Start DDEV/Lando sites
- **StopSiteCommand**: Stop DDEV/Lando sites  
- **RestartSiteCommand**: Restart DDEV/Lando sites
- **StatusSiteCommand**: Check site status and health
- **CreatePostCommand**: AI-powered blog/article creation
- **RunDrushCommand**: Execute any Drush command
- **EditNodeCommand**: Node content editing
- **UploadMediaCommand**: Media file uploads
- **QueryGraphQLCommand**: Execute GraphQL queries

### Key Services

- **IntentParser**: Regex-based natural language processing with AI fallback
- **AIService**: Multi-provider content generation (Ollama, OpenAI, Anthropic)
- **SiteSetupService**: Complete DDEV/Lando site lifecycle management
- **OutputFormatter**: Structured response formatting (JSON, text, table)
- **CommandFactory**: Dynamic command instantiation and routing

## 🤖 AI Integration

### Supported Providers

1. **Ollama (Local AI) - Default & Recommended**
   - ✅ **Privacy-focused** and completely offline
   - ✅ **No API keys required** - zero cost
   - ✅ Uses small, efficient models (llama3.2:3b by default)
   - ✅ **Auto-detection** and fallback support
   - ✅ **Optimized performance** with timeouts and error handling
   - 📦 Install with: `./setup_ollama.sh`

2. **OpenAI GPT-3.5/4**
   - Excellent for general content generation
   - Requires `OPENAI_API_KEY`
   - Higher cost but very capable

3. **Anthropic Claude**
   - Outstanding for detailed, nuanced content
   - Requires `ANTHROPIC_API_KEY`
   - Great for technical and analytical content

### Smart Provider Selection

The system automatically:
- **Defaults to Ollama** for privacy and cost savings
- **Detects availability** of each provider
- **Provides helpful error messages** with setup instructions
- **Falls back gracefully** when providers are unavailable

### Content Generation Examples

```bash
# Default local AI (privacy-focused, no API keys needed)
python main.py execute "Write a blog post about PHP 8.3 features"
python main.py execute "Create an article about Drupal security best practices"

# Explicitly specify cloud AI providers
python main.py execute "Generate article using OpenAI about Drupal performance"
python main.py execute "Create content with Anthropic about accessibility in web design"

# Override provider via command line
python main.py execute "Create post about headless CMS" --ai-provider anthropic
```

## 📊 JSON Output Format

All commands return structured JSON responses for easy automation and integration:

### Successful Operations
```json
{
  "success": true,
  "message": "DDEV site 'my-blog' started successfully",
  "data": {
    "project_name": "my-blog",
    "platform": "ddev",
    "status": "running",
    "directory": "./sites/my-blog",
    "url": "https://my-blog.ddev.site",
    "output": "Starting my-blog...\nSuccessfully started"
  }
}
```

### Content Creation Response
```json
{
  "success": true,
  "message": "Created post: AI in Modern Web Development",
  "data": {
    "node_id": 123,
    "url": "http://localhost:8080/node/123",
    "title": "AI in Modern Web Development",
    "content_type": "article",
    "ai_provider": "ollama"
  }
}
```

### GraphQL Query Response
```json
{
  "success": true,
  "message": "Found 5 nodes",
  "data": {
    "nodes": [
      {
        "id": 123,
        "title": "Latest Blog Post",
        "created": "2025-01-15T10:30:00Z",
        "url": "http://localhost:8080/node/123"
      }
    ],
    "count": 5,
    "query_type": "latest_nodes"
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Site directory not found: ./sites/nonexistent-site",
  "data": {
    "suggestions": [
      "Check the site name spelling",
      "Run 'create site named nonexistent-site' first"
    ]
  }
}
```

## 🛠️ Available Commands

### Site Management Commands
- **CreateSiteCommand**: Scaffold new Drupal sites with DDEV or Lando
- **StartSiteCommand**: Start existing DDEV/Lando sites
- **StopSiteCommand**: Stop running DDEV/Lando sites
- **RestartSiteCommand**: Restart DDEV/Lando sites
- **StatusSiteCommand**: Check site status and health

### Content Operations
- **CreatePostCommand**: AI-powered blog posts and articles
- **EditNodeCommand**: Modify existing content
- **UploadMediaCommand**: Upload and manage media files
- **QueryGraphQLCommand**: Execute GraphQL queries for content retrieval

### Site Maintenance
- **RunDrushCommand**: Execute any Drush command
  - Cache clearing and rebuilding
  - Cron execution  
  - Module enable/disable
  - Configuration import/export
  - Database updates

### Query Operations
- **Latest Content Queries**: Get recent posts by content type
- **Search Queries**: Find content by title or body text
- **User Queries**: Find users by role
- **Tagged Content**: Query content by taxonomy terms

## 🔧 Extending the Agent

### Adding New Commands

1. Create a new command class inheriting from `BaseCommand`:

```python
from commands.base_command import BaseCommand
from typing import Dict, Any

class CustomCommand(BaseCommand):
    def validate_params(self) -> bool:
        return "required_param" in self.params
    
    def execute(self) -> Dict[str, Any]:
        # Your implementation here
        return {
            "success": True,
            "message": "Custom operation completed",
            "data": {"result": "your_data_here"}
        }
```

2. Register in `main.py` CommandFactory:
```python
command_map = {
    "custom-action": CustomCommand,
    # ... existing commands
}
```

3. Add parsing patterns to `IntentParser`:
```python
command_patterns = {
    r"do something custom with (.+)": ("custom-action", "parameter"),
    # ... existing patterns
}
```

### Custom AI Providers

Extend `AIService` to support additional AI services:

```python
def _generate_custom_ai(self, prompt: str, content_type: str) -> str:
    # Your custom AI integration
    response = your_custom_api_call(prompt)
    return response.content
```

### Adding New Services

Create new service classes following the existing pattern:

```python
class MyCustomService:
    def __init__(self):
        self.config = config
    
    def perform_operation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation here
        pass
```

## 📦 Dependencies

### Core Requirements
- **typer**: Modern CLI framework with rich features  
- **requests**: HTTP client for Drupal JSON:API and GraphQL
- **python-dotenv**: Environment variable management
- **pydantic**: Data validation and settings management

### AI Provider Support
- **openai**: OpenAI API integration (optional)
- **anthropic**: Anthropic Claude API integration (optional)

### Development & Testing
- **pytest**: Testing framework
- **pytest-mock**: Mock support for testing
- **black**: Code formatting
- **flake8**: Code linting
- **mypy**: Type checking

### Optional Enhancements  
- **rich**: Enhanced terminal output formatting
- **tabulate**: Table formatting for output
- **pyyaml**: YAML configuration file support

### Installation Options

```bash
# Standard installation
pip install -r requirements.txt

# Development installation with testing and linting tools
pip install -r requirements.txt
pip install black flake8 mypy pytest pytest-mock

# Virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 🏃‍♂️ Development Workflow

### Local Development Setup

1. **Clone Repository**: `git clone <repo-url> && cd drupal-management-ai-agent`
2. **Set Up Virtual Environment**: `python -m venv .venv && source .venv/bin/activate`
3. **Install Dependencies**: `pip install -r requirements.txt`
4. **Configure Environment**: Copy `.env.example` to `.env` and edit settings
5. **Set Up Local AI**: Run `./setup_ollama.sh` (recommended)
6. **Test Configuration**: `python main.py test`
7. **Validate Architecture**: `python test_modular.py`

### Project Structure

```
drupal-management-ai-agent/
├── main.py                    # Main CLI entry point (modular architecture)
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── setup_ollama.sh           # Local AI setup script
├── test_modular.py           # Architecture validation tests
├── commands/                  # Command implementations
│   ├── base_command.py       # Abstract base class
│   ├── create_post.py        # Content creation
│   ├── create_site.py        # Site scaffolding
│   └── site_management.py    # Site lifecycle management
├── services/                  # Business logic services
│   ├── ai_service.py         # Multi-provider AI integration
│   ├── drush_service.py      # Drush command execution
│   ├── jsonapi_service.py    # Drupal JSON:API operations
│   ├── graphql_service.py    # GraphQL query execution
│   └── site_setup_service.py # DDEV/Lando management
├── parsers/                   # Natural language processing
│   ├── intent_parser.py      # Command parsing
│   └── parameter_extractor.py # Parameter validation
├── utils/                     # Utility functions
│   ├── logger.py            # Logging configuration
│   └── output_formatter.py  # Response formatting
├── docs/                     # Documentation and examples
│   └── examples/            # Example scripts and legacy tests
└── sites/                   # Created Drupal sites (ignored in git)
```

### Testing

```bash
# Run the modular architecture validation
python test_modular.py

# Test specific functionality
python main.py test

# Test commands with different output formats
python main.py execute "test command" --output-format json
python main.py execute "test command" --output-format text
python main.py execute "test command" --output-format table
```

### DDEV Integration Workflow

```bash
# Create new Drupal site with DDEV
python main.py execute "Create new site with DDEV named 'my-project'"

# The agent automatically:
# 1. Creates project directory in ./sites/my-project
# 2. Runs composer create-project drupal/recommended-project
# 3. Initializes DDEV configuration (.ddev/config.yaml)
# 4. Starts DDEV containers
# 5. Installs Drupal with configured admin credentials
# 6. Returns site URL and admin credentials

# Manage the site
python main.py execute "start my-project"
python main.py execute "status of site my-project"
python main.py execute "stop my-project site"
```

### Lando Integration Workflow

```bash
# Create new Drupal site with Lando
python main.py execute "Create new site using Lando called 'headless-site'"

# The agent automatically:
# 1. Scaffolds Drupal with Composer in ./sites/headless-site
# 2. Generates .lando.yml configuration
# 3. Starts Lando containers
# 4. Installs Drupal
# 5. Returns access information

# Platform auto-detection works seamlessly
python main.py execute "restart headless-site"  # Auto-detects Lando
```

## 🛠️ Site Management (DDEV & Lando)

Easily manage your local Drupal sites with natural language commands. The agent supports both DDEV and Lando platforms with automatic detection.

### Supported Operations
- **Create a site**: `python main.py execute "create site named my-blog using ddev"`
- **Start a site**: `python main.py execute "start my-blog site"`
- **Stop a site**: `python main.py execute "stop my-blog site"`
- **Restart a site**: `python main.py execute "restart my-blog site"`
- **Check site status**: `python main.py execute "status of site my-blog"`

### Flexible Command Formats
The intent parser supports multiple natural language patterns:
```bash
# All of these work for starting a site:
python main.py execute "start my-blog"
python main.py execute "start site my-blog"
python main.py execute "start my-blog site"

# Status checking variations:
python main.py execute "status my-blog"
python main.py execute "status of my-blog"
python main.py execute "status of site my-blog"
```

### How It Works
- **Platform Auto-Detection**: Automatically detects if your site uses DDEV (`.ddev/config.yaml`) or Lando (`.lando.yml`)
- **Smart Execution**: Executes the correct platform command for start/stop/restart/status
- **Structured Output**: Returns detailed JSON responses with status, URLs, and next steps
- **Error Handling**: Provides helpful error messages and suggestions

### Example Workflow
```bash
# Create a new site
python main.py execute "create site named my-blog using ddev"
# Returns: URL, admin credentials, directory path

# Start the site
python main.py execute "start my-blog"
# Returns: success status, running confirmation, site URL

# Check status
python main.py execute "status of site my-blog"
# Returns: detailed status information, running services

# Stop the site
python main.py execute "stop my-blog"
# Returns: confirmation of stopped services

# Restart the site
python main.py execute "restart my-blog"
# Returns: restart confirmation, updated status
```

### Site Directory Structure
```
./sites/
├── my-blog/                 # DDEV site
│   ├── .ddev/
│   ├── web/
│   └── composer.json
├── headless-site/           # Lando site  
│   ├── .lando.yml
│   ├── web/
│   └── composer.json
└── another-project/         # Auto-detected platform
    ├── .ddev/ or .lando.yml
    └── ...
```

## 🔍 Troubleshooting

### Common Issues

#### 1. **Authentication Errors**
```
Error: "Authentication failed: 403"
```
**Solutions:**
- Verify `DRUPAL_USERNAME` and `DRUPAL_PASSWORD` in `.env`
- Ensure the user has appropriate permissions (Administrator role recommended)
- Check that the Drupal site is accessible at `DRUPAL_BASE_URL`

#### 2. **AI Generation Fails**
```
Error: "AI provider 'ollama' not configured or unavailable"
```
**Solutions:**
- **For Ollama**: Run `./setup_ollama.sh` or manually install Ollama
- **For OpenAI**: Set `OPENAI_API_KEY` in `.env`
- **For Anthropic**: Set `ANTHROPIC_API_KEY` in `.env`
- Check provider status: `ollama list` or test API keys

#### 3. **Drush Commands Fail**
```
Error: "Command 'drush' not found"
```
**Solutions:**
- Ensure Drush is installed: `composer global require drush/drush`
- Check `DRUSH_PATH` configuration in `.env`
- For DDEV sites: Use `ddev drush` instead of local Drush

#### 4. **Site Creation Fails**
```
Error: "DDEV is not installed" or "Lando is not installed"
```
**Solutions:**
- **DDEV**: Install from https://ddev.com/get-started/
  - macOS: `brew install drud/ddev/ddev`
  - Linux: `curl -LO https://raw.githubusercontent.com/ddev/ddev/master/scripts/install_ddev.sh && bash install_ddev.sh`
- **Lando**: Install from https://docs.lando.dev/basics/installation.html
  - macOS: `brew install lando`
  - Linux: `curl -fsSL https://lando.dev/install.sh | bash`

#### 5. **Site Management Issues**
```
Error: "Site directory not found: ./sites/my-site"
```
**Solutions:**
- Check the site name spelling
- Verify the site was created successfully
- Check `DEFAULT_SITE_DIRECTORY` in `.env`

#### 6. **GraphQL/JSON:API Errors**
```
Error: "GraphQL endpoint not found"
```
**Solutions:**
- Enable GraphQL module in Drupal: `drush en graphql`
- Check `GRAPHQL_ENDPOINT` configuration in `.env`
- Verify Drupal permissions for API access

### Debug Mode

Enable detailed logging to diagnose issues:

```bash
# Enable verbose output
python main.py execute "your command" --verbose

# Or set logging level in code:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Configuration Validation

```bash
# Test all configurations and services
python main.py test

# Validate modular architecture
python test_modular.py

# Check Ollama status
ollama list
curl http://localhost:11434/api/tags
```

### Getting Help

If you encounter issues:

1. **Run diagnostics**: `python main.py test`
2. **Check logs**: Enable verbose mode for detailed error messages
3. **Verify configuration**: Ensure all required environment variables are set
4. **Test individual components**: Try simple commands first
5. **Check dependencies**: Ensure all required tools are installed and accessible

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Add** your command classes following MCP pattern
4. **Test** with various natural language inputs
5. **Submit** a pull request

### Code Standards

- Follow Python PEP 8 style guidelines
- Add type hints to all functions
- Keep command classes under 100 lines
- Include comprehensive error handling

## 📄 License

MIT License - feel free to use this agent in your Drupal projects!

## 🎯 Roadmap

### ✅ Completed Features
- [x] **Modular Command Pattern architecture**
- [x] **Local AI integration with Ollama** 
- [x] **Complete DDEV/Lando site lifecycle management**
- [x] **Natural language processing with regex patterns**
- [x] **Multi-format output (JSON, text, table)**
- [x] **Privacy-focused AI with local models**
- [x] **Comprehensive error handling and troubleshooting**
- [x] **Auto-detection of development platforms**
- [x] **Structured configuration management**
- [x] **Legacy code cleanup and streamlined architecture**
- [x] **Unified main.py entry point**
- [x] **Clean project structure and documentation**

### 🚧 In Progress
- [ ] **Advanced GraphQL query operations**
  - Complex content relationships
  - Custom field queries
  - Taxonomy and media queries
- [ ] **Enhanced content workflows**
  - Content moderation states
  - Workflow automation
  - Bulk operations

### 🔮 Planned Features
- [ ] **Multi-site management dashboard**
  - Manage multiple Drupal instances
  - Cross-site content synchronization
  - Centralized configuration management

- [ ] **Advanced AI capabilities**
  - Content optimization suggestions
  - SEO analysis and recommendations
  - Automated content tagging

- [ ] **Web UI for non-technical users**
  - Browser-based interface
  - Visual command builder
  - Real-time status monitoring

- [ ] **Plugin system for custom commands**
  - Third-party command extensions
  - Custom workflow integrations
  - API for external tools

- [ ] **Deployment and DevOps features**
  - Automated deployment pipelines
  - Environment synchronization
  - Backup and restore operations

- [ ] **Performance and monitoring**
  - Site performance analysis
  - Health monitoring and alerts
  - Resource optimization suggestions

### 💡 Community Ideas
- [ ] **Integration with popular services**
  - GitHub Actions workflows
  - Docker and Kubernetes support
  - CI/CD pipeline integration

- [ ] **Enhanced natural language support**
  - Multi-language command support
  - Voice command integration
  - Conversation-style interactions

---

**Built with ❤️ for the Drupal community**