# 🤖 Drupal AI Agent

A powerful **modular Python-based AI agent** designed to manage Drupal websites using **natural language commands**. Built with the **Modular Command Pattern (MCP)** and integrated with leading AI providers.

## ✨ Features

- **Natural Language Processing**: Execute Drupal tasks using plain English commands
- **AI-Powered Content Generation**: Create content using OpenAI, Anthropic, or Ollama
- **Modular Command Pattern**: Each operation is a separate, maintainable class
- **Multiple AI Providers**: Support for OpenAI, Anthropic Claude, and local Ollama
- **Comprehensive Drupal Integration**: JSON:API and Drush command execution
- **Local Development Tools**: Create new sites with DDEV or Lando
- **JSON Output**: Structured responses perfect for automation

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the agent files
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Initialize configuration
python main.py setup

# Edit the generated .env file with your settings
nano .env
```

### 3. Test Your Setup

```bash
# Test configuration
python main.py test

# Try your first command
python main.py "clear cache"
```

## 📋 Configuration (.env)

```env
# Drupal Configuration
DRUPAL_BASE_URL=http://localhost:8080
DRUPAL_USERNAME=admin
DRUPAL_PASSWORD=admin

# AI Provider API Keys (configure at least one)
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
DEFAULT_AI_PROVIDER=openai

# Development Tools
DRUSH_PATH=drush
DDEV_PATH=ddev
LANDO_PATH=lando

# Local AI (Ollama)
OLLAMA_BASE_URL=http://localhost:11434
```

## 💬 Natural Language Commands

### Content Management

```bash
# Create AI-generated blog posts
python main.py "Create a blog post about AI in Drupal"
python main.py "Generate an article using Anthropic about the future of headless CMS"

# Edit existing content
python main.py "Edit the title of node 45 to 'Headless CMS in 2025'"

# Upload media with alt text
python main.py "Upload header.jpg to media library with alt text 'Homepage Banner'"
```

### Site Maintenance

```bash
# Cache management
python main.py "Clear Drupal cache"
python main.py "Clear cache and run cron"

# Custom Drush commands
python main.py "Run drush status"
python main.py "Export configuration"
```

### Site Creation

```bash
# Create new Drupal sites
python main.py "Create new Drupal site with DDEV named 'ai-blog'"
python main.py "Create new site using Lando called 'headless-drupal'"
```

## 🏗️ Architecture

### Modular Command Pattern (MCP)

Each operation is implemented as a separate command class:

```
├── Command (Abstract Base Class)
├── CreatePostCommand      # Blog/article creation
├── RunDrushCommand       # Drush command execution
├── EditNodeCommand       # Node editing
├── UploadMediaCommand    # Media file uploads
└── CreateSiteCommand     # New site creation
```

### Key Components

- **NLParser**: Converts natural language to structured commands
- **AIContentGenerator**: Handles content generation across providers
- **DrupalAPI**: Manages JSON:API interactions
- **CommandFactory**: Creates appropriate command instances

## 🤖 AI Integration

### Supported Providers

1. **OpenAI GPT-3.5/4**
   - Best for general content generation
   - Requires `OPENAI_API_KEY`

2. **Anthropic Claude**
   - Excellent for detailed, nuanced content
   - Requires `ANTHROPIC_API_KEY`

3. **Ollama (Local)**
   - Privacy-focused local AI
   - Requires Ollama installation

### Content Generation Examples

```bash
# Using specific AI provider
python main.py "Generate article using OpenAI about Drupal security"
python main.py "Create content with Anthropic about accessibility in web design"

# Default provider (from .env)
python main.py "Write a blog post about PHP 8.3 features"
```

## 📊 JSON Output Format

All commands return structured JSON responses:

```json
{
  "success": true,
  "message": "Created post: AI in Modern Web Development",
  "data": {
    "node_id": 123,
    "url": "http://localhost:8080/node/123",
    "title": "AI in Modern Web Development"
  }
}
```

## 🛠️ Available Commands

### Content Operations
- `CreatePostCommand`: Create new blog posts/articles
- `EditNodeCommand`: Modify existing content
- `UploadMediaCommand`: Upload and manage media files

### Site Management
- `RunDrushCommand`: Execute any Drush command
- Cache clearing, cron execution, configuration export

### Development
- `CreateSiteCommand`: Scaffold new Drupal sites with DDEV/Lando

## 🔧 Extending the Agent

### Adding New Commands

1. Create a new command class inheriting from `Command`:

```python
class CustomCommand(Command):
    def validate_params(self) -> bool:
        return "required_param" in self.params
    
    def execute(self) -> Dict[str, Any]:
        # Your implementation here
        return self.result
```

2. Register in `CommandFactory.command_map`
3. Add parsing patterns to `NLParser.command_patterns`

### Custom AI Providers

Extend `AIContentGenerator` to support additional AI services:

```python
def _generate_custom_ai(self, prompt: str, content_type: str) -> str:
    # Your custom AI integration
    pass
```

## 📦 Dependencies

- **typer**: CLI framework with rich features
- **requests**: HTTP client for Drupal JSON:API
- **python-dotenv**: Environment variable management
- **openai**: OpenAI API integration
- **anthropic**: Anthropic Claude API integration

## 🏃‍♂️ Development Workflow

### Local Development Setup

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Configure Environment**: Edit `.env` with your settings
3. **Test Configuration**: `python main.py test`
4. **Start Coding**: Extend commands as needed

### DDEV Integration

```bash
# Create new Drupal site with DDEV
python main.py "Create new site with DDEV named 'my-project'"

# The agent will:
# 1. Create project directory
# 2. Run composer create-project drupal/recommended-project
# 3. Initialize DDEV configuration
# 4. Start containers and install Drupal
```

### Lando Integration

```bash
# Create new Drupal site with Lando
python main.py "Create new site using Lando called 'headless-site'"

# The agent will:
# 1. Scaffold Drupal with Composer
# 2. Generate .lando.yml configuration
# 3. Start Lando and install Drupal
```

## 🔍 Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify DRUPAL_USERNAME and DRUPAL_PASSWORD in .env
   - Ensure the user has appropriate permissions

2. **AI Generation Fails**
   - Check API keys are correctly set
   - Verify the selected provider is available

3. **Drush Commands Fail**
   - Ensure Drush is installed and in PATH
   - Check DRUSH_PATH configuration

### Debug Mode

Add logging to see detailed execution:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

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

- [ ] GraphQL API support
- [ ] Multi-site management
- [ ] Advanced content workflows
- [ ] Plugin system for custom commands
- [ ] Web UI for non-technical users
- [ ] Backup and deployment commands

---

**Built with ❤️ for the Drupal community**