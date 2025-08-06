#!/usr/bin/env python3
"""
Drupal AI Agent - Natural Language Drupal Management
A modular Python-based AI agent for managing Drupal websites using natural language commands.
"""

import os
import re
import json
import subprocess
import requests
import typer
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import openai
from anthropic import Anthropic
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer(help="Drupal AI Agent - Manage Drupal sites with natural language")

# Configuration
@dataclass
class Config:
    """System configuration from environment variables"""
    drupal_base_url: str = os.getenv('DRUPAL_BASE_URL', 'http://localhost:8080')
    drupal_username: str = os.getenv('DRUPAL_USERNAME', 'admin')
    drupal_password: str = os.getenv('DRUPAL_PASSWORD', 'admin')
    openai_api_key: str = os.getenv('OPENAI_API_KEY', '')
    anthropic_api_key: str = os.getenv('ANTHROPIC_API_KEY', '')
    ollama_base_url: str = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    default_ai_provider: str = os.getenv('DEFAULT_AI_PROVIDER', 'openai')
    drush_path: str = os.getenv('DRUSH_PATH', 'drush')
    ddev_path: str = os.getenv('DDEV_PATH', 'ddev')
    lando_path: str = os.getenv('LANDO_PATH', 'lando')

config = Config()

# Base Command Interface
class Command(ABC):
    """Abstract base class for all commands using MCP pattern"""
    
    def __init__(self, params: Dict[str, Any]):
        self.params = params
        self.result = {"success": False, "message": "", "data": {}}
    
    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """Execute the command and return result"""
        pass
    
    def validate_params(self) -> bool:
        """Validate required parameters"""
        return True

