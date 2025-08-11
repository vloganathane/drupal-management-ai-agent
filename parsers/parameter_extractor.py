"""
Parameter Extractor - Extracts structured fields from parsed commands
"""

import re
from typing import Dict, Any, List, Optional
from utils.logger import get_logger

logger = get_logger(__name__)

class ParameterExtractor:
    """Extract and validate parameters from parsed commands"""
    
    def __init__(self):
        pass
    
    def extract_content_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and validate content creation parameters
        
        Args:
            params: Raw parameters from intent parser
            
        Returns:
            Validated content parameters
        """
        validated = {}
        
        # Title extraction
        if "title" in params:
            validated["title"] = self._clean_text(params["title"])
        elif "topic" in params:
            validated["title"] = self._topic_to_title(params["topic"])
        
        # Body content
        if "body" in params:
            validated["body"] = self._clean_html(params["body"])
        
        # Content type
        validated["content_type"] = params.get("content_type", "article")
        
        # AI provider for content generation
        if "ai_provider" in params:
            validated["ai_provider"] = params["ai_provider"]
        
        # Topic for AI generation
        if "topic" in params:
            validated["topic"] = self._clean_text(params["topic"])
        
        # Tags extraction
        if "tags" in params:
            validated["tags"] = self._extract_tags(params["tags"])
        
        return validated
    
    def extract_node_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extract node operation parameters"""
        validated = {}
        
        # Node ID (required for updates/deletes)
        if "node_id" in params:
            try:
                validated["node_id"] = int(params["node_id"])
            except (ValueError, TypeError):
                raise ValueError(f"Invalid node ID: {params['node_id']}")
        
        # Update fields
        if "title" in params:
            validated["title"] = self._clean_text(params["title"])
        
        if "body" in params:
            validated["body"] = self._clean_html(params["body"])
        
        # Content type
        validated["content_type"] = params.get("content_type", "article")
        
        return validated
    
    def extract_media_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extract media upload parameters"""
        validated = {}
        
        # File path (required)
        if "file_path" in params:
            validated["file_path"] = params["file_path"].strip()
        else:
            raise ValueError("File path is required for media upload")
        
        # Alt text
        validated["alt_text"] = params.get("alt_text", "")
        
        # Title
        validated["title"] = params.get("title", self._filename_to_title(validated["file_path"]))
        
        return validated
    
    def extract_drush_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extract Drush command parameters"""
        validated = {}
        
        # Command (required)
        if "command" in params:
            validated["command"] = params["command"]
        else:
            raise ValueError("Drush command is required")
        
        # Module name for enable/disable operations
        if "module" in params:
            validated["module"] = params["module"]
        
        # Additional arguments
        if "args" in params:
            validated["args"] = params["args"] if isinstance(params["args"], list) else [params["args"]]
        
        return validated
    
    def extract_query_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extract GraphQL query parameters"""
        validated = {}
        
        # Query type (required)
        if "query_type" in params:
            validated["query_type"] = params["query_type"]
        else:
            raise ValueError("Query type is required")
        
        # Content type
        validated["content_type"] = params.get("content_type", "article")
        
        # Limit
        validated["limit"] = min(params.get("limit", 10), 100)  # Cap at 100
        
        # Search term
        if "search_term" in params:
            validated["search_term"] = self._clean_text(params["search_term"])
        
        # Role for user queries
        if "role" in params:
            validated["role"] = params["role"]
        
        # Tags for tagged content queries
        if "tags" in params:
            validated["tags"] = self._extract_tags(params["tags"])
        
        # Custom GraphQL query
        if "query" in params:
            validated["query"] = params["query"]
        
        # Query variables
        if "variables" in params:
            validated["variables"] = params["variables"]
        
        return validated
    
    def extract_site_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extract site creation parameters"""
        validated = {}
        
        # Project name (required)
        if "project_name" in params:
            validated["project_name"] = self._clean_project_name(params["project_name"])
        else:
            raise ValueError("Project name is required")
        
        # Platform
        validated["platform"] = params.get("platform", "ddev")
        
        # Directory
        if "directory" in params:
            validated["directory"] = params["directory"]
        
        # Domain
        if "domain" in params:
            validated["domain"] = params["domain"]
        
        return validated
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text input"""
        if not isinstance(text, str):
            return str(text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove quotes if they wrap the entire string
        if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
            text = text[1:-1]
        
        return text.strip()
    
    def _clean_html(self, html: str) -> str:
        """Clean HTML content"""
        # Basic HTML cleaning - in production you might want more sophisticated cleaning
        html = self._clean_text(html)
        
        # Ensure basic HTML structure if it looks like plain text
        if not re.search(r'<[^>]+>', html):
            # Convert line breaks to paragraphs
            paragraphs = html.split('\n\n')
            html = ''.join(f'<p>{p.strip()}</p>' for p in paragraphs if p.strip())
        
        return html
    
    def _topic_to_title(self, topic: str) -> str:
        """Convert topic to a proper title"""
        title = self._clean_text(topic)
        
        # Capitalize first letter of each word
        return ' '.join(word.capitalize() for word in title.split())
    
    def _filename_to_title(self, filepath: str) -> str:
        """Convert filename to a title"""
        import os
        filename = os.path.basename(filepath)
        
        # Remove extension
        name_without_ext = os.path.splitext(filename)[0]
        
        # Replace underscores and hyphens with spaces
        title = re.sub(r'[_-]+', ' ', name_without_ext)
        
        return self._topic_to_title(title)
    
    def _extract_tags(self, tags_input: Any) -> List[str]:
        """Extract and clean taxonomy tags"""
        if isinstance(tags_input, list):
            return [self._clean_text(tag) for tag in tags_input if tag]
        
        if isinstance(tags_input, str):
            # Split by comma, semicolon, or pipe
            tags = re.split(r'[,;|]', tags_input)
            return [self._clean_text(tag) for tag in tags if tag.strip()]
        
        return []
    
    def _clean_project_name(self, name: str) -> str:
        """Clean project name for site creation"""
        name = self._clean_text(name).lower()
        
        # Replace spaces and special characters with hyphens
        name = re.sub(r'[^a-z0-9-]', '-', name)
        
        # Remove multiple consecutive hyphens
        name = re.sub(r'-+', '-', name)
        
        # Remove leading/trailing hyphens
        return name.strip('-')
