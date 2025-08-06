# Drupal AI Agent Configuration Example
# Copy this file to .env and update with your actual values

# === DRUPAL CONFIGURATION ===
DRUPAL_BASE_URL=http://localhost:8080
DRUPAL_USERNAME=admin
DRUPAL_PASSWORD=admin

# === AI PROVIDER API KEYS ===
# Configure at least one AI provider

# OpenAI (GPT-3.5/4)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here

# Default AI provider to use
DEFAULT_AI_PROVIDER=openai

# === LOCAL DEVELOPMENT TOOLS ===
# Paths to your development tools
DRUSH_PATH=drush
DDEV_PATH=ddev
LANDO_PATH=lando

# === LOCAL AI (OLLAMA) ===
# For privacy-focused local AI generation
OLLAMA_BASE_URL=http://localhost:11434

# === ADVANCED CONFIGURATION ===
# Uncomment and modify as needed

# Custom Drupal site paths
# DRUPAL_SITE_PATH=/var/www/html

# Additional Drush aliases
# DRUSH_ALIAS=@local

# Development environment
# ENVIRONMENT=development