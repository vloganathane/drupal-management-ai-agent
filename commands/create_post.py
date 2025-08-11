"""
Create Post Command - Handle blog/article creation with AI content generation
"""

from typing import Dict, Any
from commands.base_command import BaseCommand
from services.ai_service import AIService
from services.jsonapi_service import JSONAPIService
from parsers.parameter_extractor import ParameterExtractor
from utils.logger import get_logger

logger = get_logger(__name__)

class CreatePostCommand(BaseCommand):
    """Create a blog post or article with optional AI content generation"""
    
    def __init__(self, params: Dict[str, Any]):
        super().__init__(params)
        self.ai_service = AIService()
        self.jsonapi_service = JSONAPIService()
        self.extractor = ParameterExtractor()
    
    def validate_params(self) -> bool:
        """Validate that we have either title or topic for content creation"""
        return "title" in self.params or "topic" in self.params
    
    def execute(self) -> Dict[str, Any]:
        """Execute the post creation command"""
        try:
            self.log_execution("Creating new post")
            
            # Extract and validate parameters
            validated_params = self.extractor.extract_content_params(self.params)
            
            # Get title and content
            title = validated_params.get("title", "New Post")
            
            # Generate content if not provided
            if "body" not in validated_params and "topic" in validated_params:
                self.log_execution(f"Generating AI content for topic: {validated_params['topic']}")
                
                provider = validated_params.get("ai_provider")
                if provider:
                    ai_service = AIService(provider)
                else:
                    ai_service = self.ai_service
                
                body = ai_service.generate_content(
                    validated_params["topic"], 
                    validated_params["content_type"]
                )
                
                # Generate taxonomy suggestions
                tags = ai_service.suggest_taxonomy_terms(body)
                if tags:
                    validated_params["tags"] = tags
                    
            else:
                body = validated_params.get("body", "<p>Default content</p>")
            
            # Create the node via JSON:API
            result = self.jsonapi_service.create_node(
                title=title,
                body=body,
                content_type=validated_params["content_type"],
                tags=validated_params.get("tags")
            )
            
            if result["success"]:
                self.set_success(
                    f"Created post: {title}",
                    {
                        "node_id": result["node_id"],
                        "url": result["url"],
                        "title": title,
                        "content_type": validated_params["content_type"],
                        "uuid": result.get("uuid"),
                        "tags": validated_params.get("tags", [])
                    }
                )
            else:
                self.set_error(f"Failed to create post: {result.get('error', 'Unknown error')}")
            
            return self.result
            
        except ValueError as e:
            self.set_error(f"Parameter validation failed: {str(e)}")
            return self.result
        except Exception as e:
            logger.error("Post creation failed: %s", str(e))
            self.set_error(f"Post creation failed: {str(e)}")
            return self.result
