#!/usr/bin/env python3
"""
Drupal AI Agent - Modular Python-based AI agent for Drupal management
Main CLI entry point using the new modular architecture
"""

import typer
from typing import Dict, Any
from pathlib import Path

# Import configuration
from config import config

# Import utilities
from utils.logger import setup_logging, get_logger
from utils.output_formatter import format_output, OutputFormat

# Import parsers
from parsers.intent_parser import IntentParser
from parsers.parameter_extractor import ParameterExtractor

# Import services (for testing)
from services.ai_service import AIService
from services.drush_service import DrushService
from services.site_setup_service import SiteSetupService

# Import commands
from commands.create_post import CreatePostCommand
from commands.create_site import CreateSiteCommand
from commands.site_management import StartSiteCommand, StopSiteCommand, RestartSiteCommand, StatusSiteCommand

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Create Typer app
app = typer.Typer(
    help="Drupal AI Agent - Manage Drupal sites with natural language using MCP + AI + GraphQL + JSON:API"
)

class CommandFactory:
    """Factory to create command instances based on intent"""
    
    command_map = {
        "create-post": CreatePostCommand,
        "create-site": CreateSiteCommand,
        "start-site": StartSiteCommand,
        "stop-site": StopSiteCommand,
        "restart-site": RestartSiteCommand,
        "status-site": StatusSiteCommand,
        # Add other commands as they're implemented
        # "edit-node": EditNodeCommand,
        # "delete-node": DeleteNodeCommand,
        # "upload-media": UploadMediaCommand,
        # "run-drush": RunDrushCommand,
        # "query-graphql": QueryGraphQLCommand,
    }
    
    @classmethod
    def create_command(cls, intent: str, params: Dict[str, Any]):
        """Create a command instance based on intent"""
        command_class = cls.command_map.get(intent)
        if command_class:
            return command_class(params)
        
        # For now, create a simple mock command for unimplemented intents
        return MockCommand(intent, params)

class MockCommand:
    """Temporary mock command for unimplemented commands"""
    
    def __init__(self, intent: str, params: Dict[str, Any]):
        self.intent = intent
        self.params = params
    
    def validate_params(self) -> bool:
        return True
    
    def execute(self) -> Dict[str, Any]:
        return {
            "success": True,
            "message": f"Mock execution of {self.intent}",
            "data": {
                "intent": self.intent,
                "params": self.params,
                "note": "This is a mock response - command not yet implemented"
            }
        }

@app.command()
def execute(
    command: str = typer.Argument(..., help="Natural language command to execute"),
    output_format: str = typer.Option("json", help="Output format (json|text|table)"),
    ai_provider: str = typer.Option(None, help="Override AI provider (openai|anthropic|ollama)")
):
    """Execute a natural language Drupal management command"""
    
    try:
        logger.info("Processing command: %s", command)
        
        # Parse the natural language command
        parser = IntentParser()
        intent, params = parser.parse(command)
        
        # Override AI provider if specified
        if ai_provider and intent == "create-post":
            params["ai_provider"] = ai_provider
        
        logger.info("Parsed intent: %s, params: %s", intent, params)
        
        if intent == "unknown":
            result = {
                "success": False,
                "message": f"Could not understand command: {command}",
                "data": {
                    "suggestions": [
                        "Try: 'create post about X'",
                        "Try: 'clear cache'", 
                        "Try: 'show latest 10 posts'",
                        "Try: 'get users with role editor'",
                        "Try: 'create site named mysite'"
                    ]
                }
            }
        else:
            # Create and execute command
            cmd = CommandFactory.create_command(intent, params)
            if cmd and cmd.validate_params():
                result = cmd.execute()
            else:
                result = {
                    "success": False,
                    "message": f"Invalid parameters for {intent}",
                    "data": {"intent": intent, "params": params}
                }
        
        # Format and output result
        output_fmt = OutputFormat(output_format.lower())
        formatted_output = format_output(result, output_fmt)
        typer.echo(formatted_output)
        
    except Exception as e:
        logger.error("Command execution failed: %s", str(e))
        error_result = {
            "success": False, 
            "message": f"System error: {str(e)}", 
            "data": {}
        }
        
        output_fmt = OutputFormat(output_format.lower())
        formatted_output = format_output(error_result, output_fmt)
        typer.echo(formatted_output)