# AI Content Generator
class AIContentGenerator:
    """Handle AI-powered content generation"""
    
    def __init__(self, provider: str = config.default_ai_provider):
        self.provider = provider
        self._setup_clients()
    
    def _setup_clients(self):
        """Initialize AI client based on provider"""
        if self.provider == 'openai' and config.openai_api_key:
            openai.api_key = config.openai_api_key
        elif self.provider == 'anthropic' and config.anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=config.anthropic_api_key)
    
    def generate_content(self, prompt: str, content_type: str = "article") -> str:
        """Generate content using the configured AI provider"""
        try:
            if self.provider == 'openai' and config.openai_api_key:
                return self._generate_openai(prompt, content_type)
            elif self.provider == 'anthropic' and config.anthropic_api_key:
                return self._generate_anthropic(prompt, content_type)
            elif self.provider == 'ollama':
                return self._generate_ollama(prompt, content_type)
            else:
                return f"AI provider '{self.provider}' not configured or unavailable"
        except Exception as e:
            logger.error(f"AI content generation failed: {e}")
            return f"Error generating content: {str(e)}"
    
    def _generate_openai(self, prompt: str, content_type: str) -> str:
        """Generate content using OpenAI"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Generate a {content_type} for a Drupal website. Format with HTML tags appropriate for Drupal content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )
        return response.choices[0].message.content
    
    def _generate_anthropic(self, prompt: str, content_type: str) -> str:
        """Generate content using Anthropic"""
        message = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1500,
            messages=[
                {"role": "user", "content": f"Generate a {content_type} for a Drupal website about: {prompt}. Format with HTML tags appropriate for Drupal content."}
            ]
        )
        return message.content[0].text
    
    def _generate_ollama(self, prompt: str, content_type: str) -> str:
        """Generate content using Ollama"""
        try:
            response = requests.post(
                f"{config.ollama_base_url}/api/generate",
                json={
                    "model": "llama2",
                    "prompt": f"Generate a {content_type} for a Drupal website about: {prompt}",
                    "stream": False
                }
            )
            return response.json().get("response", "No content generated")
        except Exception as e:
            return f"Ollama error: {str(e)}"

# Drupal API Client
class DrupalAPI:
    """Handle Drupal JSON:API interactions"""
    
    def __init__(self):
        self.base_url = config.drupal_base_url.rstrip('/')
        self.session = requests.Session()
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Drupal"""
        try:
            auth_response = self.session.post(
                f"{self.base_url}/user/login?_format=json",
                json={
                    "name": config.drupal_username,
                    "pass": config.drupal_password
                },
                headers={"Content-Type": "application/json"}
            )
            if auth_response.status_code == 200:
                logger.info("Successfully authenticated with Drupal")
            else:
                logger.warning(f"Authentication failed: {auth_response.status_code}")
        except Exception as e:
            logger.error(f"Authentication error: {e}")
    
    def create_node(self, title: str, body: str, content_type: str = "article") -> Dict[str, Any]:
        """Create a new Drupal node"""
        try:
            node_data = {
                "data": {
                    "type": f"node--{content_type}",
                    "attributes": {
                        "title": title,
                        "body": {
                            "value": body,
                            "format": "full_html"
                        },
                        "status": True
                    }
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/jsonapi/node/{content_type}",
                json=node_data,
                headers={"Content-Type": "application/vnd.api+json"}
            )
            
            if response.status_code == 201:
                node = response.json()["data"]
                return {
                    "success": True,
                    "node_id": node["attributes"]["drupal_internal__nid"],
                    "url": f"{self.base_url}/node/{node['attributes']['drupal_internal__nid']}"
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_node(self, node_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing Drupal node"""
        try:
            # First get the node to determine its type
            node_response = self.session.get(f"{self.base_url}/jsonapi/node/article/{node_id}")
            if node_response.status_code != 200:
                return {"success": False, "error": f"Node {node_id} not found"}
            
            node_data = {"data": {"type": "node--article", "id": str(node_id), "attributes": updates}}
            
            response = self.session.patch(
                f"{self.base_url}/jsonapi/node/article/{node_id}",
                json=node_data,
                headers={"Content-Type": "application/vnd.api+json"}
            )
            
            return {"success": response.status_code == 200, "node_id": node_id}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def upload_media(self, file_path: str, alt_text: str = "") -> Dict[str, Any]:
        """Upload media file to Drupal"""
        try:
            if not os.path.exists(file_path):
                return {"success": False, "error": "File not found"}
            
            with open(file_path, 'rb') as f:
                files = {'files[field_media_image_0]': f}
                data = {
                    'alt': alt_text,
                    'title': os.path.basename(file_path)
                }
                
                response = self.session.post(
                    f"{self.base_url}/entity_browser/ajax/upload",
                    files=files,
                    data=data
                )
                
                return {"success": response.status_code == 200}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Command Implementations
class CreatePostCommand(Command):
    """Create a blog post or article"""
    
    def validate_params(self) -> bool:
        return "title" in self.params or "topic" in self.params
    
    def execute(self) -> Dict[str, Any]:
        try:
            ai_generator = AIContentGenerator()
            drupal_api = DrupalAPI()
            
            title = self.params.get("title", self.params.get("topic", "New Post"))
            
            # Generate content if not provided
            if "body" not in self.params:
                prompt = self.params.get("topic", title)
                body = ai_generator.generate_content(prompt, "article")
            else:
                body = self.params["body"]
            
            result = drupal_api.create_node(title, body, self.params.get("type", "article"))
            
            if result["success"]:
                self.result = {
                    "success": True,
                    "message": f"Created post: {title}",
                    "data": {
                        "node_id": result["node_id"],
                        "url": result["url"],
                        "title": title
                    }
                }
            else:
                self.result = {
                    "success": False,
                    "message": f"Failed to create post: {result.get('error', 'Unknown error')}",
                    "data": {}
                }
            
            return self.result
        except Exception as e:
            self.result = {"success": False, "message": f"Error: {str(e)}", "data": {}}
            return self.result

class RunDrushCommand(Command):
    """Execute Drush commands"""
    
    def validate_params(self) -> bool:
        return "command" in self.params
    
    def execute(self) -> Dict[str, Any]:
        try:
            command = self.params["command"]
            drush_cmd = [config.drush_path] + command.split()
            
            result = subprocess.run(
                drush_cmd,
                capture_output=True,
                text=True,
                cwd=self.params.get("site_path", ".")
            )
            
            self.result = {
                "success": result.returncode == 0,
                "message": f"Drush command executed: {command}",
                "data": {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "return_code": result.returncode
                }
            }
            
            return self.result
        except Exception as e:
            self.result = {"success": False, "message": f"Error: {str(e)}", "data": {}}
            return self.result

class EditNodeCommand(Command):
    """Edit an existing Drupal node"""
    
    def validate_params(self) -> bool:
        return "node_id" in self.params and ("title" in self.params or "body" in self.params)
    
    def execute(self) -> Dict[str, Any]:
        try:
            drupal_api = DrupalAPI()
            node_id = int(self.params["node_id"])
            
            updates = {}
            if "title" in self.params:
                updates["title"] = self.params["title"]
            if "body" in self.params:
                updates["body"] = {"value": self.params["body"], "format": "full_html"}
            
            result = drupal_api.update_node(node_id, updates)
            
            if result["success"]:
                self.result = {
                    "success": True,
                    "message": f"Updated node {node_id}",
                    "data": {"node_id": node_id, "url": f"{config.drupal_base_url}/node/{node_id}"}
                }
            else:
                self.result = {
                    "success": False,
                    "message": f"Failed to update node: {result.get('error', 'Unknown error')}",
                    "data": {}
                }
            
            return self.result
        except Exception as e:
            self.result = {"success": False, "message": f"Error: {str(e)}", "data": {}}
            return self.result

class UploadMediaCommand(Command):
    """Upload media files to Drupal"""
    
    def validate_params(self) -> bool:
        return "file_path" in self.params
    
    def execute(self) -> Dict[str, Any]:
        try:
            drupal_api = DrupalAPI()
            file_path = self.params["file_path"]
            alt_text = self.params.get("alt_text", "")
            
            result = drupal_api.upload_media(file_path, alt_text)
            
            if result["success"]:
                self.result = {
                    "success": True,
                    "message": f"Uploaded media: {os.path.basename(file_path)}",
                    "data": {"file_path": file_path, "alt_text": alt_text}
                }
            else:
                self.result = {
                    "success": False,
                    "message": f"Failed to upload media: {result.get('error', 'Unknown error')}",
                    "data": {}
                }
            
            return self.result
        except Exception as e:
            self.result = {"success": False, "message": f"Error: {str(e)}", "data": {}}
            return self.result

class CreateSiteCommand(Command):
    """Create a new Drupal site using DDEV or Lando"""
    
    def validate_params(self) -> bool:
        return "project_name" in self.params
    
    def execute(self) -> Dict[str, Any]:
        try:
            project_name = self.params["project_name"]
            directory = self.params.get("directory", f"./{project_name}")
            domain = self.params.get("domain", f"{project_name}.ddev.site")
            platform = self.params.get("platform", "ddev")
            
            # Create project directory
            Path(directory).mkdir(parents=True, exist_ok=True)
            os.chdir(directory)
            
            if platform.lower() == "ddev":
                return self._create_ddev_site(project_name, domain)
            elif platform.lower() == "lando":
                return self._create_lando_site(project_name, domain)
            else:
                self.result = {"success": False, "message": "Platform must be 'ddev' or 'lando'", "data": {}}
                return self.result
            
        except Exception as e:
            self.result = {"success": False, "message": f"Error: {str(e)}", "data": {}}
            return self.result
    
    def _create_ddev_site(self, project_name: str, domain: str) -> Dict[str, Any]:
        """Create Drupal site using DDEV"""
        try:
            # Create Drupal project with Composer
            subprocess.run(["composer", "create-project", "drupal/recommended-project", ".", "--no-interaction"], check=True)
            
            # Initialize DDEV
            subprocess.run([config.ddev_path, "config", "--project-type=drupal10", f"--project-name={project_name}"], check=True)
            
            # Start DDEV
            subprocess.run([config.ddev_path, "start"], check=True)
            
            # Install Drupal
            subprocess.run([config.ddev_path, "drush", "site:install", "--yes"], check=True)
            
            self.result = {
                "success": True,
                "message": f"Created Drupal site '{project_name}' with DDEV",
                "data": {
                    "project_name": project_name,
                    "url": f"https://{project_name}.ddev.site",
                    "platform": "ddev",
                    "directory": os.getcwd()
                }
            }
            return self.result
            
        except subprocess.CalledProcessError as e:
            self.result = {"success": False, "message": f"DDEV setup failed: {str(e)}", "data": {}}
            return self.result
    
    def _create_lando_site(self, project_name: str, domain: str) -> Dict[str, Any]:
        """Create Drupal site using Lando"""
        try:
            # Create Drupal project with Composer
            subprocess.run(["composer", "create-project", "drupal/recommended-project", ".", "--no-interaction"], check=True)
            
            # Initialize Lando
            lando_config = f"""
name: {project_name}
recipe: drupal10
config:
  webroot: web
proxy:
  appserver:
    - {domain}
"""
            with open(".lando.yml", "w") as f:
                f.write(lando_config)
            
            # Start Lando
            subprocess.run([config.lando_path, "start"], check=True)
            
            # Install Drupal
            subprocess.run([config.lando_path, "drush", "site:install", "--yes"], check=True)
            
            self.result = {
                "success": True,
                "message": f"Created Drupal site '{project_name}' with Lando",
                "data": {
                    "project_name": project_name,
                    "url": f"https://{domain}",
                    "platform": "lando",
                    "directory": os.getcwd()
                }
            }
            return self.result
            
        except subprocess.CalledProcessError as e:
            self.result = {"success": False, "message": f"Lando setup failed: {str(e)}", "data": {}}
            return self.result

# Natural Language Parser
class NLParser:
    """Parse natural language commands into structured commands"""
    
    def __init__(self):
        self.ai_generator = AIContentGenerator()
        self.command_patterns = {
            r"create.*(?:post|article|blog).*about\s+(.+)": ("create-post", "topic"),
            r"create.*(?:post|article|blog).*titled?\s+['\"](.+)['\"]": ("create-post", "title"),
            r"generate.*(?:content|article).*using\s+(\w+).*about\s+(.+)": ("create-post", "ai_content"),
            r"clear.*cache": ("run-drush", "cache-clear"),
            r"run\s+cron": ("run-drush", "cron"),
            r"drush\s+(.+)": ("run-drush", "custom"),
            r"edit.*(?:title|node)\s+(\d+).*to\s+['\"](.+)['\"]": ("edit-node", "title"),
            r"upload\s+(.+?)\s+.*alt.*['\"](.+)['\"]": ("upload-media", "file_alt"),
            r"upload\s+(.+)": ("upload-media", "file"),
            r"create.*(?:new|site).*(?:ddev|lando).*named?\s+['\"]?(.+?)['\"]?": ("create-site", "project"),
        }
    
    def parse(self, command_text: str) -> tuple[str, Dict[str, Any]]:
        """Parse natural language command into intent and parameters"""
        command_text = command_text.lower().strip()
        
        for pattern, (intent, param_type) in self.command_patterns.items():
            match = re.search(pattern, command_text, re.IGNORECASE)
            if match:
                return self._extract_params(intent, param_type, match, command_text)
        
        # Fallback: try to use AI to understand the command
        return self._ai_parse_fallback(command_text)
    
    def _extract_params(self, intent: str, param_type: str, match: re.Match, original: str) -> tuple[str, Dict[str, Any]]:
        """Extract parameters based on pattern match"""
        params = {}
        
        if intent == "create-post":
            if param_type == "topic":
                params = {"topic": match.group(1).strip()}
            elif param_type == "title":
                params = {"title": match.group(1).strip()}
            elif param_type == "ai_content":
                params = {"topic": match.group(2).strip(), "ai_provider": match.group(1).strip()}
        
        elif intent == "run-drush":
            if param_type == "cache-clear":
                params = {"command": "cache:rebuild"}
            elif param_type == "cron":
                params = {"command": "cron:run"}
            elif param_type == "custom":
                params = {"command": match.group(1).strip()}
        
        elif intent == "edit-node":
            if param_type == "title":
                params = {"node_id": match.group(1), "title": match.group(2).strip()}
        
        elif intent == "upload-media":
            if param_type == "file_alt":
                params = {"file_path": match.group(1).strip(), "alt_text": match.group(2).strip()}
            elif param_type == "file":
                params = {"file_path": match.group(1).strip()}
        
        elif intent == "create-site":
            if param_type == "project":
                params = {"project_name": match.group(1).strip()}
                # Detect platform from original command
                if "lando" in original:
                    params["platform"] = "lando"
                else:
                    params["platform"] = "ddev"
        
        return intent, params
    
    def _ai_parse_fallback(self, command_text: str) -> tuple[str, Dict[str, Any]]:
        """Use AI to parse unrecognized commands"""
        try:
            prompt = f"""
            Parse this Drupal management command into a structured format:
            Command: "{command_text}"
            
            Return JSON with:
            - "intent": one of [create-post, run-drush, edit-node, upload-media, create-site, unknown]
            - "params": object with relevant parameters
            
            Examples:
            "Create blog about AI" -> {{"intent": "create-post", "params": {{"topic": "AI"}}}}
            "Clear cache" -> {{"intent": "run-drush", "params": {{"command": "cache:rebuild"}}}}
            """
            
            response = self.ai_generator.generate_content(prompt, "json")
            
            try:
                parsed = json.loads(response)
                return parsed.get("intent", "unknown"), parsed.get("params", {})
            except json.JSONDecodeError:
                return "unknown", {"raw_command": command_text}
                
        except Exception as e:
            logger.error(f"AI parsing failed: {e}")
            return "unknown", {"raw_command": command_text}

# Command Factory
class CommandFactory:
    """Factory to create command instances based on intent"""
    
    command_map = {
        "create-post": CreatePostCommand,
        "run-drush": RunDrushCommand,
        "edit-node": EditNodeCommand,
        "upload-media": UploadMediaCommand,
        "create-site": CreateSiteCommand,
    }
    
    @classmethod
    def create_command(cls, intent: str, params: Dict[str, Any]) -> Optional[Command]:
        """Create a command instance based on intent"""
        command_class = cls.command_map.get(intent)
        if command_class:
            return command_class(params)
        return None

# Main CLI Interface
@app.command()
def execute(
    command: str = typer.Argument(..., help="Natural language command to execute"),
    output_format: str = typer.Option("json", help="Output format (json|text)")
):
    """Execute a natural language Drupal management command"""
    
    try:
        # Parse the natural language command
        parser = NLParser()
        intent, params = parser.parse(command)
        
        if intent == "unknown":
            result = {
                "success": False,
                "message": f"Could not understand command: {command}",
                "data": {"suggestions": ["Try: 'create post about X'", "Try: 'clear cache'", "Try: 'create site named mysite'"]}
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
        
        # Output result
        if output_format == "json":
            typer.echo(json.dumps(result, indent=2))
        else:
            if result["success"]:
                typer.echo(f"✅ {result['message']}")
                if result["data"]:
                    for key, value in result["data"].items():
                        typer.echo(f"   {key}: {value}")
            else:
                typer.echo(f"❌ {result['message']}")
        
    except Exception as e:
        error_result = {"success": False, "message": f"System error: {str(e)}", "data": {}}
        if output_format == "json":
            typer.echo(json.dumps(error_result, indent=2))
        else:
            typer.echo(f"❌ System error: {str(e)}")

@app.command()
def setup():
    """Setup the Drupal AI Agent configuration"""
    typer.echo("🚀 Setting up Drupal AI Agent...")
    
    # Create .env file template
    env_template = """# Drupal AI Agent Configuration
DRUPAL_BASE_URL=http://localhost:8080
DRUPAL_USERNAME=admin
DRUPAL_PASSWORD=admin

# AI Provider API Keys (at least one required)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
DEFAULT_AI_PROVIDER=openai

# Local Development Tools
DRUSH_PATH=drush
DDEV_PATH=ddev
LANDO_PATH=lando

# Ollama (for local AI)
OLLAMA_BASE_URL=http://localhost:11434
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_template)
        typer.echo("✅ Created .env file template")
        typer.echo("📝 Please edit .env with your configuration")
    else:
        typer.echo("⚠️  .env file already exists")
    
    typer.echo("\n📋 Setup checklist:")
    typer.echo("1. Configure your Drupal site URL and credentials in .env")
    typer.echo("2. Add at least one AI provider API key")
    typer.echo("3. Ensure Drush is installed and accessible")
    typer.echo("4. Install DDEV or Lando for site creation features")

@app.command()
def test():
    """Test the Drupal AI Agent configuration"""
    typer.echo("🧪 Testing Drupal AI Agent...")
    
    # Test configuration
    typer.echo(f"Drupal URL: {config.drupal_base_url}")
    typer.echo(f"AI Provider: {config.default_ai_provider}")
    
    # Test AI providers
    ai_gen = AIContentGenerator()
    test_content = ai_gen.generate_content("test", "test")
    if "error" not in test_content.lower():
        typer.echo("✅ AI content generation working")
    else:
        typer.echo("❌ AI content generation failed")
    
    # Test Drupal connection
    try:
        drupal_api = DrupalAPI()
        typer.echo("✅ Drupal connection configured")
    except Exception as e:
        typer.echo(f"❌ Drupal connection failed: {e}")
    
    typer.echo("\n🎯 Try these test commands:")
    typer.echo('python main.py "clear cache"')
    typer.echo('python main.py "create post about testing"')

if __name__ == "__main__":
    app()