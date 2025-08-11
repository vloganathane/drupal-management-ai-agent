"""
Intent Parser - Maps natural language to command intents
"""

import re
from typing import Tuple, Dict, Any
from services.ai_service import AIService
from utils.logger import get_logger

logger = get_logger(__name__)

class IntentParser:
    """Parse natural language commands into structured intents"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.command_patterns = {
            # Content creation
            r"create.*(?:post|article|blog).*about\s+(.+)": ("create-post", "topic"),
            r"create.*(?:post|article|blog).*titled?\s+['\"](.+)['\"]": ("create-post", "title"),
            r"generate.*(?:content|article).*using\s+(\w+).*about\s+(.+)": ("create-post", "ai_content"),
            
            # Node operations
            r"edit.*(?:title|node)\s+(\d+).*to\s+['\"](.+)['\"]": ("edit-node", "title"),
            r"update.*node\s+(\d+).*body.*['\"](.+)['\"]": ("edit-node", "body"),
            r"delete.*node\s+(\d+)": ("delete-node", "node_id"),
            
            # Media operations
            r"upload\s+(.+?)\s+.*alt.*['\"](.+)['\"]": ("upload-media", "file_alt"),
            r"upload\s+(.+)": ("upload-media", "file"),
            
            # Drush operations
            r"clear.*cache": ("run-drush", "cache-clear"),
            r"rebuild.*cache": ("run-drush", "cache-rebuild"),
            r"run\s+cron": ("run-drush", "cron"),
            r"drush\s+(.+)": ("run-drush", "custom"),
            r"enable.*module\s+(.+)": ("run-drush", "enable-module"),
            r"disable.*module\s+(.+)": ("run-drush", "disable-module"),
            
            # GraphQL queries
            r"show.*(?:titles?|list).*(?:latest|recent)\s+(\d+)\s+(?:blog\s+)?posts?": ("query-graphql", "latest_posts"),
            r"get.*(?:latest|recent)\s+(\d+)\s+(?:articles?|posts?)": ("query-graphql", "latest_posts"),
            r"find.*(?:posts?|articles?|nodes?).*about\s+(.+)": ("query-graphql", "search_term"),
            r"search.*(?:for\s+)?content.*about\s+(.+)": ("query-graphql", "search_term"),
            r"fetch.*(?:article|node).*bodies?.*containing.*word\s+['\"]?(\w+)['\"]?": ("query-graphql", "content_search"),
            r"query.*nodes.*(?:type|content_type)\s+['\"]?(\w+)['\"]?": ("query-graphql", "type_filter"),
            r"get.*nodes.*tagged.*['\"](.+)['\"]": ("query-graphql", "tagged_content"),
            
            # User queries
            r"get.*(?:all\s+)?users.*with\s+role\s+['\"]?(\w+)['\"]?": ("query-graphql", "users_by_role"),
            r"show.*users.*with\s+role\s+(\w+)": ("query-graphql", "users_by_role"),
            r"list.*(?:all\s+)?(\w+)s?": ("query-graphql", "users_by_role"),
            
            # Site creation
            r"create.*site.*named?\s+([a-zA-Z0-9\-_]+)": ("create-site", "project"),
            r"create.*(?:new|site).*(?:ddev|lando).*named?\s+['\"]?(.+?)['\"]?": ("create-site", "project"),
            r"create.*(?:site|new).*named?\s+([a-zA-Z0-9\-_]+).*(?:using|with)\s+(?:ddev|lando)": ("create-site", "project"),
            r"setup.*(?:ddev|lando).*site.*['\"]?(.+?)['\"]?": ("create-site", "project"),
            
            # Site management (order matters - more specific patterns first)
            r"restart\s+(?:site\s+)?([a-zA-Z0-9\-_]+)": ("restart-site", "project"),
            r"restart.*(?:site|project)\s+([a-zA-Z0-9\-_]+)": ("restart-site", "project"),
            r"start\s+(?:site\s+)?([a-zA-Z0-9\-_]+)": ("start-site", "project"),
            r"start.*(?:site|project)\s+([a-zA-Z0-9\-_]+)": ("start-site", "project"),
            r"stop\s+(?:site\s+)?([a-zA-Z0-9\-_]+)": ("stop-site", "project"),
            r"stop.*(?:site|project)\s+([a-zA-Z0-9\-_]+)": ("stop-site", "project"),
            r"status\s+(?:of\s+)?(?:site\s+)?([a-zA-Z0-9\-_]+)": ("status-site", "project"),
            r"status.*(?:of|for)\s+(?:site\s+)?([a-zA-Z0-9\-_]+)": ("status-site", "project"),
        }
    
    def parse(self, command_text: str) -> Tuple[str, Dict[str, Any]]:
        """
        Parse natural language command into intent and parameters
        
        Args:
            command_text: Natural language command
            
        Returns:
            Tuple of (intent, parameters)
        """
        command_text = command_text.lower().strip()
        
        # Try pattern matching first
        for pattern, (intent, param_type) in self.command_patterns.items():
            match = re.search(pattern, command_text, re.IGNORECASE)
            if match:
                return self._extract_params(intent, param_type, match, command_text)
        
        # Fallback to AI parsing
        return self._ai_parse_fallback(command_text)
    
    def _extract_params(self, intent: str, param_type: str, match: re.Match, 
                       original: str) -> Tuple[str, Dict[str, Any]]:
        """Extract parameters based on pattern match"""
        params = {}
        
        if intent == "create-post":
            if param_type == "topic":
                params = {"topic": match.group(1).strip()}
            elif param_type == "title":
                params = {"title": match.group(1).strip()}
            elif param_type == "ai_content":
                params = {
                    "topic": match.group(2).strip(), 
                    "ai_provider": match.group(1).strip()
                }
        
        elif intent == "edit-node":
            if param_type == "title":
                params = {"node_id": int(match.group(1)), "title": match.group(2).strip()}
            elif param_type == "body":
                params = {"node_id": int(match.group(1)), "body": match.group(2).strip()}
        
        elif intent == "delete-node":
            if param_type == "node_id":
                params = {"node_id": int(match.group(1))}
        
        elif intent == "upload-media":
            if param_type == "file_alt":
                params = {
                    "file_path": match.group(1).strip(), 
                    "alt_text": match.group(2).strip()
                }
            elif param_type == "file":
                params = {"file_path": match.group(1).strip()}
        
        elif intent == "run-drush":
            if param_type == "cache-clear":
                params = {"command": "cache:clear"}
            elif param_type == "cache-rebuild":
                params = {"command": "cache:rebuild"}
            elif param_type == "cron":
                params = {"command": "cron:run"}
            elif param_type == "custom":
                params = {"command": match.group(1).strip()}
            elif param_type == "enable-module":
                params = {"command": "pm:enable", "module": match.group(1).strip()}
            elif param_type == "disable-module":
                params = {"command": "pm:disable", "module": match.group(1).strip()}
        
        elif intent == "query-graphql":
            if param_type == "latest_posts":
                params = {"query_type": "latest_nodes", "content_type": "article", "limit": int(match.group(1))}
            elif param_type == "search_term":
                params = {"query_type": "search_nodes", "search_term": match.group(1).strip()}
            elif param_type == "content_search":
                params = {"query_type": "search_nodes", "search_term": match.group(1).strip()}
            elif param_type == "type_filter":
                params = {"query_type": "latest_nodes", "content_type": match.group(1).strip()}
            elif param_type == "users_by_role":
                role = match.group(1).strip()
                params = {"query_type": "users_by_role", "role": role}
            elif param_type == "tagged_content":
                tags = [tag.strip() for tag in match.group(1).split(',')]
                params = {"query_type": "nodes_with_tags", "tags": tags}
        
        elif intent == "create-site":
            if param_type == "project":
                params = {"project_name": match.group(1).strip()}
                # Detect platform from original command
                if "lando" in original:
                    params["platform"] = "lando"
                else:
                    params["platform"] = "ddev"
        
        elif intent in ["start-site", "stop-site", "restart-site", "status-site"]:
            if param_type == "project":
                params = {"project_name": match.group(1).strip()}
        
        return intent, params
    
    def _ai_parse_fallback(self, command_text: str) -> Tuple[str, Dict[str, Any]]:
        """Use AI to parse unrecognized commands"""
        try:
            prompt = f'''
            Parse this Drupal management command into a structured format:
            Command: "{command_text}"
            
            Return JSON with:
            - "intent": one of [create-post, edit-node, delete-node, upload-media, run-drush, query-graphql, create-site, start-site, stop-site, restart-site, status-site, unknown]
            - "params": object with relevant parameters
            
            Examples:
            "Create blog about AI" -> {{"intent": "create-post", "params": {{"topic": "AI"}}}}
            "Clear cache" -> {{"intent": "run-drush", "params": {{"command": "cache:clear"}}}}
            "Show latest 5 posts" -> {{"intent": "query-graphql", "params": {{"query_type": "latest_nodes", "content_type": "article", "limit": 5}}}}
            "Start test-blog site" -> {{"intent": "start-site", "params": {{"project_name": "test-blog"}}}}
            "Stop my-site" -> {{"intent": "stop-site", "params": {{"project_name": "my-site"}}}}
            "Status of blog-site" -> {{"intent": "status-site", "params": {{"project_name": "blog-site"}}}}
            '''
            
            response = self.ai_service.generate_content(prompt, "json")
            
            try:
                import json
                parsed = json.loads(response)
                return parsed.get("intent", "unknown"), parsed.get("params", {})
            except json.JSONDecodeError:
                logger.warning("Failed to parse AI response as JSON")
                return "unknown", {"raw_command": command_text}
                
        except Exception as e:
            logger.error("AI parsing failed: %s", str(e))
            return "unknown", {"raw_command": command_text}