@app.command()
def setup():
    """Setup the Drupal AI Agent configuration"""
    typer.echo("🚀 Setting up Drupal AI Agent (Modular Architecture)...")
    
    # Create .env file template if it doesn't exist
    env_template = """# Drupal AI Agent Configuration
DRUPAL_BASE_URL=http://localhost:8080
DRUPAL_USERNAME=admin
DRUPAL_PASSWORD=admin

# GraphQL Configuration
GRAPHQL_ENDPOINT=/graphql

# AI Provider API Keys (configure at least one)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
DEFAULT_AI_PROVIDER=openai

# Local Development Tools
DRUSH_PATH=drush
DDEV_PATH=ddev
LANDO_PATH=lando

# Site Setup
DEFAULT_SITE_DIRECTORY=./sites
DEFAULT_DRUPAL_VERSION=drupal10

# Ollama (for local AI)
OLLAMA_BASE_URL=http://localhost:11434
"""
    
    env_file = Path('.env')
    if not env_file.exists():
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_template)
        typer.echo("✅ Created .env file template")
        typer.echo("📝 Please edit .env with your configuration")
    else:
        typer.echo("⚠️  .env file already exists")
    
    # Validate configuration
    if config.validate():
        typer.echo("✅ Configuration validation passed")
    else:
        typer.echo("❌ Configuration validation failed")
        typer.echo("   Please check your .env file settings")
    
    typer.echo("\n📋 Setup checklist:")
    typer.echo("1. Configure your Drupal site URL and credentials in .env")
    typer.echo("2. Add at least one AI provider API key")
    typer.echo("3. Ensure Drush is installed and accessible")
    typer.echo("4. Install DDEV or Lando for site creation features")
    typer.echo("5. Enable GraphQL module in your Drupal site")

@app.command()
def test():
    """Test the Drupal AI Agent configuration and services"""
    typer.echo("🧪 Testing Drupal AI Agent (Modular Architecture)...")
    
    # Test configuration
    typer.echo(f"Drupal URL: {config.drupal_base_url}")
    typer.echo(f"GraphQL URL: {config.graphql_url}")
    typer.echo(f"JSON:API URL: {config.jsonapi_url}")
    typer.echo(f"AI Provider: {config.default_ai_provider}")
    
    # Test AI service
    try:
        ai_service = AIService()
        test_content = ai_service.generate_content("test", "test")
        if "error" not in test_content.lower():
            typer.echo("✅ AI content generation working")
        else:
            typer.echo(f"❌ AI content generation failed: {test_content}")
    except Exception as e:
        typer.echo(f"❌ AI service test failed: {e}")
    
    # Test Drush service
    try:
        drush_service = DrushService()
        status = drush_service.get_site_status()
        if status["success"]:
            typer.echo("✅ Drush service working")
        else:
            typer.echo(f"❌ Drush service failed: {status.get('error', 'Unknown error')}")
    except Exception as e:
        typer.echo(f"❌ Drush service test failed: {e}")
    
    typer.echo("\n🎯 Try these test commands:")
    typer.echo('python main.py execute "create post about testing modular architecture"')
    typer.echo('python main.py execute "clear cache" --output-format text')
    typer.echo('python main.py execute "show latest 5 blog posts"')
    typer.echo('python main.py execute "create site with ddev named test-site"')

@app.command()
def create_site(
    name: str = typer.Argument(..., help="Project name"),
    platform: str = typer.Option("ddev", help="Platform to use (ddev|lando)"),
    directory: str = typer.Option(None, help="Target directory")
):
    """Create a new Drupal site using DDEV or Lando (Test Case Implementation)"""
    
    typer.echo(f"🚀 Creating Drupal site '{name}' using {platform.upper()}...")
    
    try:
        site_service = SiteSetupService(platform)
        result = site_service.create_site(name, directory)
        
        if result["success"]:
            typer.echo("✅ Site creation successful!")
            typer.echo(f"   URL: {result['data']['url']}")
            typer.echo(f"   Directory: {result['data']['directory']}")
            typer.echo(f"   Admin: {result['data']['admin_user']} / {result['data']['admin_pass']}")
        else:
            typer.echo(f"❌ Site creation failed: {result['error']}")
            
    except Exception as e:
        typer.echo(f"❌ Site creation error: {str(e)}")

if __name__ == "__main__":
    app()
