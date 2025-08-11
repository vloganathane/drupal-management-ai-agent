"""
Configuration module for Drupal AI Agent
Loads environment variables and provides global settings
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class Config:
    """System configuration from environment variables"""
    
    # Drupal Configuration
    drupal_base_url: str = os.getenv('DRUPAL_BASE_URL', 'http://localhost:8080')
    drupal_username: str = os.getenv('DRUPAL_USERNAME', 'admin')
    drupal_password: str = os.getenv('DRUPAL_PASSWORD', 'admin')
    
    # GraphQL Configuration
    graphql_endpoint: str = os.getenv('GRAPHQL_ENDPOINT', '/graphql')
    
    # AI Provider Configuration
    openai_api_key: str = os.getenv('OPENAI_API_KEY', '')
    anthropic_api_key: str = os.getenv('ANTHROPIC_API_KEY', '')
    ollama_base_url: str = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    default_ai_provider: str = os.getenv('DEFAULT_AI_PROVIDER', 'ollama')
    
    # Local LLM Configuration
    ollama_model: str = os.getenv('OLLAMA_MODEL', 'llama3.2:3b')  # Small, efficient model
    ollama_timeout: int = int(os.getenv('OLLAMA_TIMEOUT', '120'))  # Increased timeout for local models
    
    # Development Tools
    drush_path: str = os.getenv('DRUSH_PATH', 'drush')
    ddev_path: str = os.getenv('DDEV_PATH', 'ddev')
    lando_path: str = os.getenv('LANDO_PATH', 'lando')
    
    # Site Setup Configuration
    default_site_directory: str = os.getenv('DEFAULT_SITE_DIRECTORY', './sites')
    default_drupal_version: str = os.getenv('DEFAULT_DRUPAL_VERSION', 'drupal10')
    
    @property
    def graphql_url(self) -> str:
        """Get full GraphQL URL"""
        return f"{self.drupal_base_url.rstrip('/')}{self.graphql_endpoint}"
    
    @property
    def jsonapi_url(self) -> str:
        """Get full JSON:API URL"""
        return f"{self.drupal_base_url.rstrip('/')}/jsonapi"
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.drupal_base_url:
            return False
        
        # At least one AI provider should be configured
        if not any([self.openai_api_key, self.anthropic_api_key, self.ollama_base_url]):
            return False
            
        return True

# Global configuration instance
config = Config()
